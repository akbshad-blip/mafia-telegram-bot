from __future__ import annotations

import asyncio, json, logging
from datetime import datetime, timezone
from html import escape
from pathlib import Path

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ChatPermissions, InputFile
from telegram.constants import ParseMode
from telegram.error import TelegramError, Forbidden
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, ContextTypes, filters
from telegram.helpers import create_deep_linked_url

from config import settings
from locales import t, LANGS
from database import Database
from game.engine import GameEngine
from game.roles import composition, validate_custom, ROLE_ORDER

log = logging.getLogger(__name__)


class UserBot:
    def __init__(self, db: Database):
        self.db = db
        self.app = Application.builder().token(settings.user_bot_token).concurrent_updates(True).build()
        self.api = self.app.bot
        self.engine = GameEngine(db, self)
        self.username: str | None = None
        self.lobby_messages: dict[int, int] = {}
        self.pending_support: dict[int, int] = {}
        self.pending_count: dict[int, int] = {}
        self.pending_join_code: set[int] = set()
        self.pending_mafia_chat: set[int] = set()
        self._mafia_chat_game: dict[int,int] = {}
        self._initialized = False
        self._install_handlers()

    def _install_handlers(self):
        self.app.add_handler(CommandHandler("start", self.start))
        self.app.add_handler(CommandHandler("menu", self.menu))
        # Public BotFather command contract. /newgame remains a backward-compatible alias.
        self.app.add_handler(CommandHandler("create", self.create_command))
        self.app.add_handler(CommandHandler("newgame", self.create_command))
        self.app.add_handler(CommandHandler("join", self.join_command))
        self.app.add_handler(CommandHandler("invite", self.invite_command))
        self.app.add_handler(CommandHandler("lobby", self.lobby_command))
        self.app.add_handler(CommandHandler("profile", self.profile_command))
        self.app.add_handler(CommandHandler("stats", self.stats_command))
        self.app.add_handler(CommandHandler("rules", self.rules_command))
        self.app.add_handler(CommandHandler("support", self.support_command))
        self.app.add_handler(CommandHandler("language", self.language_command))
        self.app.add_handler(CommandHandler("help", self.help_command))
        self.app.add_handler(CallbackQueryHandler(self.callbacks))
        self.app.add_handler(MessageHandler(filters.StatusUpdate.LEFT_CHAT_MEMBER, self.left_member))
        self.app.add_handler(MessageHandler(filters.ChatType.PRIVATE & ~filters.COMMAND & filters.ALL, self.private_messages))
        self.app.add_handler(MessageHandler(filters.ALL & filters.ChatType.GROUPS, self.group_messages))

    async def initialize(self):
        if self._initialized: return
        await self.app.initialize()
        me = await self.app.bot.get_me()
        self.username = me.username
        await self.app.bot.set_my_commands([
            ("start", "Запустить бота"), ("menu", "Открыть главное меню"),
            ("create", "Создать игру в группе"), ("join", "Войти в игру по коду"),
            ("invite", "Получить код и ссылку приглашения"), ("lobby", "Показать лобби группы"),
            ("profile", "Мой профиль"), ("stats", "Моя статистика"),
            ("rules", "Правила игры"), ("support", "Поддержка"),
            ("language", "Изменить язык"), ("help", "Помощь")
        ])
        log.info("User Bot initialized: @%s id=%s", me.username, me.id)
        self._initialized = True

    async def run(self):
        """Local long-polling runner. Production Render uses the shared webhook server."""
        await self.initialize()
        await self.app.start()
        await self.app.updater.start_polling(allowed_updates=Update.ALL_TYPES, drop_pending_updates=False)
        try:
            await asyncio.Event().wait()
        finally:
            await self.app.updater.stop()
            await self.app.stop()
            await self.app.shutdown()

    def language_keyboard(self):
        return InlineKeyboardMarkup([[InlineKeyboardButton(LANGS[k], callback_data=f"lang:{k}")] for k in LANGS])

    def rules_keyboard(self, lang):
        return InlineKeyboardMarkup([
            [InlineKeyboardButton(t(lang, "accept_rules"), callback_data="rules:accept")],
            [InlineKeyboardButton(t(lang, "language"), callback_data="menu:lang")]
        ])

    def main_keyboard(self, lang):
        return InlineKeyboardMarkup([
            [InlineKeyboardButton(t(lang,"create_game"), callback_data="menu:new"), InlineKeyboardButton(t(lang,"join_game"), callback_data="menu:join")],
            [InlineKeyboardButton(t(lang,"profile"), callback_data="menu:profile"), InlineKeyboardButton(t(lang,"stats"), callback_data="menu:stats")],
            [InlineKeyboardButton(t(lang,"rules_button"), callback_data="menu:rules"), InlineKeyboardButton(t(lang,"support"), callback_data="menu:support")],
            [InlineKeyboardButton(t(lang,"language"), callback_data="menu:lang"), InlineKeyboardButton(t(lang,"help"), callback_data="menu:help")],
        ])

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        u = update.effective_user
        existing = await self.db.user_stats(u.id)
        user = await self.db.get_or_create_user(u, settings.default_language, mark_started=True)
        if existing is None:
            await self.db.log("NEW_USER", actor_id=u.id, details=f"name={u.full_name};username=@{u.username or '—'}")
            try: await self.db.queue_admin_notification("NEW_USER", u.id, {"name":u.full_name,"username":u.username,"language":settings.default_language})
            except Exception: log.exception("Failed to queue new-user notification")
        lang = await self.db.language(u.id, settings.default_language)
        # Rules are the hard gate. Deep-links, commands and game actions are
        # deliberately processed only after the user accepts them.
        if not user.rules_accepted:
            await update.effective_message.reply_text(t(lang,"choose_language"), reply_markup=self.language_keyboard())
            return
        payload = context.args[0] if context.args else ""
        if payload.startswith("game_"):
            await self.join_deep_link(update, u, lang, payload); return
        await self.send_welcome(update.effective_message, u, lang)

    async def send_asset(self, chat_id: int, name: str, caption: str, reply_markup=None):
        """Send an optional Telegram sticker first, then the readable message.

        Sticker file_ids are optional because Telegram file_ids are instance-specific.
        If a sticker is not configured, the bot falls back cleanly to the emoji-rich
        message instead of breaking the flow.
        """
        sticker_map = {
            "welcome": settings.sticker_welcome, "rules": settings.sticker_rules,
            "roles": settings.sticker_role, "lobby": settings.sticker_lobby,
            "night": settings.sticker_night, "day": settings.sticker_day,
        }
        sticker_id = sticker_map.get(name, "")
        local = Path(__file__).resolve().parent.parent / "assets" / "stickers" / f"{name}.webp"
        try:
            if sticker_id:
                await self.api.send_sticker(chat_id, sticker_id)
            elif local.exists():
                with local.open("rb") as fh:
                    await self.api.send_sticker(chat_id, InputFile(fh, filename=local.name))
        except TelegramError:
            log.warning("Sticker %s could not be sent; continuing with text", name)
        return await self.api.send_message(chat_id, caption, parse_mode=ParseMode.HTML, reply_markup=reply_markup)

    async def send_welcome(self, message, user, lang):
        name = escape(user.full_name)
        text = t(lang, "welcome_full", name=name)
        await self.send_asset(message.chat_id, "welcome", text, self.main_keyboard(lang))

    async def menu(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        u=update.effective_user; await self.db.get_or_create_user(u, settings.default_language, mark_started=True); lang=await self.db.language(u.id,settings.default_language)
        user=await self.db.user_stats(u.id)
        if not user or not user.rules_accepted:
            await update.effective_message.reply_text(t(lang,"rules_required"), reply_markup=self.language_keyboard()); return
        await self.send_welcome(update.effective_message,u,lang)

    async def _command_ready(self, update: Update):
        u = update.effective_user
        user = await self.db.user_stats(u.id)
        lang = await self.db.language(u.id, settings.default_language)
        if not user or not user.rules_accepted:
            await update.effective_message.reply_text(t(lang, "rules_required"), reply_markup=self.language_keyboard())
            return None, lang
        return user, lang

    async def join_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user, lang = await self._command_ready(update)
        if not user: return
        self.pending_join_code.add(update.effective_user.id)
        await update.effective_message.reply_text(t(lang, "join_hint"), parse_mode=ParseMode.HTML)

    async def profile_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user, lang = await self._command_ready(update)
        if not user: return
        username = f"@{escape(user.username)}" if user.username else t(lang, "no_username")
        text = t(lang, "profile_card", name=escape(user.display_name), username=username, tg_id=user.telegram_id,
                  language=user.language, first=user.first_start_at.strftime('%Y-%m-%d %H:%M:%S UTC') if user.first_start_at else '—',
                  last=user.last_seen_at.strftime('%Y-%m-%d %H:%M:%S UTC') if user.last_seen_at else '—',
                  rules=user.rules_accepted_at.strftime('%Y-%m-%d %H:%M:%S UTC') if user.rules_accepted_at else '—',
                  games=user.games_played, wins=user.wins, losses=user.losses, blocked=t(lang,'yes') if user.blocked_bot else t(lang,'no'))
        await update.effective_message.reply_text(text, parse_mode=ParseMode.HTML, reply_markup=self.main_keyboard(lang))

    async def stats_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user, lang = await self._command_ready(update)
        if not user: return
        roles = await self.db.role_stats(user.telegram_id)
        role_lines = "\n".join(f"• {t(lang, 'role_'+r.role)} — {r.games}/{r.wins}/{r.losses}" for r in roles) or "—"
        text = t(lang, "stats_detailed", games=user.games_played, wins=user.wins, losses=user.losses, roles=role_lines)
        await update.effective_message.reply_text(text, parse_mode=ParseMode.HTML, reply_markup=self.main_keyboard(lang))

    async def rules_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        lang = await self.db.language(update.effective_user.id, settings.default_language)
        kb=self.rules_keyboard(lang)
        await self.send_asset(update.effective_message.chat_id,"roles",t(lang,"rules_full"),kb)

    async def support_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user, lang = await self._command_ready(update)
        if not user: return
        await update.effective_message.reply_text(t(lang, "support_menu"), parse_mode=ParseMode.HTML, reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton(t(lang, "new_ticket"), callback_data="support:new")],
            [InlineKeyboardButton(t(lang, "my_ticket"), callback_data="support:status")],
            [InlineKeyboardButton(t(lang, "faq"), callback_data="support:faq")],
            [InlineKeyboardButton(t(lang, "contact_admin"), url=settings.admin_contact_url or "https://t.me/")],
            [InlineKeyboardButton(t(lang, "back"), callback_data="menu:back")],
        ]))

    async def language_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        lang = await self.db.language(update.effective_user.id, settings.default_language)
        await update.effective_message.reply_text(t(lang, "choose_language"), reply_markup=self.language_keyboard())

    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user, lang = await self._command_ready(update)
        if not user: return
        await self.send_asset(update.effective_message.chat_id,"features",t(lang,"help_text"),self.main_keyboard(lang))

    async def create_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Create a lobby in the current Telegram group."""
        u = update.effective_user
        user, lang = await self._command_ready(update)
        if not user: return
        if update.effective_chat.type not in ("group", "supergroup"):
            await update.effective_message.reply_text(t(lang, "create_in_group_text"), parse_mode=ParseMode.HTML)
            return
        await self.create_lobby(update.effective_chat.id, u.id, update.effective_chat.title or "Mafia")

    async def new_game_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await self.create_command(update, context)

    async def join_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        u = update.effective_user
        user, lang = await self._command_ready(update)
        if not user: return
        if update.effective_chat.type != "private":
            await update.effective_message.reply_text(t(lang, "join_private_only"), parse_mode=ParseMode.HTML)
            return
        if context.args:
            await self.join_by_code(update, u, lang, context.args[0].strip().upper())
            return
        self.pending_join_code.add(u.id)
        await update.effective_message.reply_text(
            t(lang, "join_hint"), parse_mode=ParseMode.HTML,
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(t(lang, "back"), callback_data="menu:back")]])
        )

    async def join_by_code(self, update, u, lang, code):
        game = await self.db.game_by_code(code)
        if not game or not game.active or game.phase != "LOBBY":
            await self.send_message(u.id, t(lang, "room_code_invalid"))
            return
        if not await self.member_is_player_eligible(game.chat_id, u.id):
            await self.send_message(u.id, t(lang, "must_be_group_member"))
            return
        try:
            member = await self.api.get_chat_member(game.chat_id, u.id)
            if member.status in {"left", "kicked"}:
                raise TelegramError("not member")
        except TelegramError:
            await self.send_message(u.id, t(lang, "must_be_group_member"))
            return
        user = await self.db.user_stats(u.id)
        if not user or not user.started_bot or not user.rules_accepted:
            await self.send_message(u.id, t(lang, "open_private"))
            return
        ok, reason = await self.db.join_game(game.id, u.id, u)
        if ok:
            await self.db.log("GAME_JOIN", game.id, u.id)
            await self.send_message(u.id, t(lang, "joined"))
            await self.refresh_lobby(game.id)
        elif reason == "exists":
            await self.send_message(u.id, t(lang, "already_joined"))
        elif reason == "full":
            await self.send_message(u.id, t(lang, "too_many", max=game.player_limit))

    async def invite_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        u = update.effective_user
        user, lang = await self._command_ready(update)
        if not user: return
        if update.effective_chat.type not in ("group", "supergroup"):
            await update.effective_message.reply_text(t(lang, "invite_group_only"), parse_mode=ParseMode.HTML)
            return
        game = await self.db.active_game(update.effective_chat.id)
        if not game or game.phase != "LOBBY":
            await update.effective_message.reply_text(t(lang, "no_active_lobby"), parse_mode=ParseMode.HTML)
            return
        if u.id != game.creator_id:
            await update.effective_message.reply_text(t(lang, "creator_only"), parse_mode=ParseMode.HTML)
            return
        url = create_deep_linked_url(self.username or "", f"game_{game.id}")
        await self.send_message(u.id, t(lang, "invite_text", url=url, code=game.room_code))
        await update.effective_message.reply_text(t(lang, "invite_sent"), parse_mode=ParseMode.HTML)

    async def lobby_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        u = update.effective_user
        user, lang = await self._command_ready(update)
        if not user: return
        if update.effective_chat.type not in ("group", "supergroup"):
            await update.effective_message.reply_text(t(lang, "lobby_group_only"), parse_mode=ParseMode.HTML)
            return
        game = await self.db.active_game(update.effective_chat.id)
        if not game or game.phase != "LOBBY":
            await update.effective_message.reply_text(t(lang, "no_active_lobby"), parse_mode=ParseMode.HTML)
            return
        await self.refresh_lobby(game.id)

    async def join_deep_link(self, update, u, lang, payload):
        try: game_id=int(payload.split("_",1)[1])
        except ValueError: await self.send_message(u.id,t(lang,"invalid_action")); return
        game=await self.db.game(game_id)
        user=await self.db.user_stats(u.id)
        if not user or not user.rules_accepted:
            await self.send_message(u.id, t(lang,"rules_required"), reply_markup=self.rules_keyboard(lang)); return
        if not game or not game.active or game.phase!="LOBBY": await self.send_message(u.id,t(lang,"invalid_action")); return
        if not await self.member_is_player_eligible(game.chat_id,u.id): await self.send_message(u.id,t(lang,"admin_group_error")); return
        try:
            member=await self.api.get_chat_member(game.chat_id,u.id)
            if member.status in {"left","kicked"}: raise TelegramError("not member")
        except TelegramError:
            await self.send_message(u.id,t(lang,"must_be_group_member")); return
        ok,reason=await self.db.join_game(game_id,u.id,u)
        if ok:
            await self.db.log("GAME_JOIN",game_id,u.id); await self.send_message(u.id,t(lang,"joined")); await self.refresh_lobby(game_id)
        elif reason=="exists": await self.send_message(u.id,t(lang,"already_joined"))
        elif reason=="full": await self.send_message(u.id,t(lang,"too_many",max=game.player_limit))

    async def callbacks(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        q=update.callback_query; u=q.from_user
        await self.db.get_or_create_user(u,settings.default_language,mark_started=(q.message and q.message.chat.type=="private"))
        lang=await self.db.language(u.id,settings.default_language); data=q.data or ""
        if data.startswith("lang:"):
            new = data.split(":", 1)[1]
            if new not in LANGS:
                await q.answer("Invalid language", show_alert=True)
                return
            await q.answer()
            try:
                await self.db.set_language(u.id, new)
                user = await self.db.user_stats(u.id)
                if not user or not user.rules_accepted:
                    await self.show_rules(q, new)
                else:
                    # Render the complete main menu immediately so the language change is obvious.
                    await q.edit_message_text(
                        t(new, "welcome_full", name=escape(u.full_name)),
                        parse_mode=ParseMode.HTML,
                        reply_markup=self.main_keyboard(new),
                    )
            except Exception:
                log.exception("Failed to change language for user_id=%s", u.id)
                try:
                    await q.message.reply_text(t(lang, "language_change_error"))
                except TelegramError:
                    pass
            return
        if data == "menu:lang":
            await q.answer()
            await q.edit_message_text(t(lang,"choose_language"), reply_markup=self.language_keyboard())
            return
        if data.startswith("rules:"):
            action=data.split(":",1)[1]
            if action=="accept":
                await self.db.accept_rules(u.id); await self.db.log("RULES_ACCEPTED",actor_id=u.id); lang=await self.db.language(u.id,settings.default_language)
                await q.answer("✅"); await q.edit_message_text(t(lang,"rules_accepted"),parse_mode=ParseMode.HTML,reply_markup=self.main_keyboard(lang))
            elif action=="show": await q.answer(); await self.show_rules(q,lang)
            return
        user_state=await self.db.user_stats(u.id)
        if not user_state or not user_state.rules_accepted:
            await q.answer(t(lang,"rules_required"), show_alert=True)
            await self.send_message(u.id, t(lang,"rules_required"), reply_markup=self.rules_keyboard(lang))
            return
        if data.startswith("menu:"):
            await self.menu_callback(q,u,lang,data); return
        if data.startswith("count:"):
            await self.count_callback(q,u,data); return
        if data.startswith("countcustom:"):
            gid=int(data.split(":",1)[1]); game=await self.db.game(gid)
            if not game or u.id!=game.creator_id: await q.answer("⛔",show_alert=True); return
            self.pending_count[u.id]=gid; await q.answer(); await q.edit_message_text(t(lang,"custom_count_prompt"),parse_mode=ParseMode.HTML); return
        if data.startswith("create:"):
            await self.create_callback(q,u,lang,data); return
        if data.startswith("support:"):
            await self.support_callback(q,u,lang,data); return
        if data.startswith("ticket:"):
            await self.ticket_callback(q,u,lang,data); return
        if data.startswith("lobby:"): await self.lobby_callback(q,u,data); return
        if data.startswith("settings:"): await self.settings_callback(q,u,data); return
        if data.startswith("roles:"): await self.role_settings_callback(q,u,data); return
        if data.startswith("ready:"): await self.ready_callback(q,u,data); return
        if data.startswith("act:"): await self.action_callback(q,u,data); return
        if data.startswith("mafia:"): await self.mafia_callback(q,u,data); return
        if data.startswith("vote:"): await self.vote_callback(q,u,data); return
        if data.startswith("extra_request:"): await self.extra_request_callback(q,u,data); return
        if data.startswith("extra_vote:"): await self.extra_vote_callback(q,u,data); return

    async def show_rules(self,q,lang):
        text=t(lang,"rules_full")
        kb=self.rules_keyboard(lang)
        try:
            await q.edit_message_text(text,parse_mode=ParseMode.HTML,reply_markup=kb)
        except TelegramError: await q.message.reply_text(text,parse_mode=ParseMode.HTML,reply_markup=kb)

    async def menu_callback(self,q,u,lang,data):
        action=data.split(":",1)[1]; await q.answer()
        if action=="lang": await q.edit_message_text(t(lang,"choose_language"),reply_markup=self.language_keyboard())
        elif action=="rules": await self.show_rules(q,lang)
        elif action=="stats": await self.show_stats(q,u.id,lang)
        elif action=="profile": await self.show_profile(q,u.id,lang)
        elif action=="help": await q.edit_message_text(t(lang,"help_text"),parse_mode=ParseMode.HTML,reply_markup=self.main_keyboard(lang))
        elif action=="support": await self.show_support(q,lang)
        elif action=="new":
            kb=InlineKeyboardMarkup([[InlineKeyboardButton(t(lang,"how_add_bot"),callback_data="create:guide")],[InlineKeyboardButton(t(lang,"create_in_group"),callback_data="create:group")],[InlineKeyboardButton(t(lang,"how_create"),callback_data="create:how")],[InlineKeyboardButton(t(lang,"back"),callback_data="menu:back")]])
            await self.send_asset(q.message.chat_id,"menu",t(lang,"create_menu"),kb)
        elif action=="join":
            self.pending_join_code.add(u.id)
            await q.edit_message_text(t(lang,"join_hint"),parse_mode=ParseMode.HTML,reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(t(lang,"join_how"),callback_data="menu:join_help")],[InlineKeyboardButton(t(lang,"back"),callback_data="menu:back")]]))
        elif action=="join_help":
            await q.edit_message_text(t(lang,"join_help_text"),parse_mode=ParseMode.HTML,reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(t(lang,"back"),callback_data="menu:join")]]))
        elif action=="back": await q.edit_message_text(t(lang,"main_menu"),reply_markup=self.main_keyboard(lang))

    async def show_stats(self,q,uid,lang):
        s=await self.db.user_stats(uid); roles=await self.db.role_stats(uid)
        role_lines="\n".join(f"• {t(lang,'role_'+r.role)} — {r.games}/{r.wins}/{r.losses}" for r in roles) or "—"
        text=t(lang,"stats_detailed",games=s.games_played,wins=s.wins,losses=s.losses,roles=role_lines)
        await self.send_asset(q.message.chat_id,"features",text,self.main_keyboard(lang))

    async def show_profile(self,q,uid,lang):
        s=await self.db.user_stats(uid); username=f"@{escape(s.username)}" if s.username else t(lang,"no_username")
        text=t(lang,"profile_card",name=escape(s.display_name),username=username,tg_id=s.telegram_id,language=s.language,first=s.first_start_at.strftime('%Y-%m-%d %H:%M:%S UTC') if s.first_start_at else '—',last=s.last_seen_at.strftime('%Y-%m-%d %H:%M:%S UTC'),rules=s.rules_accepted_at.strftime('%Y-%m-%d %H:%M:%S UTC') if s.rules_accepted_at else '—',games=s.games_played,wins=s.wins,losses=s.losses,blocked=t(lang,'yes') if s.blocked_bot else t(lang,'no'))
        await self.send_asset(q.message.chat_id,"menu",text,self.main_keyboard(lang))

    async def create_callback(self,q,u,lang,data):
        action=data.split(":",1)[1]; await q.answer()
        if action=="guide": await self.send_bot_guide(q.message.chat_id,lang); return
        if action=="how": await q.edit_message_text(t(lang,"create_how"),parse_mode=ParseMode.HTML,reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(t(lang,"back"),callback_data="menu:new")]])); return
        if action=="group": await q.edit_message_text(t(lang,"create_in_group_text"),parse_mode=ParseMode.HTML,reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(t(lang,"how_create"),callback_data="create:how")],[InlineKeyboardButton(t(lang,"back"),callback_data="menu:new")]])); return

    async def send_bot_guide(self,chat_id,lang):
        await self.send_message(chat_id,t(lang,"bot_guide"))

    async def create_lobby(self,chat_id,creator_id,title):
        lang=await self.db.language(creator_id,settings.default_language); creator=await self.db.user_stats(creator_id)
        if not creator or not creator.started_bot or not creator.rules_accepted:
            url=create_deep_linked_url(self.username or "","create_game"); await self.send_group_message(chat_id,f"🔐 {t(lang,'creator_start_required')}\n\n{url}"); return
        if await self.db.active_game(chat_id): await self.send_group_message(chat_id,t(lang,"active_game")); return
        ok,missing=await self.check_group_ready(chat_id,creator_id)
        if not ok:
            await self.send_group_message(chat_id,t(lang,"admin_permissions_missing",missing=', '.join(missing))); return
        game=await self.db.create_game(chat_id,creator_id,title or "Mafia",lang,10,composition(10)); member=await self.api.get_chat_member(chat_id,creator_id)
        await self.db.join_game(game.id,creator_id,member.user); await self.db.log("GAME_CREATED",game.id,creator_id)
        await self.send_asset(chat_id,"lobby",t(lang,"lobby_created"),self.lobby_keyboard(game))
        await self.send_group_rules(chat_id,lang); await self.refresh_lobby(game.id)

    async def check_group_ready(self,chat_id,creator_id):
        try:
            me=await self.api.get_me(); member=await self.api.get_chat_member(chat_id,me.id)
            if member.status not in {"administrator","creator"}: return False,["administrator"]
            required=[]
            for attr,label in (("can_delete_messages","delete messages"),("can_restrict_members","restrict members")):
                if member.status=="administrator" and not getattr(member,attr,False):required.append(label)
            return not required,required
        except TelegramError:return False,["administrator access"]

    async def send_group_rules(self,chat_id,lang): await self.send_group_message(chat_id,t(lang,"rules_group"))

    def lobby_keyboard(self,game):
        l=game.language; return InlineKeyboardMarkup([
            [InlineKeyboardButton(t(l,"join"),callback_data=f"lobby:join:{game.id}"),InlineKeyboardButton(t(l,"leave"),callback_data=f"lobby:leave:{game.id}"),InlineKeyboardButton(t(l,"invite"),callback_data=f"lobby:invite:{game.id}")],
            [InlineKeyboardButton(t(l,"player_count"),callback_data=f"lobby:count:{game.id}"),InlineKeyboardButton(t(l,"roles"),callback_data=f"lobby:roles:{game.id}")],
            [InlineKeyboardButton(t(l,"settings"),callback_data=f"lobby:settings:{game.id}"),InlineKeyboardButton(t(l,"rules"),callback_data=f"lobby:rules:{game.id}")],
            [InlineKeyboardButton(t(l,"how_it_works"),callback_data=f"lobby:help:{game.id}")],
            [InlineKeyboardButton(t(l,"start"),callback_data=f"lobby:start:{game.id}")]
        ])

    async def refresh_lobby(self,game_id):
        game=await self.db.game(game_id)
        if not game or not game.active:return
        rows=await self.db.players(game_id); names="\n".join(f"{i+1}. {escape(u.full_name)}" for i,(_,u) in enumerate(rows)) or "—"
        cfg=json.loads(game.role_config or "{}")
        role_icons={"mafia":"🔴","doctor":"🩺","commissioner":"🔎","lover":"💗","detective":"🕵️","bodyguard":"🛡","civilian":"⚪"}
        roleline="  ".join(f"{role_icons[r]} {cfg.get(r,0)}" for r in ROLE_ORDER if cfg.get(r,0))
        text=t(game.language,"lobby_v2",count=len(rows),max=game.player_limit,players=names,roles=roleline,game_id=game.id,code=game.room_code)
        old=self.lobby_messages.get(game_id)
        if old:
            try:await self.api.delete_message(game.chat_id,old)
            except TelegramError:pass
        m=await self.send_group_message(game.chat_id,text,reply_markup=self.lobby_keyboard(game));self.lobby_messages[game_id]=m.message_id

    async def lobby_callback(self,q,u,data):
        _,action,gid=data.split(":",2); game=await self.db.game(int(gid)); lang=await self.db.language(u.id,settings.default_language)
        if not game or not game.active or game.phase!="LOBBY" or not q.message or q.message.chat_id!=game.chat_id:await q.answer(t(lang,"invalid_action"),show_alert=True);return
        if action=="back":
            await q.answer(); await self.refresh_lobby(game.id); return
        if action=="help":
            await q.answer(); await self.send_message(u.id, t(lang,"lobby_help", code=game.room_code), reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(t(lang,"back"), callback_data=f"lobby:back:{game.id}")]])); return
        if action=="join":
            if not await self.member_is_player_eligible(game.chat_id,u.id):await q.answer(t(lang,"admin_group_error"),show_alert=True);return
            user=await self.db.user_stats(u.id)
            if not user or not user.started_bot or not user.rules_accepted:
                url=create_deep_linked_url(self.username or "",f"game_{game.id}");await q.answer(t(lang,"open_private"),show_alert=True);await self.send_group_message(game.chat_id,f"🔐 {escape(u.full_name)} — {url}");return
            ok,reason=await self.db.join_game(game.id,u.id,u)
            if not ok:await q.answer(t(lang,"already_joined") if reason=="exists" else t(lang,"too_many",max=game.player_limit),show_alert=True);return
            await self.db.log("GAME_JOIN",game.id,u.id);await q.answer("✅");await self.send_message(u.id,t(lang,"joined"));await self.refresh_lobby(game.id)
            game=await self.db.game(game.id)
            rows=await self.db.players(game.id)
            if game and game.auto_start and len(rows)>=game.player_limit and u.id==game.creator_id:
                ok,reason=await self.engine.start(game.id)
                if not ok:
                    await self.send_message(u.id,t(lang,{"not_enough":"not_enough","too_many":"too_many","private_not_started":"open_private","private_delivery_failed":"private_delivery_failed"}.get(reason,"invalid_action"),min=settings.min_players,max=game.player_limit))
        elif action=="leave":
            if u.id==game.creator_id:await q.answer(t(lang,"creator_only"),show_alert=True);return
            if await self.db.player(game.id,u.id):await self.db.leave_game(game.id,u.id);await self.db.log("GAME_LEAVE",game.id,u.id);await q.answer("🚪");await self.refresh_lobby(game.id)
        elif action=="invite":
            await q.answer();url=create_deep_linked_url(self.username or "",f"game_{game.id}");await self.send_message(u.id,t(lang,"invite_text",url=url,code=game.room_code))
        elif action=="count": await q.answer();await self.show_player_count(q,game)
        elif action=="roles": await q.answer();await self.show_role_config(q,game)
        elif action=="settings":
            if u.id!=game.creator_id:await q.answer(t(lang,"creator_only"),show_alert=True);return
            await q.answer();await self.show_settings(q,game)
        elif action=="rules":await q.answer();await q.message.reply_text(t(lang,"rules_full"))
        elif action=="start":
            if u.id!=game.creator_id:await q.answer(t(lang,"creator_only"),show_alert=True);return
            ok,reason=await self.engine.start(game.id);await q.answer("▶️" if ok else t(lang,{"not_enough":"not_enough","too_many":"too_many","private_not_started":"open_private","private_delivery_failed":"private_delivery_failed","role_config_invalid":"role_invalid"}.get(reason,"invalid_action"),min=settings.min_players,max=game.player_limit),show_alert=not ok)

    async def count_callback(self,q,u,data):
        _,gid_s,count_s=data.split(":",2);gid=int(gid_s);count=int(count_s);game=await self.db.game(gid)
        if not game or u.id!=game.creator_id or game.phase!="LOBBY" or not 5<=count<=40:await q.answer(t(await self.db.language(u.id),"invalid_action"),show_alert=True);return
        cfg=composition(count);await self.db.set_game_fields(gid,player_limit=count,role_config=json.dumps(cfg));await q.answer("✅");await self.refresh_lobby(gid)

    async def show_player_count(self,q,game):
        vals=[5,6,7,8,9,10,11,12,15,20,25,30,35,40];rows=[]
        for i in range(0,len(vals),5):rows.append([InlineKeyboardButton(str(v),callback_data=f"count:{game.id}:{v}") for v in vals[i:i+5]])
        rows.append([InlineKeyboardButton(t(game.language,"custom_count"),callback_data=f"countcustom:{game.id}"),InlineKeyboardButton(t(game.language,"how_it_works"),callback_data=f"lobby:help:{game.id}")])
        rows.append([InlineKeyboardButton(t(game.language,"back"),callback_data=f"lobby:back:{game.id}")])
        await q.edit_message_text(t(game.language,"choose_player_count"),reply_markup=InlineKeyboardMarkup(rows))

    async def show_role_config(self,q,game):
        cfg=json.loads(game.role_config or "{}")
        # Backward compatibility with old four-role games.
        for role in ROLE_ORDER: cfg.setdefault(role, 0)
        l=game.language
        lines=[
            f"🔴 {t(l,'role_mafia')}: <b>{cfg['mafia']}</b> 🔒",
            f"🩺 {t(l,'role_doctor')}: <b>{cfg['doctor']}</b> 🔒",
            f"🔎 {t(l,'role_commissioner')}: <b>{cfg['commissioner']}</b>",
            f"💗 {t(l,'role_lover')}: <b>{cfg['lover']}</b>",
            f"🕵️ {t(l,'role_detective')}: <b>{cfg['detective']}</b>",
            f"🛡 {t(l,'role_bodyguard')}: <b>{cfg['bodyguard']}</b>",
            f"⚪ {t(l,'role_civilian')}: <b>{cfg['civilian']}</b>",
        ]
        kb=[
            [InlineKeyboardButton("➖ 🔴",callback_data=f"roles:minus:mafia:{game.id}"),InlineKeyboardButton("🔴 +",callback_data=f"roles:plus:mafia:{game.id}"),InlineKeyboardButton(t(l,'role_info'),callback_data=f"roles:info:mafia:{game.id}")],
            [InlineKeyboardButton("➖ 🔎",callback_data=f"roles:minus:commissioner:{game.id}"),InlineKeyboardButton("🔎 +",callback_data=f"roles:plus:commissioner:{game.id}"),InlineKeyboardButton(t(l,'role_info'),callback_data=f"roles:info:commissioner:{game.id}")],
            [InlineKeyboardButton("➖ 💗",callback_data=f"roles:minus:lover:{game.id}"),InlineKeyboardButton("💗 +",callback_data=f"roles:plus:lover:{game.id}"),InlineKeyboardButton(t(l,'role_info'),callback_data=f"roles:info:lover:{game.id}")],
            [InlineKeyboardButton("➖ 🕵️",callback_data=f"roles:minus:detective:{game.id}"),InlineKeyboardButton("🕵️ +",callback_data=f"roles:plus:detective:{game.id}"),InlineKeyboardButton(t(l,'role_info'),callback_data=f"roles:info:detective:{game.id}")],
            [InlineKeyboardButton("➖ 🛡",callback_data=f"roles:minus:bodyguard:{game.id}"),InlineKeyboardButton("🛡 +",callback_data=f"roles:plus:bodyguard:{game.id}"),InlineKeyboardButton(t(l,'role_info'),callback_data=f"roles:info:bodyguard:{game.id}")],
            [InlineKeyboardButton(t(l,'auto_balance'),callback_data=f"roles:auto:{game.id}")],
            [InlineKeyboardButton(t(l,'back'),callback_data=f"lobby:back:{game.id}")],
        ]
        text=t(l,"role_config_text",roles="\n".join(lines),total=game.player_limit)
        await q.edit_message_text(text,parse_mode=ParseMode.HTML,reply_markup=InlineKeyboardMarkup(kb))


    async def settings_callback(self,q,u,data):
        _,action,gid=data.split(":",2);game=await self.db.game(int(gid));
        if not game or u.id!=game.creator_id or game.phase!="LOBBY":await q.answer("⛔",show_alert=True);return
        mapping={"auto":"auto_start","ready":"ready_required","skip":"allow_skip_vote","repeat":"doctor_repeat_target","commissioner":"commissioner_eliminate","revote":"tie_revote","extra":"extra_time_enabled"}
        if action=="back":await q.answer();await self.refresh_lobby(game.id);return
        if action=="help": await q.answer(); await self.send_message(u.id,t(await self.db.language(u.id,game.language),"settings_help"),reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(t(game.language,"back"),callback_data=f"lobby:settings:{game.id}")]])); return
        if action in mapping:await self.db.set_game_setting(game.id,mapping[action],not getattr(game,mapping[action]));await q.answer("✅");game=await self.db.game(game.id);await self.show_settings(q,game);return
        if action=="self":await self.db.set_game_setting(game.id,"doctor_self_heal",not game.doctor_self_heal);await q.answer("✅");game=await self.db.game(game.id);await self.show_settings(q,game)

    async def show_settings(self,q,game):
        l=game.language; yes=t(l,"on");no=t(l,"off")
        val=lambda x:yes if x else no
        rows=[[InlineKeyboardButton(f"⚡ {t(l,'setting_auto')}: {val(game.auto_start)}",callback_data=f"settings:auto:{game.id}"),InlineKeyboardButton(f"🟢 {t(l,'setting_ready')}: {val(game.ready_required)}",callback_data=f"settings:ready:{game.id}")],[InlineKeyboardButton(f"⏭ {t(l,'setting_skip')}: {val(game.allow_skip_vote)}",callback_data=f"settings:skip:{game.id}"),InlineKeyboardButton(f"🩺 {t(l,'setting_self')}: {val(game.doctor_self_heal)}",callback_data=f"settings:self:{game.id}")],[InlineKeyboardButton(f"🩺 {t(l,'setting_repeat')}: {val(game.doctor_repeat_target)}",callback_data=f"settings:repeat:{game.id}"),InlineKeyboardButton(f"🔎 {t(l,'setting_commissioner')}: {val(game.commissioner_eliminate)}",callback_data=f"settings:commissioner:{game.id}")],[InlineKeyboardButton(f"⚖️ {t(l,'setting_revote')}: {val(game.tie_revote)}",callback_data=f"settings:revote:{game.id}"),InlineKeyboardButton(f"⏱ {t(l,'setting_extra')}: {val(game.extra_time_enabled)}",callback_data=f"settings:extra:{game.id}")],[InlineKeyboardButton(t(l,"how_it_works"),callback_data=f"settings:help:{game.id}")],[InlineKeyboardButton(t(l,"back"),callback_data=f"settings:back:{game.id}")]]
        await q.edit_message_text(t(l,"settings_title"),parse_mode=ParseMode.HTML,reply_markup=InlineKeyboardMarkup(rows))

    async def role_settings_callback(self,q,u,data):
        parts=data.split(":")
        if len(parts)==3: _,action,gid=parts; role=None
        else: _,action,role,gid=parts
        game=await self.db.game(int(gid)); lang=await self.db.language(u.id,settings.default_language)
        if not game or game.phase!="LOBBY" or u.id!=game.creator_id: await q.answer(t(lang,"creator_only"),show_alert=True); return
        cfg=json.loads(game.role_config or "{}")
        for r in ROLE_ORDER: cfg.setdefault(r,0)
        if action=="auto":
            cfg=composition(game.player_limit); await self.db.set_game_fields(game.id,role_config=json.dumps(cfg)); await q.answer("✅"); await self.show_role_config(q,await self.db.game(game.id)); return
        if action=="info" and role:
            await q.answer(); await self.send_message(u.id,t(lang,f"{role}_guide"),reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(t(lang,"back"),callback_data=f"lobby:roles:{game.id}")]])); return
        if action in {"plus","minus"} and role in {"mafia","commissioner","lover","detective","bodyguard"}:
            current=int(cfg.get(role,0)); delta=1 if action=="plus" else -1
            if role=="mafia":
                new=max(1,min(9,current+delta))
            else:
                new=max(0,min(1,current+delta))
            cfg[role]=new
            used=sum(int(cfg.get(r,0)) for r in ROLE_ORDER if r!="civilian")
            civilians=game.player_limit-used
            if civilians<1:
                cfg[role]=current
                await q.answer(t(lang,"role_no_room"),show_alert=True); return
            cfg["doctor"]=1; cfg["civilian"]=civilians
            try:
                validate_custom(game.player_limit,cfg["mafia"],1,cfg["commissioner"],cfg["lover"],cfg["detective"],cfg["bodyguard"])
            except ValueError:
                cfg[role]=current; cfg["civilian"]=game.player_limit-sum(int(cfg.get(r,0)) for r in ROLE_ORDER if r!="civilian")
                await q.answer(t(lang,"role_invalid"),show_alert=True); return
            await self.db.set_game_fields(game.id,role_config=json.dumps(cfg)); await q.answer("✅"); await self.show_role_config(q,await self.db.game(game.id))


    async def ready_callback(self,q,u,data):
        _,gid,val=data.split(":",2);game=await self.db.game(int(gid));lang=await self.db.language(u.id,settings.default_language)
        if not game or game.phase!="READY_CHECK" or not await self.db.player(game.id,u.id):await q.answer(t(lang,"invalid_action"),show_alert=True);return
        await self.db.set_ready(game.id,u.id,val=="1");await q.answer(t(lang,"ready_saved"))
        rows=await self.db.players(game.id)
        if rows and all(p.ready for p,_ in rows):await self.engine.ready_check(game.id)

    async def action_callback(self,q,u,data):
        try:_,gid,night,kind,target=data.split(":",4);gid=int(gid);night=int(night);target=int(target)
        except ValueError:await q.answer("⛔",show_alert=True);return
        game=await self.db.game(gid);lang=await self.db.language(u.id,settings.default_language)
        if not game or game.phase!="NIGHT" or game.night_number!=night:await q.answer(t(lang,"invalid_action"),show_alert=True);return
        row=await self.db.player(gid,u.id);tr=await self.db.player(gid,target)
        if not row or not row[0].alive or not tr or not tr[0].alive:await q.answer(t(lang,"not_alive"),show_alert=True);return
        role=row[0].role
        timeout={"mafia":game.mafia_timeout,"doctor":game.doctor_timeout,"commissioner":game.commissioner_timeout}.get(role,60)
        if game.phase_started_at and (datetime.now(timezone.utc)-game.phase_started_at).total_seconds()>timeout:await q.answer(t(lang,"action_expired"),show_alert=True);return
        allowed={"mafia":{"mafia"},"doctor":{"doctor"},"commissioner":{"check","eliminate"},"lover":{"block"},"detective":{"detect"},"bodyguard":{"guard"}}.get(role,set())
        if kind not in allowed or target==u.id and role in {"commissioner","lover","detective"}:await q.answer(t(lang,"invalid_action"),show_alert=True);return
        if role=="mafia" and tr[0].role=="mafia":await q.answer(t(lang,"invalid_action"),show_alert=True);return
        if role=="commissioner" and kind=="eliminate" and game.night_number<2:await q.answer(t(lang,"invalid_action"),show_alert=True);return
        if role=="doctor":
            if target==u.id and (not game.doctor_self_heal or row[0].doctor_self_heal_count>=game.doctor_self_heal_uses):await q.answer(t(lang,"invalid_action"),show_alert=True);return
            if not game.doctor_repeat_target and row[0].last_doctor_target==target:await q.answer(t(lang,"invalid_action"),show_alert=True);return
        await self.db.record_action(gid,u.id,kind,target)
        if role=="doctor":await self.db.set_player(gid,u.id,last_doctor_target=target,doctor_self_heal_used=row[0].doctor_self_heal_used or target==u.id,doctor_self_heal_count=row[0].doctor_self_heal_count+(1 if target==u.id else 0))
        if role=="commissioner" and kind=="check":
            result=t(lang,"check_mafia") if tr[0].role=="mafia" else t(lang,"check_not_mafia")
            await self.send_message(u.id,t(lang,"commissioner_result",name=escape(tr[1].display_name),result=result))
        if role=="mafia":await self.notify_mafia_choice(gid,u.id,target)
        await q.answer("✅")
        await self.engine.maybe_resolve_night(gid)

    async def notify_mafia_choice(self,game_id,actor_id,target_id):
        game=await self.db.game(game_id);rows=await self.db.players(game_id);target=next((u for p,u in rows if u.telegram_id==target_id),None)
        if not game or not target:return
        for p,u in rows:
            if p.alive and p.role=="mafia" and u.telegram_id!=actor_id:
                lang=await self.db.language(u.telegram_id,game.language)
                try:await self.send_message(u.telegram_id,t(lang,"mafia_partner_choice",name=escape(target.display_name)),reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(t(lang,"choose_same"),callback_data=f"act:{game.id}:{game.night_number}:mafia:{target_id}")],[InlineKeyboardButton(t(lang,"mafia_chat"),callback_data=f"mafia:chat:{game.id}")]]))
                except Exception:pass

    async def notify_mafia_consensus(self,game_id,target_id):
        if not target_id:return
        game=await self.db.game(game_id);rows=await self.db.players(game_id);target=next((u for p,u in rows if u.telegram_id==target_id),None)
        if not target:return
        for p,u in rows:
            if p.alive and p.role=="mafia":
                try:await self.send_message(u.telegram_id,t(game.language,"mafia_consensus",name=escape(target.display_name)))
                except Exception:pass

    async def mafia_callback(self,q,u,data):
        parts=data.split(":")
        if len(parts)!=3 or parts[1]!="chat": await q.answer("⛔",show_alert=True); return
        gid=int(parts[2]);game=await self.db.game(gid);row=await self.db.player(gid,u.id)
        if not game or game.phase!="NIGHT" or not row or not row[0].alive or row[0].role!="mafia": await q.answer("⛔",show_alert=True); return
        self.pending_mafia_chat.add(u.id);self._mafia_chat_game[u.id]=gid;await q.answer();await self.send_message(u.id,t(await self.db.language(u.id,game.language),"mafia_chat_prompt"))

    async def vote_callback(self,q,u,data):
        try:_,gid,round_s,target_s=data.split(":",3);gid=int(gid);rnd=int(round_s);target=int(target_s)
        except ValueError:await q.answer("⛔",show_alert=True);return
        game=await self.db.game(gid);lang=await self.db.language(u.id,settings.default_language);expected="VOTING_REVOTE" if rnd==2 else "VOTING"
        row=await self.db.player(gid,u.id)
        if not game or game.phase!=expected or game.voting_round!=rnd or not row or not row[0].alive:await q.answer(t(lang,"invalid_action"),show_alert=True);return
        if target==u.id:await q.answer(t(lang,"invalid_action"),show_alert=True);return
        if target==0 and not game.allow_skip_vote:await q.answer(t(lang,"invalid_action"),show_alert=True);return
        if target:
            tr=await self.db.player(gid,target)
            if not tr or not tr[0].alive:await q.answer(t(lang,"invalid_action"),show_alert=True);return
            if rnd==2 and target not in set(json.loads(game.revote_candidates or "[]")):await q.answer(t(lang,"invalid_action"),show_alert=True);return
        await self.db.set_vote(gid,u.id,target or None);await q.answer(t(lang,"vote_saved"))

    async def extra_request_callback(self,q,u,data):
        gid=int(data.split(":",1)[1]);game=await self.db.game(gid);row=await self.db.player(gid,u.id) if game else None
        if not game or game.phase!="DISCUSSION" or not row or not row[0].alive:await q.answer("⛔",show_alert=True);return
        ok=await self.engine.request_extra_time(gid);await q.answer("⏱" if ok else "⛔",show_alert=not ok)
    async def extra_vote_callback(self,q,u,data):
        _,val,gid=data.split(":",2);gid=int(gid);game=await self.db.game(gid);row=await self.db.player(gid,u.id) if game else None
        if not game or game.phase!="EXTRA_TIME" or not row or not row[0].alive:await q.answer("⛔",show_alert=True);return
        await self.db.add_extra_vote(gid,u.id,val=="1");await q.answer("✅")
        if sum(await self.db.extra_counts(gid))>=len(await self.db.alive_ids(gid)):await self.engine.resolve_extra_time(gid)

    async def show_support(self,q,lang):
        kb=InlineKeyboardMarkup([[InlineKeyboardButton(t(lang,"new_ticket"),callback_data="support:new")],[InlineKeyboardButton(t(lang,"my_ticket"),callback_data="support:status")],[InlineKeyboardButton(t(lang,"faq"),callback_data="support:faq")],[InlineKeyboardButton(t(lang,"contact_admin"),url=settings.admin_contact_url or "https://t.me/")],[InlineKeyboardButton(t(lang,"back"),callback_data="menu:back")]])
        await self.send_asset(q.message.chat_id,"support",t(lang,"support_menu"),kb)

    async def support_callback(self,q,u,lang,data):
        action=data.split(":",1)[1];await q.answer()
        if action=="new":
            ticket=await self.db.open_user_ticket(u.id) or await self.db.create_ticket(u.id);self.pending_support[u.id]=ticket.id;await self.db.log("TICKET_CREATED",actor_id=u.id,details=f"ticket={ticket.id}");await q.edit_message_text(t(lang,"ticket_prompt"),parse_mode=ParseMode.HTML,reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(t(lang,"cancel"),callback_data=f"ticket:cancel:{ticket.id}")]]))
        elif action=="status":
            ticket=await self.db.open_user_ticket(u.id);text=t(lang,"no_ticket") if not ticket else t(lang,"ticket_status",id=ticket.id,status=t(lang,"status_"+ticket.status.lower(),ticket.status));await q.edit_message_text(text,parse_mode=ParseMode.HTML,reply_markup=self.main_keyboard(lang))
        elif action=="faq":await q.edit_message_text(t(lang,"faq_text"),parse_mode=ParseMode.HTML,reply_markup=self.main_keyboard(lang))

    async def ticket_callback(self,q,u,lang,data):
        _,action,tid=data.split(":",2)
        if action=="cancel":self.pending_support.pop(u.id,None);await q.answer();await q.edit_message_text(t(lang,"cancelled"),reply_markup=self.main_keyboard(lang))

    async def private_messages(self,update,context):
        u=update.effective_user
        state=await self.db.user_stats(u.id)
        if not state or not state.rules_accepted:
            lang=await self.db.language(u.id,settings.default_language)
            await self.send_message(u.id,t(lang,"rules_required"),reply_markup=self.rules_keyboard(lang))
            return
        if u.id in self.pending_mafia_chat:
            self.pending_mafia_chat.discard(u.id); game=None
            game_id=getattr(self, "_mafia_chat_game", {}).get(u.id) if hasattr(self, "_mafia_chat_game") else None
            if game_id:
                game=await self.db.game(game_id)
            if game and game.active and game.phase=="NIGHT" and await self.db.get_role(game.id,u.id)=="mafia":
                for p,other in await self.db.players(game.id):
                    if p.alive and p.role=="mafia" and other.telegram_id!=u.id:
                        try:
                            await self.api.copy_message(other.telegram_id,u.id,update.effective_message.message_id)
                            await self.send_message(other.telegram_id,t(await self.db.language(other.telegram_id,game.language),"mafia_chat_prefix",name=escape(u.full_name)))
                        except TelegramError: pass
                await self.send_message(u.id,t(await self.db.language(u.id),"mafia_chat_sent"))
            return
        if u.id in self.pending_join_code:
            self.pending_join_code.discard(u.id)
            code=(update.effective_message.text or "").strip().upper()
            lang=await self.db.language(u.id,settings.default_language)
            await self.join_by_code(update, u, lang, code)
            return
        if u.id in self.pending_count:
            gid=self.pending_count.pop(u.id); text=(update.effective_message.text or "").strip()
            try: count=int(text)
            except ValueError: await self.send_message(u.id,t(await self.db.language(u.id),"custom_count_invalid")); self.pending_count[u.id]=gid; return
            game=await self.db.game(gid)
            if not game or game.creator_id!=u.id or not 5<=count<=40: await self.send_message(u.id,t(await self.db.language(u.id),"custom_count_invalid")); return
            cfg=composition(count);await self.db.set_game_fields(gid,player_limit=count,role_config=json.dumps(cfg));await self.send_message(u.id,t(await self.db.language(u.id),"custom_count_saved",count=count));await self.refresh_lobby(gid)
            game=await self.db.game(gid); rows=await self.db.players(gid)
            if game and game.auto_start and len(rows)>=game.player_limit:
                ok,reason=await self.engine.start(gid)
                if not ok: await self.send_message(u.id,t(await self.db.language(u.id),{"private_not_started":"open_private","private_delivery_failed":"private_delivery_failed","role_config_invalid":"role_invalid"}.get(reason,"invalid_action")))
            return
        tid=self.pending_support.get(u.id)
        if not tid:return
        ticket=await self.db.ticket(tid)
        if not ticket or ticket.status=="CLOSED":self.pending_support.pop(u.id,None);return
        msg=update.effective_message
        ctype="text";value=msg.text or msg.caption or ""
        if msg.photo:ctype="photo"
        elif msg.document:ctype="document"
        elif msg.voice:ctype="voice"
        elif msg.audio:ctype="audio"
        elif msg.video:ctype="video"
        await self.db.add_ticket_message(tid,u.id,"user",ctype,value,msg.message_id);await self.db.log("TICKET_MESSAGE",actor_id=u.id,details=f"ticket={tid};type={ctype}");self.pending_support.pop(u.id,None)
        await self.send_message(u.id,t(await self.db.language(u.id),"ticket_received",id=tid))
        try:
            user=await self.db.user_stats(u.id)
            await self.db.queue_admin_notification("TICKET_CREATED",u.id,{"ticket_id":tid,"name":user.display_name,"username":user.username,"type":ctype,"text":value})
        except Exception as exc:
            await self.db.log("ERROR",actor_id=u.id,details=f"ticket notification queue failed: {type(exc).__name__}: {exc}")

    async def member_is_player_eligible(self,chat_id,user_id):
        try:
            member=await self.api.get_chat_member(chat_id,user_id)
            if member.status in {"left","kicked"}: return False
            return not bool(getattr(member.user,"is_bot",False))
        except TelegramError:return False
    async def group_messages(self,update,context):
        if not update.message:return
        game=await self.db.active_game(update.effective_chat.id)
        if not game:return
        uid=update.effective_user.id;row=await self.db.player(game.id,uid)
        if not row:return
        if game.phase in {"NIGHT","VOTING","VOTING_REVOTE","READY_CHECK","EXTRA_TIME"}:
            if settings.delete_forbidden_messages:
                try:await update.message.delete()
                except TelegramError:pass
            warnings=await self.db.add_warning(game.id,uid);await self.db.log("WARNING",game.id,uid,f"group message during {game.phase}: {warnings}")
            if warnings>settings.max_warnings:await self.restrict_member(update.effective_chat.id,uid)
        elif game.phase=="DISCUSSION" and not row[0].alive:
            try:await update.message.delete()
            except TelegramError:pass
        elif game.phase=="LAST_WORD":
            allowed=self.engine.last_word_player.get(game.id)
            if uid!=allowed or row[0].final_word_used:
                try:await update.message.delete()
                except TelegramError:pass
            else:await self.db.set_player(game.id,uid,final_word_used=True)

    async def left_member(self,update,context):
        chat=update.effective_chat;game=await self.db.active_game(chat.id)
        if not game or not update.message or not update.message.left_chat_member:return
        uid=update.message.left_chat_member.id;row=await self.db.player(game.id,uid)
        if not row:return
        if game.phase=="LOBBY":
            if uid==game.creator_id:await self.db.cancel(game.id);await self.send_group_message(chat.id,t(game.language,"game_cancelled"));return
            await self.db.leave_game(game.id,uid);await self.refresh_lobby(game.id)
        else:await self.engine.player_left(game.id,uid)

    async def restrict_member(self,chat_id,user_id):
        try:await self.api.restrict_chat_member(chat_id,user_id,ChatPermissions(can_send_messages=False))
        except TelegramError:await self.db.log("ERROR",details=f"restrict failed {chat_id}/{user_id}")
    async def unlock_member(self,chat_id,user_id):
        try:await self.api.restrict_chat_member(chat_id,user_id,ChatPermissions(can_send_messages=True,can_send_audios=True,can_send_documents=True,can_send_photos=True,can_send_videos=True,can_send_video_notes=True,can_send_voice_notes=True,can_send_polls=True,can_send_other_messages=True,can_add_web_page_previews=True))
        except TelegramError:pass
    async def lock_group(self,chat_id):
        game=await self.db.active_game(chat_id)
        if game:
            for p,u in await self.db.players(game.id):
                if p.alive:await self.restrict_member(chat_id,u.telegram_id)
    async def open_day(self,chat_id):
        game=await self.db.active_game(chat_id)
        if game:
            for p,u in await self.db.players(game.id):
                if p.alive:await self.unlock_member(chat_id,u.telegram_id)
    async def prepare_last_word(self,chat_id,uid):
        game=await self.db.active_game(chat_id)
        if game:
            for _,u in await self.db.players(game.id):await self.restrict_member(chat_id,u.telegram_id)
            await self.unlock_member(chat_id,uid)
    async def send_extra_time_button(self,game_id):
        game=await self.db.game(game_id)
        if game and game.extra_time_enabled:await self.send_group_message(game.chat_id,t(game.language,"extra_button"),reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(t(game.language,"extra_button"),callback_data=f"extra_request:{game.id}")]]))
    async def send_extra_time_request(self,game_id):
        game=await self.db.game(game_id)
        if game:await self.send_group_message(game.chat_id,t(game.language,"extra_request",percent=game.extra_time_approval_percent),reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(t(game.language,"extra_yes"),callback_data=f"extra_vote:1:{game.id}"),InlineKeyboardButton(t(game.language,"extra_no"),callback_data=f"extra_vote:0:{game.id}")]]))
    async def send_message(self,user_id,text,**kwargs):
        try:return await self.api.send_message(user_id,text,parse_mode=ParseMode.HTML,**kwargs)
        except Forbidden:
            await self.db.mark_blocked(user_id,True)
            try: await self.db.queue_admin_notification("USER_BLOCKED", user_id, {"reason":"Telegram returned Forbidden while the User Bot tried to message the user."})
            except Exception: pass
            raise
    async def send_group_message(self,chat_id,text,**kwargs):
        try:return await self.api.send_message(chat_id,text,parse_mode=ParseMode.HTML,**kwargs)
        except (Forbidden,TelegramError):
            if isinstance(chat_id,int) and chat_id<0:await self.db.set_group_active(chat_id,False)
            raise
    async def send_phase_media(self,chat_id,kind,lang,text):
        await self.send_asset(chat_id, kind, text)
        return True

    async def send_night_result(self,game_id,killed,saved):
        game=await self.db.game(game_id);rows=await self.db.players(game_id)
        if saved:await self.send_group_message(game.chat_id,t(game.language,"saved"))
        for uid in killed:
            user=next((u for p,u in rows if u.telegram_id==uid),None)
            if user:await self.send_group_message(game.chat_id,t(game.language,"night_death",name=escape(user.full_name),role=""))
    async def finish_group(self,game_id,winner):
        self.lobby_messages.pop(game_id,None);game=await self.db.game(game_id);rows=await self.db.players(game_id)
        if not game:return
        roles="\n".join(f"• {escape(u.full_name)} — {escape(t(game.language,p.role))}" for p,u in rows)
        for _,u in rows:await self.unlock_member(game.chat_id,u.telegram_id)
        if winner=="CANCELLED":await self.send_group_message(game.chat_id,t(game.language,"game_cancelled_generic"));return
        winner_text=t(game.language,"role_mafia") if winner=="MAFIA" else t(game.language,"role_civilian")
        await self.send_group_message(game.chat_id,t(game.language,"game_over",winner=winner_text,roles=roles))
        if settings.channel_url:await self.send_group_message(game.chat_id,t(game.language,"channel_promo",url=settings.channel_url))
    async def send_startup_notice(self,chat_id):await self.send_group_message(chat_id,t(settings.default_language,"help_text"))
