from __future__ import annotations

import asyncio
import json
from collections import Counter
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from config import settings
from game.roles import assign_roles, validate_custom
from locales import t


class GameEngine:
    """Authoritative server-side Mafia state machine.

    Telegram callbacks are treated as untrusted input. Every action is revalidated
    against the DB state before it is accepted.
    """

    def __init__(self, db, bot):
        self.db = db
        self.bot = bot
        self.tasks: dict[int, asyncio.Task] = {}
        self.locks: dict[int, asyncio.Lock] = {}
        self.last_word_player: dict[int, int] = {}

    def lock(self, game_id: int) -> asyncio.Lock:
        return self.locks.setdefault(game_id, asyncio.Lock())

    async def schedule(self, game_id: int, callback, seconds: int):
        old = self.tasks.pop(game_id, None)
        if old and not old.done():
            old.cancel()

        async def runner():
            try:
                await asyncio.sleep(max(0, seconds))
                await callback(game_id)
            except asyncio.CancelledError:
                pass
            except Exception as exc:
                await self.db.log("ERROR", game_id, details=f"timer {callback.__name__}: {type(exc).__name__}: {exc}")

        self.tasks[game_id] = asyncio.create_task(runner())

    async def cancel_timer(self, game_id):
        task = self.tasks.pop(game_id, None)
        if task and not task.done():
            task.cancel()

    async def _private_preflight(self, rows, game):
        """Verify every participant can receive private bot messages before the game state advances."""
        failed = []
        for _, user in rows:
            lang = await self.db.language(user.telegram_id, game.language)
            try:
                await self.bot.send_message(user.telegram_id, t(lang, "preflight_ok"))
            except Exception as exc:
                failed.append(user.full_name)
                await self.db.log("ERROR", game.id, user.telegram_id, f"private preflight failed: {type(exc).__name__}: {exc}")
        return failed

    async def start(self, game_id: int):
        async with self.lock(game_id):
            game = await self.db.game(game_id)
            rows = await self.db.players(game_id)
            if not game or not game.active:
                return False, "inactive"
            if len(rows) < settings.min_players:
                return False, "not_enough"
            if len(rows) > settings.max_players:
                return False, "too_many"
            try:
                cfg = json.loads(game.role_config or "{}")
                validate_custom(game.player_limit, int(cfg.get("mafia", 0)), int(cfg.get("doctor", 0)), int(cfg.get("commissioner", 0)), int(cfg.get("lover", 0)), int(cfg.get("detective", 0)), int(cfg.get("bodyguard", 0)))
            except (ValueError, TypeError, json.JSONDecodeError):
                return False, "role_config_invalid"
            if len(rows) != game.player_limit:
                return False, "not_enough"
            for _, u in rows:
                user = await self.db.user_stats(u.telegram_id)
                if not user or not user.started_bot:
                    return False, "private_not_started"
            failed = await self._private_preflight(rows, game)
            if failed:
                return False, "private_delivery_failed"
            if game.ready_required:
                await self.db.set_phase(game_id, "READY_CHECK", settings.ready_timeout)
                for p, u in rows:
                    await self.db.set_ready(game_id, u.telegram_id, False)
                    lang = await self.db.language(u.telegram_id, game.language)
                    try:
                        await self.bot.send_message(u.telegram_id, t(lang, "ready_title"), reply_markup=self.ready_keyboard(lang, game_id))
                    except Exception as exc:
                        await self.db.log("ERROR", game_id, u.telegram_id, f"ready prompt failed: {type(exc).__name__}: {exc}")
                try:
                    await self.bot.send_group_message(game.chat_id, t(game.language, "game_starting"))
                except Exception as exc:
                    await self.db.log("ERROR", game_id, details=f"start announcement failed: {type(exc).__name__}: {exc}")
                await self.schedule(game_id, self.ready_check, settings.ready_timeout)
            else:
                await self.db.set_phase(game_id, "ROLE_DISTRIBUTION", None)
                try:
                    await self.bot.send_group_message(game.chat_id, t(game.language, "game_starting"))
                except Exception as exc:
                    await self.db.log("ERROR", game_id, details=f"start announcement failed: {type(exc).__name__}: {exc}")
                await self._distribute_roles_and_night(game_id)
            return True, "ok"

    def ready_keyboard(self, lang, game_id):
        return InlineKeyboardMarkup([[InlineKeyboardButton(t(lang, "ready_yes"), callback_data=f"ready:{game_id}:1"),
                                      InlineKeyboardButton(t(lang, "ready_no"), callback_data=f"ready:{game_id}:0")]])

    async def recover_role_distribution(self, game_id):
        async with self.lock(game_id):
            game = await self.db.game(game_id)
            if not game or not game.active or game.phase != "ROLE_DISTRIBUTION":
                return
            await self._distribute_roles_and_night(game_id)

    async def ready_check(self, game_id):
        async with self.lock(game_id):
            game = await self.db.game(game_id)
            rows = await self.db.players(game_id)
            if not game or not game.active or game.phase != "READY_CHECK":
                return
            if rows and all(p.ready for p, _ in rows):
                await self._distribute_roles_and_night(game_id)
            else:
                await self.db.set_phase(game_id, "LOBBY", None)
                await self.bot.send_group_message(game.chat_id, t(game.language, "ready_failed"))

    async def _distribute_roles_and_night(self, game_id):
        rows = await self.db.players(game_id)
        if not rows or any(p.role is None for p, _ in rows):
            assignments = assign_roles([u.telegram_id for _, u in rows], json.loads(game.role_config or "{}") or None)
            await self.db.assign_roles(game_id, assignments)
            rows = await self.db.players(game_id)
        game = await self.db.game(game_id)
        for p, u in rows:
            lang = await self.db.language(u.telegram_id, game.language)
            try:
                await self.bot.send_message(u.telegram_id, t(lang, "role_sent", role=t(lang, p.role), description=t(lang, f"{p.role}_desc")))
                try:
                    await self.bot.send_message(u.telegram_id, t(lang, f"{p.role}_guide"))
                except Exception:
                    pass
                if p.role == "mafia":
                    mates = [f"{v.full_name} (@{v.username})" if v.username else v.full_name for q, v in rows if q.role == "mafia" and v.telegram_id != u.telegram_id]
                    if mates:
                        await self.bot.send_message(u.telegram_id, t(lang, "mafia_team", names=", ".join(mates)))
            except Exception as exc:
                await self.db.log("ERROR", game_id, u.telegram_id, f"role delivery failed: {type(exc).__name__}: {exc}")
                await self._cancel_locked(game_id, "private role delivery failed")
                return
        await self._night(game_id)

    async def night(self, game_id):
        async with self.lock(game_id):
            await self._night(game_id)

    async def _night(self, game_id):
        game = await self.db.game(game_id)
        if not game or not game.active:
            return
        await self.db.set_game_fields(game_id, night_number=game.night_number + 1, extra_time_used=False)
        await self.db.set_phase(game_id, "NIGHT", game.night_timeout)
        game = await self.db.game(game_id)
        await self.bot.lock_group(game.chat_id)
        try:
            await self.bot.send_phase_media(game.chat_id, "night", game.language,
                                             t(game.language, "night", seconds=game.night_timeout))
        except Exception as exc:
            await self.db.log("ERROR", game_id, details=f"night announcement failed: {type(exc).__name__}: {exc}")
        await self.send_night_actions(game_id)
        await self.schedule(game_id, self.resolve_night, game.night_timeout)

    async def send_night_actions(self, game_id):
        game = await self.db.game(game_id)
        rows = await self.db.players(game_id)
        alive = [(p, u) for p, u in rows if p.alive]
        mafia_ids = {u.telegram_id for p, u in alive if p.role == "mafia"}
        for p, u in alive:
            lang = await self.db.language(u.telegram_id, game.language)
            try:
                if p.role == "mafia":
                    targets = [(tp, tu) for tp, tu in alive if tu.telegram_id not in mafia_ids]
                    await self.bot.send_message(u.telegram_id, t(lang, "mafia_wait"), reply_markup=self.target_keyboard(targets, "mafia", game.id, game.night_number, lang))
                elif p.role == "doctor":
                    targets = []
                    for tp, tu in alive:
                        if tu.telegram_id == u.telegram_id and (not game.doctor_self_heal or p.doctor_self_heal_count >= game.doctor_self_heal_uses):
                            continue
                        if not game.doctor_repeat_target and p.last_doctor_target == tu.telegram_id:
                            continue
                        targets.append((tp, tu))
                    await self.bot.send_message(u.telegram_id, t(lang, "doctor_action"), reply_markup=self.target_keyboard(targets, "doctor", game.id, game.night_number, lang))
                elif p.role == "commissioner":
                    targets = [(tp, tu) for tp, tu in alive if tu.telegram_id != u.telegram_id]
                    await self.bot.send_message(u.telegram_id, t(lang, "commissioner_action"), reply_markup=self.target_keyboard(targets, "check", game.id, game.night_number, lang))
                    if game.night_number >= 2 and game.commissioner_eliminate:
                        await self.bot.send_message(u.telegram_id, t(lang, "commissioner_eliminate"), reply_markup=self.target_keyboard(targets, "eliminate", game.id, game.night_number, lang))
                elif p.role == "lover":
                    targets = [(tp, tu) for tp, tu in alive if tu.telegram_id != u.telegram_id]
                    await self.bot.send_message(u.telegram_id, t(lang, "lover_action"), reply_markup=self.target_keyboard(targets, "block", game.id, game.night_number, lang))
                elif p.role == "detective":
                    targets = [(tp, tu) for tp, tu in alive if tu.telegram_id != u.telegram_id]
                    await self.bot.send_message(u.telegram_id, t(lang, "detective_action"), reply_markup=self.target_keyboard(targets, "detect", game.id, game.night_number, lang))
                elif p.role == "bodyguard":
                    targets = [(tp, tu) for tp, tu in alive if tu.telegram_id != u.telegram_id]
                    await self.bot.send_message(u.telegram_id, t(lang, "bodyguard_action"), reply_markup=self.target_keyboard(targets, "guard", game.id, game.night_number, lang))
            except Exception as exc:
                await self.db.log("ERROR", game_id, u.telegram_id, f"night action delivery failed: {type(exc).__name__}: {exc}")

    @staticmethod
    def target_keyboard(players, kind, game_id, night_number, lang):
        rows = [[InlineKeyboardButton(u.full_name[:32], callback_data=f"act:{game_id}:{night_number}:{kind}:{u.telegram_id}")] for _, u in players]
        if kind == "mafia": rows.append([InlineKeyboardButton(t(lang, "mafia_chat"), callback_data=f"mafia:chat:{game_id}")])
        return InlineKeyboardMarkup(rows)

    async def resolve_night(self, game_id):
        async with self.lock(game_id):
            game = await self.db.game(game_id)
            if not game or not game.active or game.phase != "NIGHT":
                return
            rows = await self.db.players(game_id)
            alive = {u.telegram_id: (p, u) for p, u in rows if p.alive}
            mafia_actions = [a for a in await self.db.action_targets(game_id, "mafia")
                             if a.user_id in alive and alive[a.user_id][0].role == "mafia"]
            mafia_count = sum(1 for p, _ in rows if p.alive and p.role == "mafia")
            mafia_target, consensus = self._mafia_target(mafia_actions, alive.keys(), mafia_count)
            if consensus:
                await self.bot.notify_mafia_consensus(game_id, mafia_target)
            # Lover blocks a target's night ability.
            blocked_actions = {a.target_user_id for a in await self.db.action_targets(game_id, "block") if a.user_id in alive and alive[a.user_id][0].role == "lover" and a.target_user_id in alive}
            if mafia_target in blocked_actions: mafia_target = None
            doctor_actions = [a for a in await self.db.action_targets(game_id, "doctor") if a.user_id in alive and alive[a.user_id][0].role == "doctor" and a.user_id not in blocked_actions]
            doctor_target = doctor_actions[-1].target_user_id if doctor_actions and doctor_actions[-1].target_user_id in alive else None
            shoot_actions = [a for a in await self.db.action_targets(game_id, "eliminate") if a.user_id in alive and alive[a.user_id][0].role == "commissioner" and a.user_id not in blocked_actions]
            shoot_target = shoot_actions[-1].target_user_id if shoot_actions and shoot_actions[-1].target_user_id in alive else None
            guard_actions = [a for a in await self.db.action_targets(game_id, "guard") if a.user_id in alive and alive[a.user_id][0].role == "bodyguard" and a.user_id not in blocked_actions]
            guard_target = guard_actions[-1].target_user_id if guard_actions and guard_actions[-1].target_user_id in alive else None

            killed = {uid for uid in (mafia_target, shoot_target) if uid}
            if guard_target in killed:
                killed.discard(guard_target)
            saved = doctor_target in killed if doctor_target else False
            if doctor_target:
                killed.discard(doctor_target)
            if guard_target and guard_target in alive and any(target in killed for target in {guard_target}):
                killed.discard(guard_target)
            # A bodyguard protects another player; if that protected player was attacked, the attack is cancelled.
            if guard_target and guard_target not in killed:
                # The guard target is the protected player; reconstruct attack sources.
                attacked_targets={x for x in (mafia_target,shoot_target) if x}
                if guard_target in attacked_targets:
                    killed.discard(guard_target)
            for uid in killed:
                await self.db.eliminate(game_id, uid)

            checks = [a for a in await self.db.action_targets(game_id, "check")
                      if a.user_id in alive and alive[a.user_id][0].role == "commissioner"]
            for action in checks:
                target = alive.get(action.target_user_id)
                if not target or action.user_id in blocked_actions:
                    continue
                lang = await self.db.language(action.user_id, game.language)
                result = t(lang, "check_mafia") if target[0].role == "mafia" else t(lang, "check_not_mafia")
                try:
                    await self.bot.send_message(action.user_id, t(lang, "commissioner_result", name=target[1].full_name, result=result))
                except Exception as exc:
                    await self.db.log("ERROR", game_id, action.user_id, f"commissioner result delivery failed: {type(exc).__name__}: {exc}")
            detective_checks = await self.db.action_targets(game_id, "detect")
            for action in detective_checks:
                target = alive.get(action.target_user_id)
                if not target or action.user_id in blocked_actions:
                    continue
                lang = await self.db.language(action.user_id, game.language)
                activity = await self.db.action_targets(game_id, "detect")
                # Detective receives a simple faction result without exposing the exact role.
                result = t(lang, "detective_mafia") if target[0].role == "mafia" else t(lang, "detective_not_mafia")
                try:
                    await self.bot.send_message(action.user_id, t(lang, "detective_result", name=target[1].full_name, result=result))
                except Exception as exc:
                    await self.db.log("ERROR", game_id, action.user_id, f"detective result delivery failed: {type(exc).__name__}: {exc}")

            await self.db.clear_actions(game_id)
            try:
                await self.bot.send_night_result(game_id, killed, saved)
            except Exception as exc:
                await self.db.log("ERROR", game_id, details=f"night result delivery failed: {type(exc).__name__}: {exc}")
            winner = await self.check_winner(game_id)
            if winner:
                await self._finish(game_id, winner)
                return
            await self._day(game_id)

    @staticmethod
    def _mafia_target(actions, alive_ids, mafia_count):
        """Shared Mafia decision:
        - everyone active chooses the same target -> immediate consensus;
        - if some Mafia never chooses, the first/proposed target can resolve at timeout;
        - if several targets exist, the largest proposal group wins;
        - a tie means no attack.
        """
        valid = [a.target_user_id for a in actions if a.target_user_id in alive_ids]
        if not valid:
            return None, False
        counts = Counter(valid)
        leaders = sorted(counts, key=lambda x: (-counts[x], x))
        top = leaders[0]
        top_count = counts[top]
        if len(valid) == mafia_count and top_count == mafia_count:
            return top, True
        if top_count > len(valid) / 2:
            return top, False
        if len(valid) < mafia_count and len(set(valid)) == 1:
            return top, False
        if len(leaders) > 1 and counts[leaders[0]] == counts[leaders[1]]:
            return None, False
        return top, False


    async def maybe_resolve_night(self, game_id):
        """Resolve early only when every required night role has submitted a valid action."""
        ready = False
        async with self.lock(game_id):
            game=await self.db.game(game_id)
            if not game or not game.active or game.phase!="NIGHT": return
            rows=await self.db.players(game_id); alive=[(p,u) for p,u in rows if p.alive]
            mafia=[u.telegram_id for p,u in alive if p.role=="mafia"]
            ma=await self.db.action_targets(game_id,"mafia")
            targets={a.target_user_id for a in ma if a.user_id in mafia}
            if not mafia or len(targets)!=1 or len([a for a in ma if a.user_id in mafia])<len(mafia): return
            required_roles={"doctor":"doctor","commissioner":"check","lover":"block","detective":"detect","bodyguard":"guard"}
            for role,kind in required_roles.items():
                ids=[u.telegram_id for p,u in alive if p.role==role]
                actions=await self.db.action_targets(game_id,kind)
                if ids and not any(a.user_id in ids for a in actions): return
            ready=True
        if ready: await self.resolve_night(game_id)
    async def day(self, game_id):
        async with self.lock(game_id):
            await self._day(game_id)

    async def _day(self, game_id):
        game = await self.db.game(game_id)
        if not game or not game.active:
            return
        await self.db.set_game_fields(game_id, day_number=game.day_number + 1, extra_time_used=False)
        await self.db.set_phase(game_id, "DISCUSSION", game.discussion_timeout)
        game = await self.db.game(game_id)
        await self.bot.open_day(game.chat_id)
        try:
            await self.bot.send_phase_media(game.chat_id, "day", game.language,
                                             t(game.language, "discussion", seconds=game.discussion_timeout))
            await self.bot.send_extra_time_button(game_id)
        except Exception as exc:
            await self.db.log("ERROR", game_id, details=f"day announcement failed: {type(exc).__name__}: {exc}")
        await self.schedule(game_id, self.start_voting, game.discussion_timeout)

    async def request_extra_time(self, game_id):
        async with self.lock(game_id):
            game = await self.db.game(game_id)
            if not game or not game.active or game.phase != "DISCUSSION" or game.extra_time_used or not game.extra_time_enabled:
                return False
            await self.db.clear_extra_votes(game_id)
            await self.db.set_phase(game_id, "EXTRA_TIME", 20)
            await self.bot.send_extra_time_request(game_id)
            await self.schedule(game_id, self.resolve_extra_time, 20)
            return True

    async def resolve_extra_time(self, game_id):
        async with self.lock(game_id):
            game = await self.db.game(game_id)
            if not game or not game.active or game.phase != "EXTRA_TIME":
                return
            yes, _ = await self.db.extra_counts(game_id)
            alive = len(await self.db.alive_ids(game_id))
            approved = alive > 0 and yes * 100 >= alive * game.extra_time_approval_percent
            if approved:
                await self.db.set_game_fields(game_id, extra_time_used=True)
                await self.db.set_phase(game_id, "DISCUSSION", game.extra_time_seconds)
                await self.bot.send_group_message(game.chat_id, t(game.language, "extra_added"))
                await self.schedule(game_id, self.start_voting, game.extra_time_seconds)
            else:
                await self.bot.send_group_message(game.chat_id, t(game.language, "extra_denied"))
                await self._start_voting(game_id)

    async def start_voting(self, game_id):
        async with self.lock(game_id):
            await self._start_voting(game_id)

    async def _start_voting(self, game_id):
        game = await self.db.game(game_id)
        if not game or not game.active or game.phase not in {"DISCUSSION", "EXTRA_TIME"}:
            return
        await self.db.set_phase(game_id, "VOTING", game.voting_timeout)
        await self.db.set_game_fields(game_id, voting_round=1)
        await self.db.clear_votes(game_id)
        await self.bot.lock_group(game.chat_id)
        try:
            await self.bot.send_group_message(game.chat_id, t(game.language, "voting"))
        except Exception as exc:
            await self.db.log("ERROR", game_id, details=f"voting announcement failed: {type(exc).__name__}: {exc}")
        rows = await self.db.players(game_id)
        alive = [(p, u) for p, u in rows if p.alive]
        for p, u in alive:
            lang = await self.db.language(u.telegram_id, game.language)
            try:
                await self.bot.send_message(u.telegram_id, t(lang, "vote"), reply_markup=self.vote_keyboard(alive, lang, game.allow_skip_vote, game.id, game.voting_round))
            except Exception as exc:
                await self.db.log("ERROR", game_id, u.telegram_id, f"vote prompt delivery failed: {type(exc).__name__}: {exc}")
        await self.schedule(game_id, self.resolve_vote, game.voting_timeout)

    @staticmethod
    def vote_keyboard(alive, lang, allow_skip=True, game_id=None, voting_round=1):
        rows = [[InlineKeyboardButton(u.full_name[:32], callback_data=f"vote:{game_id}:{voting_round}:{u.telegram_id}")] for _, u in alive]
        if allow_skip:
            rows.append([InlineKeyboardButton(t(lang, "skip"), callback_data=f"vote:{game_id}:{voting_round}:0")])
        return InlineKeyboardMarkup(rows)

    async def resolve_vote(self, game_id):
        async with self.lock(game_id):
            game = await self.db.game(game_id)
            if not game or not game.active or game.phase != "VOTING":
                return
            counts = await self.db.vote_counts(game_id)
            rows = await self.db.players(game_id)
            names = {u.telegram_id: u.full_name for _, u in rows}
            result_lines = [f"• {names.get(uid, uid)} — {count}" for uid, count in sorted(counts.items(), key=lambda x: (-x[1], str(names.get(x[0], x[0]))))]
            try:
                await self.bot.send_group_message(game.chat_id, t(game.language, "results", results="\n".join(result_lines) or "—"))
            except Exception as exc:
                await self.db.log("ERROR", game_id, details=f"vote result delivery failed: {type(exc).__name__}: {exc}")
            if not counts:
                await self._night(game_id)
                return
            top = max(counts.values())
            leaders = [uid for uid, count in counts.items() if count == top]
            if 0 in leaders:
                await self.bot.send_group_message(game.chat_id, t(game.language, "no_elimination"))
                await self._night(game_id)
                return
            tied = leaders
            if len(tied) > 1 and game.tie_revote:
                await self.db.set_game_fields(game_id, voting_round=2, revote_candidates=json.dumps(tied))
                await self.db.set_phase(game_id, "VOTING_REVOTE", settings.voting_timeout)
                await self.db.clear_votes(game_id)
                try:
                    await self.bot.send_group_message(game.chat_id, t(game.language, "tie"))
                except Exception as exc:
                    await self.db.log("ERROR", game_id, details=f"tie announcement failed: {type(exc).__name__}: {exc}")
                alive_tied = [(p, u) for p, u in rows if p.alive and u.telegram_id in tied]
                for p, u in rows:
                    if p.alive:
                        lang = await self.db.language(u.telegram_id, game.language)
                        try:
                            await self.bot.send_message(u.telegram_id, t(lang, "revote"), reply_markup=self.vote_keyboard(alive_tied, lang, game.allow_skip_vote, game.id, game.voting_round))
                        except Exception as exc:
                            await self.db.log("ERROR", game_id, u.telegram_id, f"revote prompt delivery failed: {type(exc).__name__}: {exc}")
                await self.schedule(game_id, self.resolve_revote, game.voting_timeout)
                return
            if len(tied) > 1:
                await self.bot.send_group_message(game.chat_id, t(game.language, "no_elimination"))
                await self._night(game_id)
                return
            await self._eliminate_and_last_word(game_id, tied[0])

    async def resolve_revote(self, game_id):
        async with self.lock(game_id):
            game = await self.db.game(game_id)
            if not game or not game.active or game.phase != "VOTING_REVOTE":
                return
            counts = await self.db.vote_counts(game_id)
            if not counts:
                await self.bot.send_group_message(game.chat_id, t(game.language, "no_elimination"))
                await self._night(game_id)
                return
            top = max(counts.values())
            leaders = [uid for uid, count in counts.items() if count == top]
            if 0 in leaders:
                await self.bot.send_group_message(game.chat_id, t(game.language, "no_elimination"))
                await self._night(game_id)
                return
            tied = leaders
            if len(tied) != 1:
                await self.bot.send_group_message(game.chat_id, t(game.language, "no_elimination"))
                await self._night(game_id)
                return
            await self._eliminate_and_last_word(game_id, tied[0])

    async def _eliminate_and_last_word(self, game_id, telegram_id):
        await self.db.eliminate(game_id, telegram_id)
        game = await self.db.game(game_id)
        row = await self.db.player(game_id, telegram_id)
        if not game or not row:
            await self._night(game_id)
            return
        self.last_word_player[game_id] = telegram_id
        await self.db.set_phase(game_id, "LAST_WORD", game.last_word_timeout)
        # Enter the timed state before Telegram notifications so a delivery error
        # can never leave the game permanently stuck in LAST_WORD.
        await self.bot.prepare_last_word(game.chat_id, telegram_id)
        await self.schedule(game_id, self.finish_last_word, game.last_word_timeout)
        lang = await self.db.language(telegram_id, game.language)
        role_text = ""  # Roles remain hidden until the final game result by project design.
        try:
            await self.bot.send_group_message(game.chat_id, t(game.language, "eliminated", name=row[1].full_name, role=role_text))
        except Exception as exc:
            await self.db.log("ERROR", game_id, details=f"elimination announcement failed: {type(exc).__name__}: {exc}")
        try:
            await self.bot.send_message(telegram_id, t(lang, "last_word", seconds=game.last_word_timeout))
        except Exception as exc:
            await self.db.log("ERROR", game_id, telegram_id, f"last word delivery failed: {type(exc).__name__}: {exc}")

    async def finish_last_word(self, game_id):
        async with self.lock(game_id):
            game = await self.db.game(game_id)
            if not game or not game.active or game.phase != "LAST_WORD":
                return
            uid = self.last_word_player.pop(game_id, None)
            if uid:
                await self.db.set_player(game_id, uid, final_word_used=True)
                await self.bot.restrict_member(game.chat_id, uid)
            winner = await self.check_winner(game_id)
            if winner:
                await self._finish(game_id, winner)
            else:
                await self._night(game_id)

    async def check_winner(self, game_id):
        rows = await self.db.players(game_id)
        mafia = sum(1 for p, _ in rows if p.alive and p.role == "mafia")
        civilians = sum(1 for p, _ in rows if p.alive and p.role != "mafia")
        if mafia == 0:
            return "CIVILIANS"
        if mafia >= civilians:
            return "MAFIA"
        return None

    async def _cancel_locked(self, game_id, reason="cancelled"):
        game = await self.db.game(game_id)
        if not game or not game.active:
            return False
        await self.cancel_timer(game_id)
        await self.db.cancel(game_id)
        await self.db.log("GAME_CANCELLED", game_id, details=reason)
        try:
            await self.bot.finish_group(game_id, "CANCELLED")
        except Exception as exc:
            await self.db.log("ERROR", game_id, details=f"cancel notification failed: {type(exc).__name__}: {exc}")
        return True

    async def cancel(self, game_id, reason="cancelled"):
        async with self.lock(game_id):
            return await self._cancel_locked(game_id, reason)

    async def player_left(self, game_id, telegram_id):
        """Atomically process a player leaving during an active game."""
        async with self.lock(game_id):
            game = await self.db.game(game_id)
            row = await self.db.player(game_id, telegram_id)
            if not game or not game.active or not row:
                return
            # Before roles are assigned, leaving means leaving the lobby/ready queue,
            # not becoming a dead player. This prevents an impossible READY_CHECK.
            if game.phase == "READY_CHECK":
                if telegram_id == game.creator_id:
                    await self._cancel_locked(game_id, "creator left during ready check")
                    return
                await self.cancel_timer(game_id)
                await self.db.leave_game(game_id, telegram_id)
                await self.db.set_phase(game_id, "LOBBY", None)
                await self.db.log("GAME_LEAVE", game_id, telegram_id, "left during ready check")
                await self.bot.refresh_lobby(game_id)
                return
            if row[0].alive:
                await self.db.eliminate(game_id, telegram_id)
                await self.db.clear_actions_for_user(game_id, telegram_id)
                await self.db.clear_vote_for_user(game_id, telegram_id)
                await self.db.log("PLAYER_LEFT", game_id, telegram_id)
            winner = await self.check_winner(game_id)
            if winner:
                await self._finish(game_id, winner)

    async def finish(self, game_id, winner):
        async with self.lock(game_id):
            await self._finish(game_id, winner)

    async def _finish(self, game_id, winner):
        game = await self.db.game(game_id)
        if not game or not game.active:
            return
        await self.cancel_timer(game_id)
        await self.db.finish(game_id, winner)
        try:
            await self.bot.finish_group(game_id, winner)
        except Exception as exc:
            await self.db.log("ERROR", game_id, details=f"game finish notification failed: {type(exc).__name__}: {exc}")
