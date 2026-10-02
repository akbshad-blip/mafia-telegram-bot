from __future__ import annotations

import asyncio
import hmac
import io
import logging
from datetime import datetime, timezone, timedelta
from html import escape

from telegram import Bot, Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.constants import ParseMode
from telegram.error import TelegramError, Forbidden
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, ContextTypes, filters

from config import settings
from database import Database
from admin_locales import LANGS, t

log = logging.getLogger(__name__)


class AdminBot:
    """Separate admin control plane.

    The Admin Bot is the control UI; the User Bot remains the sender for user/group
    broadcasts and game notifications. Pending admin notifications are persisted in
    PostgreSQL, so events that happen while the admin session is closed are delivered
    when the session is opened again.
    """

    def __init__(self, db: Database):
        self.db = db
        self.app = Application.builder().token(settings.admin_bot_token).concurrent_updates(True).build()
        self.user_api = Bot(settings.user_bot_token)
        self.authenticated: set[int] = set()
        self.awaiting_password: set[int] = set()
        self.failed_attempts: dict[int, int] = {}
        self.locked_until: dict[int, datetime] = {}
        self.ticket_reply: dict[int, int] = {}
        self.broadcast_target: dict[int, str | tuple[str, int]] = {}
        self.broadcast_source: dict[int, object] = {}
        self.broadcast_selection: set[int] = set()
        self.user_lookup: set[int] = set()
        self._initialized = False
        self._notification_task: asyncio.Task | None = None
        self._install_handlers()

    def _install_handlers(self):
        self.app.add_handler(CommandHandler("start", self.start))
        self.app.add_handler(CommandHandler("menu", self.menu_command))
        self.app.add_handler(CommandHandler("stats", self.stats_command))
        self.app.add_handler(CommandHandler("users", self.users_command))
        self.app.add_handler(CommandHandler("groups", self.groups_command))
        self.app.add_handler(CommandHandler("games", self.games_command))
        self.app.add_handler(CommandHandler("support", self.support_command))
        self.app.add_handler(CommandHandler("broadcast", self.broadcast_command))
        self.app.add_handler(CommandHandler("logs", self.logs_command))
        self.app.add_handler(CommandHandler("system", self.system_command))
        self.app.add_handler(CommandHandler("language", self.language_command))
        self.app.add_handler(CommandHandler("logout", self.logout))
        self.app.add_handler(CommandHandler("health", self.health_command))
        self.app.add_handler(CommandHandler("help", self.help_command))
        self.app.add_handler(CallbackQueryHandler(self.callbacks))
        self.app.add_handler(MessageHandler(filters.ChatType.PRIVATE & ~filters.COMMAND & filters.ALL, self.messages))
        self.app.add_error_handler(self.error_handler)

    async def initialize(self):
        if self._initialized:
            return
        await self.app.initialize()
        await self.user_api.initialize()
        me = await self.app.bot.get_me()
        await self.app.bot.set_my_commands([
            ("start", "Open admin login"), ("menu", "Open admin panel"),
            ("stats", "Statistics"), ("users", "Users"), ("groups", "Groups"),
            ("games", "Games"), ("support", "Support tickets"),
            ("broadcast", "Broadcast"), ("logs", "Logs"), ("system", "System"),
            ("health", "Check bot health"), ("language", "Panel language"),
            ("logout", "Close admin session"), ("help", "Admin help")
        ])
        log.info("Admin Bot initialized: @%s id=%s", me.username, me.id)
        self._initialized = True
        self._notification_task = asyncio.create_task(self._notification_loop())

    async def run(self):
        await self.initialize()
        await self.app.start()
        await self.app.updater.start_polling(allowed_updates=Update.ALL_TYPES, drop_pending_updates=False)
        try:
            await asyncio.Event().wait()
        finally:
            await self.app.updater.stop()
            await self.app.stop()
            await self.app.shutdown()
            await self.user_api.shutdown()

    def allowed_id(self, uid: int) -> bool:
        return uid in settings.admin_ids

    async def lang(self, uid: int) -> str:
        return await self.db.admin_language(uid, "en")

    def panel_keyboard(self, lang: str) -> InlineKeyboardMarkup:
        return InlineKeyboardMarkup([
            [InlineKeyboardButton(t(lang, "stats"), callback_data="admin:stats"), InlineKeyboardButton(t(lang, "users"), callback_data="admin:users")],
            [InlineKeyboardButton(t(lang, "groups"), callback_data="admin:groups"), InlineKeyboardButton(t(lang, "games"), callback_data="admin:games")],
            [InlineKeyboardButton(t(lang, "support"), callback_data="admin:tickets"), InlineKeyboardButton(t(lang, "broadcast"), callback_data="admin:broadcast")],
            [InlineKeyboardButton(t(lang, "logs"), callback_data="admin:logs"), InlineKeyboardButton(t(lang, "system"), callback_data="admin:system")],
            [InlineKeyboardButton(t(lang, "language"), callback_data="admin:language"), InlineKeyboardButton(t(lang, "refresh"), callback_data="admin:refresh")],
            [InlineKeyboardButton(t(lang, "logout"), callback_data="admin:logout")],
        ])

    async def _require_auth(self, update) -> bool:
        uid = update.effective_user.id
        if update.effective_chat.type != "private" or uid not in self.authenticated:
            if update.effective_chat.type == "private":
                lang = await self.lang(uid)
                await update.effective_message.reply_text(t(lang, "access"))
            return False
        return True

    async def start(self, update, context):
        if update.effective_chat.type != "private":
            return
        uid = update.effective_user.id
        lang = await self.lang(uid)
        if not self.allowed_id(uid):
            await update.effective_message.reply_text(t(lang, "access"))
            return
        locked = self.locked_until.get(uid)
        if locked and locked > datetime.now(timezone.utc):
            await update.effective_message.reply_text(t(lang, "locked"))
            return
        if uid in self.authenticated:
            await self.show_panel(uid)
            await self.flush_notifications(uid)
            return
        self.awaiting_password.add(uid)
        await update.effective_message.reply_text(t(lang, "password"), parse_mode=ParseMode.HTML)

    async def help_command(self, update, context):
        if await self._require_auth(update):
            lang=await self.lang(update.effective_user.id)
            text=t(lang,"admin_help")
            await update.effective_message.reply_text(text,parse_mode=ParseMode.HTML,reply_markup=self.panel_keyboard(lang))

    async def health_command(self, update, context):
        if not await self._require_auth(update): return
        uid=update.effective_user.id; lang=await self.lang(uid)
        started="✅"; user_ok="❌"; admin_ok="❌"; db_ok="❌"
        try: await self.user_api.get_me(); user_ok="✅"
        except TelegramError: pass
        try: await self.app.bot.get_me(); admin_ok="✅"
        except TelegramError: pass
        try: await self.db.admin_overview(); db_ok="✅"
        except Exception: log.exception("Admin health DB check failed")
        text=t(lang,"health",user_ok=user_ok,admin_ok=admin_ok,db_ok=db_ok,webhook_mode="ON" if settings.webhook_mode else "OFF")
        await update.effective_message.reply_text(text,parse_mode=ParseMode.HTML,reply_markup=self.panel_keyboard(lang))

    async def error_handler(self, update, context):
        log.exception("Admin Bot handler error", exc_info=context.error)
        if update and getattr(update,"effective_chat",None) and update.effective_chat.type=="private":
            uid=update.effective_user.id if update.effective_user else None
            if uid and uid in self.authenticated:
                try: await self.app.bot.send_message(uid,t(await self.lang(uid),"admin_error"))
                except TelegramError: pass

    async def language_command(self, update, context):
        uid = update.effective_user.id
        if not self.allowed_id(uid):
            return
        await update.effective_message.reply_text(
            t(await self.lang(uid), "choose_language"),
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(LANGS[k], callback_data=f"admin:lang:{k}")] for k in LANGS]),
        )

    async def menu_command(self, update, context):
        if await self._require_auth(update):
            await self.show_panel(update.effective_chat.id)

    async def stats_command(self, update, context):
        if await self._require_auth(update):
            await self.stats_menu_message(update.effective_chat.id, await self.lang(update.effective_user.id))

    async def users_command(self, update, context):
        if await self._require_auth(update):
            await self.users_menu_message(update.effective_chat.id, await self.lang(update.effective_user.id))

    async def groups_command(self, update, context):
        if await self._require_auth(update):
            await self.groups_menu_message(update.effective_chat.id, await self.lang(update.effective_user.id))

    async def games_command(self, update, context):
        if await self._require_auth(update):
            await self.games_menu_message(update.effective_chat.id, await self.lang(update.effective_user.id))

    async def support_command(self, update, context):
        if await self._require_auth(update):
            await self.tickets_menu_message(update.effective_chat.id, await self.lang(update.effective_user.id))

    async def broadcast_command(self, update, context):
        if await self._require_auth(update):
            await self.broadcast_menu_message(update.effective_chat.id, await self.lang(update.effective_user.id))

    async def logs_command(self, update, context):
        if await self._require_auth(update):
            await self.logs_menu_message(update.effective_chat.id, await self.lang(update.effective_user.id))

    async def system_command(self, update, context):
        if await self._require_auth(update):
            lang = await self.lang(update.effective_user.id)
            await update.effective_message.reply_text(t(lang, "system_text"), parse_mode=ParseMode.HTML, reply_markup=self.panel_keyboard(lang))

    async def users_menu_message(self, chat_id, lang):
        s = await self.db.admin_overview()
        await self.app.bot.send_message(chat_id, t(lang, "users_summary", **s), parse_mode=ParseMode.HTML,
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(t(lang, "find"), callback_data="admin:user_lookup")], [InlineKeyboardButton(t(lang, "back"), callback_data="admin:refresh")]]))

    async def groups_menu_message(self, chat_id, lang):
        groups = await self.db.groups_for_broadcast()
        rows = "\n".join(f"• {escape(g.title)} — <code>{g.chat_id}</code> — games: {g.games_count}" for g in groups) or "—"
        await self.app.bot.send_message(chat_id, t(lang, "groups_summary", rows=rows)[:3900], parse_mode=ParseMode.HTML, reply_markup=self.panel_keyboard(lang))

    async def games_menu_message(self, chat_id, lang):
        s = await self.db.admin_overview()
        await self.app.bot.send_message(chat_id, t(lang, "games_summary", **s), parse_mode=ParseMode.HTML, reply_markup=self.panel_keyboard(lang))

    async def tickets_menu_message(self, chat_id, lang):
        tickets = await self.db.tickets(30)
        rows = [[InlineKeyboardButton(f"#{x.id} · {x.status} · {x.user_id}", callback_data=f"admin:ticket:{x.id}")] for x in tickets]
        rows.append([InlineKeyboardButton(t(lang, "back"), callback_data="admin:refresh")])
        await self.app.bot.send_message(chat_id, t(lang, "tickets_summary"), parse_mode=ParseMode.HTML, reply_markup=InlineKeyboardMarkup(rows))

    async def logs_menu_message(self, chat_id, lang):
        rows = await self.db.recent_logs(30)
        text = t(lang, "logs_summary", rows="\n".join(f"• {r.created_at:%Y-%m-%d %H:%M:%S} | {escape(str(r.event))} | {escape(str(r.actor_id or '—'))} | {escape(str(r.details or ''))}" for r in rows) or "—")
        await self.app.bot.send_message(chat_id, text[:3900], parse_mode=ParseMode.HTML, reply_markup=self.panel_keyboard(lang))

    async def stats_menu_message(self, chat_id, lang):
        await self.app.bot.send_message(chat_id, t(lang, "stats_period"), parse_mode=ParseMode.HTML, reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton(t(lang,"today"), callback_data="period:today"), InlineKeyboardButton(t(lang,"week"), callback_data="period:7d")],
            [InlineKeyboardButton(t(lang,"month"), callback_data="period:month"), InlineKeyboardButton(t(lang,"year"), callback_data="period:year")],
            [InlineKeyboardButton(t(lang,"all"), callback_data="period:all")],
            [InlineKeyboardButton(t(lang,"back"), callback_data="admin:refresh")],
        ]))

    async def show_panel(self, chat_id, message_id=None):
        lang = await self.lang(chat_id)
        s = await self.db.admin_overview()
        text = (f"{t(lang,'dashboard')}\n━━━━━━━━━━━━━━\n"
                f"👤 {t(lang,'users')}: <b>{s['users']}</b>\n▶️ {t(lang,'started_label')}: <b>{s['started']}</b>\n📜 {t(lang,'rules_label')}: <b>{s['accepted']}</b>\n"
                f"🚫 {t(lang,'blocked')}: <b>{s['blocked']}</b>\n🏘 {t(lang,'groups')}: <b>{s['groups']}</b>\n🎮 {t(lang,'games')}: <b>{s['games']}</b>\n"
                f"🔥 {t(lang,'active_label')}: <b>{s['active_games']}</b>\n🔴 {t(lang,'mafia_wins_label')}: <b>{s['mafia_wins']}</b>\n⚪ {t(lang,'civilian_wins_label')}: <b>{s['civilian_wins']}</b>\n"
                f"🎫 {t(lang,'support')}: <b>{s['tickets']}</b>\n⚠️ {t(lang,'errors_label')}: <b>{s['errors']}</b>")
        if message_id:
            try:
                await self.app.bot.edit_message_text(chat_id, message_id, text, parse_mode=ParseMode.HTML, reply_markup=self.panel_keyboard(lang))
                return
            except TelegramError:
                pass
        await self.app.bot.send_message(chat_id, text, parse_mode=ParseMode.HTML, reply_markup=self.panel_keyboard(lang))

    async def messages(self, update, context):
        if update.effective_chat.type != "private":
            return
        uid = update.effective_user.id
        if uid in self.awaiting_password:
            await self.password_message(update)
            return
        if uid not in self.authenticated:
            return
        if uid in self.user_lookup:
            self.user_lookup.discard(uid)
            raw = (update.effective_message.text or "").strip()
            try:
                target = int(raw)
            except ValueError:
                await self.app.bot.send_message(uid, t(await self.lang(uid), "bad_id")); self.user_lookup.add(uid); return
            user = await self.db.user_card(target)
            if not user:
                await self.app.bot.send_message(uid, t(await self.lang(uid), "not_found")); return
            lang = await self.lang(uid)
            text = t(lang, "card", name=escape(user.display_name), username=escape(user.username or "—"), id=user.telegram_id,
                      language=user.language, first=user.first_start_at or "—", last=user.last_seen_at,
                      rules=user.rules_accepted, blocked=user.blocked_bot, games=user.games_played, wins=user.wins, losses=user.losses)
            await self.app.bot.send_message(uid, text, parse_mode=ParseMode.HTML, reply_markup=self.panel_keyboard(lang)); return
        if uid in self.broadcast_selection:
            self.broadcast_selection.discard(uid)
            raw = (update.effective_message.text or "").strip()
            try: target_id = int(raw)
            except ValueError:
                await self.app.bot.send_message(uid, t(await self.lang(uid), "bad_id")); self.broadcast_selection.add(uid); return
            self.broadcast_target[uid] = (self.broadcast_target.pop(uid), target_id)
            await self.app.bot.send_message(uid, t(await self.lang(uid), "send_content")); return
        if uid in self.ticket_reply:
            await self.receive_ticket_reply(update, uid); return
        if uid in self.broadcast_target:
            await self.receive_broadcast(update, uid); return

    async def password_message(self, update):
        uid = update.effective_user.id
        supplied = update.effective_message.text or ""
        try: await update.effective_message.delete()
        except TelegramError: pass
        self.awaiting_password.discard(uid)
        if hmac.compare_digest(supplied, settings.admin_password):
            self.failed_attempts.pop(uid, None); self.locked_until.pop(uid, None); self.authenticated.add(uid)
            await self.db.log("ADMIN_LOGIN", actor_id=uid)
            await self.show_panel(uid)
            await self.flush_notifications(uid)
            return
        n = self.failed_attempts.get(uid, 0) + 1; self.failed_attempts[uid] = n
        if n >= 5:
            self.failed_attempts[uid] = 0; self.locked_until[uid] = datetime.now(timezone.utc) + timedelta(minutes=5); msg=t(await self.lang(uid),"locked")
        else: msg=t(await self.lang(uid),"wrong")
        await self.db.log("ADMIN_LOGIN_FAILED", actor_id=uid, details=f"attempt={n}")
        await self.app.bot.send_message(uid, msg)

    async def logout(self, update, context):
        uid = update.effective_user.id
        if not self.allowed_id(uid): return
        self.authenticated.discard(uid); self.awaiting_password.discard(uid); self.ticket_reply.pop(uid, None); self.broadcast_target.pop(uid, None)
        await self.db.log("ADMIN_LOGOUT", actor_id=uid)
        await update.effective_message.reply_text(t(await self.lang(uid), "session_closed"))

    async def callbacks(self, update, context):
        q = update.callback_query; uid = q.from_user.id
        if uid not in self.authenticated:
            await q.answer(t(await self.lang(uid), "session_expired"), show_alert=True); return
        await q.answer(); data=q.data or ""; lang=await self.lang(uid)
        if data=="admin:refresh": await self.show_panel(uid,q.message.message_id); await self.flush_notifications(uid); return
        if data=="admin:logout": self.authenticated.discard(uid); await q.edit_message_text(t(lang,"session_closed")); await self.db.log("ADMIN_LOGOUT",actor_id=uid); return
        if data=="admin:language": await q.edit_message_text(t(lang,"choose_language"),reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(LANGS[k],callback_data=f"admin:lang:{k}")] for k in LANGS])); return
        if data.startswith("admin:lang:"):
            new=data.split(":")[-1]
            if new in LANGS: await self.db.set_admin_language(uid,new)
            await self.show_panel(uid,q.message.message_id); return
        if data=="admin:stats": await self.stats_menu_message(uid,lang); return
        if data=="admin:user_lookup": self.user_lookup.add(uid); await q.edit_message_text(t(lang,"send_id")); return
        if data=="admin:users": await self.users_menu_message(uid,lang); return
        if data=="admin:groups": await self.groups_menu_message(uid,lang); return
        if data=="admin:games": await self.games_menu_message(uid,lang); return
        if data=="admin:tickets": await self.tickets_menu_message(uid,lang); return
        if data.startswith("admin:ticket_cancel_reply:"):
            self.ticket_reply.pop(uid,None)
            await self.tickets_menu_message(uid,lang)
            return
        if data.startswith("admin:ticket:"): await self.ticket_action(q,uid,data,lang); return
        if data.startswith("admin:broadcast"): await self.broadcast_menu(q,uid,data,lang); return
        if data=="admin:logs": await self.logs_menu_message(uid,lang); return
        if data=="admin:system": await q.edit_message_text(t(lang,"system_text"),parse_mode=ParseMode.HTML,reply_markup=self.panel_keyboard(lang)); return
        if data.startswith("period:"): await self.period_menu(q,data,lang); return
        await q.answer(t(lang,"invalid_admin_action"), show_alert=True)

    async def period_menu(self,q,data,lang):
        key=data.split(":",1)[1]; now=datetime.now(timezone.utc); since=None
        if key=="today": since=now.replace(hour=0,minute=0,second=0,microsecond=0)
        elif key=="7d": since=now-timedelta(days=7)
        elif key=="month": since=now.replace(day=1,hour=0,minute=0,second=0,microsecond=0)
        elif key=="year": since=now.replace(month=1,day=1,hour=0,minute=0,second=0,microsecond=0)
        s=await self.db.admin_overview(since)
        period_label=t(lang,{"today":"period_today","7d":"period_7d","month":"period_month","year":"period_year","all":"period_all"}.get(key,"period_all"))
        await q.edit_message_text(t(lang,"period_result",period=period_label,**s),parse_mode=ParseMode.HTML,reply_markup=self.panel_keyboard(lang))

    async def ticket_action(self,q,uid,data,lang):
        tid=int(data.split(":")[-1]); ticket=await self.db.ticket(tid)
        if not ticket: await q.edit_message_text(t(lang, "ticket_not_found"), reply_markup=self.panel_keyboard(lang)); return
        if data.startswith("admin:ticket_assign:"):
            ok=await self.db.assign_ticket(tid,uid); await self.db.log("TICKET_ASSIGNED",actor_id=uid,details=f"ticket={tid}")
            await q.answer(t(lang,"assigned") if ok else t(lang,"ticket_owned"),show_alert=not ok)
        elif data.startswith("admin:ticket_reply:"):
            if ticket.assigned_admin_id not in (None,uid): await q.answer(t(lang,"ticket_owned"),show_alert=True); return
            await self.db.assign_ticket(tid,uid); self.ticket_reply[uid]=tid
            await q.edit_message_text(t(lang,"ticket_reply",id=tid),reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(t(lang,"cancel"),callback_data=f"admin:ticket_cancel_reply:{tid}")]])); return
        elif data.startswith("admin:ticket_cancel_reply:"):
            self.ticket_reply.pop(uid,None); await q.edit_message_text(t(lang,"tickets_summary"),reply_markup=self.panel_keyboard(lang)); return
        elif data.startswith("admin:ticket_close:"):
            if ticket.assigned_admin_id not in (None,uid): await q.answer(t(lang,"ticket_owned"),show_alert=True); return
            await self.db.close_ticket(tid); await self.db.log("TICKET_CLOSED",actor_id=uid,details=f"ticket={tid}")
        ticket=await self.db.ticket(tid)
        status_label=t(lang, "status_"+ticket.status.lower(), ticket.status)
        messages=await self.db.ticket_messages(tid, 8)
        history=[]
        for m in reversed(messages):
            who="👤" if m.direction=="user" else "🛡"
            body=escape(m.text or f"[{m.content_type}]")[:500]
            history.append(f"{who} <b>{m.content_type}</b>: {body}")
        history_text="\n".join(history) or "—"
        text=f"🎫 <b>Ticket #{tid}</b>\n━━━━━━━━━━━━━━\nStatus: <b>{escape(str(status_label))}</b>\nOwner: <code>{ticket.assigned_admin_id or '—'}</code>\nUser: <code>{ticket.user_id}</code>\n\n💬 <b>Последние сообщения</b>\n{history_text}"
        kb=[[InlineKeyboardButton(t(lang,"take"),callback_data=f"admin:ticket_assign:{tid}")],[InlineKeyboardButton(t(lang,"reply"),callback_data=f"admin:ticket_reply:{tid}"),InlineKeyboardButton(t(lang,"close"),callback_data=f"admin:ticket_close:{tid}")],[InlineKeyboardButton(t(lang,"back"),callback_data="admin:tickets")]]
        await q.edit_message_text(text,parse_mode=ParseMode.HTML,reply_markup=InlineKeyboardMarkup(kb))

    async def receive_ticket_reply(self,update,uid):
        tid=self.ticket_reply.pop(uid); ticket=await self.db.ticket(tid)
        if not ticket:return
        try:
            await self._send_update_content(self.user_api,ticket.user_id,update.effective_message,self.app.bot)
            msg=update.effective_message
            ctype=self._content_type(msg)
            await self.db.add_ticket_message(tid,uid,"admin",ctype,msg.text or msg.caption,msg.message_id)
            await self.db.log("TICKET_RESPONSE",actor_id=uid,details=f"ticket={tid}")
            await self.app.bot.send_message(uid,t(await self.lang(uid),"ticket_sent",id=tid))
        except TelegramError:
            await self.app.bot.send_message(uid,t(await self.lang(uid),"ticket_fail"))

    async def broadcast_menu_message(self,chat_id,lang):
        await self.app.bot.send_message(chat_id,t(lang,"broadcast_choose"),parse_mode=ParseMode.HTML,reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton(t(lang,"all_users"),callback_data="admin:broadcast_users"),InlineKeyboardButton(t(lang,"all_groups"),callback_data="admin:broadcast_groups")],
            [InlineKeyboardButton(t(lang,"selected_user"),callback_data="admin:broadcast_user_select"),InlineKeyboardButton(t(lang,"selected_group"),callback_data="admin:broadcast_group_select")],
            [InlineKeyboardButton(t(lang,"back"),callback_data="admin:refresh")],
        ]))

    async def broadcast_menu(self,q,uid,data,lang):
        if data=="admin:broadcast_confirm": await self.execute_broadcast(uid); return
        if data=="admin:broadcast_cancel": self.broadcast_source.pop(uid,None); await q.edit_message_text(t(lang,"cancel"),reply_markup=self.panel_keyboard(lang)); return
        target={"admin:broadcast_users":"users","admin:broadcast_groups":"groups","admin:broadcast_user_select":"user","admin:broadcast_group_select":"group"}.get(data)
        if target in {"user","group"}:
            self.broadcast_target[uid]=target; self.broadcast_selection.add(uid); await q.edit_message_text(t(lang,"send_id")); return
        if target:
            self.broadcast_target[uid]=target; await q.edit_message_text(t(lang,"send_content"),parse_mode=ParseMode.HTML); return
        if data=="admin:broadcast": await self.broadcast_menu_message(uid,lang)

    async def receive_broadcast(self,update,uid):
        target=self.broadcast_target.pop(uid); msg=update.effective_message; self.broadcast_source[uid]=(target,msg)
        if isinstance(target,tuple): count=1
        elif target=="users": count=len(await self.db.users_for_broadcast())
        else: count=len(await self.db.groups_for_broadcast())
        preview=msg.text or msg.caption or "[media]";lang=await self.lang(uid)
        await self.app.bot.send_message(uid,t(lang,"confirm",preview=escape(preview[:1500]),count=count),parse_mode=ParseMode.HTML,reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(t(lang,"send"),callback_data="admin:broadcast_confirm"),InlineKeyboardButton(t(lang,"cancel"),callback_data="admin:broadcast_cancel")]]))

    async def execute_broadcast(self,uid):
        target,msg=self.broadcast_source.pop(uid); lang=await self.lang(uid)
        if isinstance(target,tuple): recipients=[target[1]]; is_user=target[0]=="user"; target_label=target[0]
        else: recipients=await self.db.users_for_broadcast() if target=="users" else await self.db.groups_for_broadcast(); is_user=target=="users"; target_label=target
        success=failure=blocked=0
        for r in recipients:
            dest=r if isinstance(r,int) else (r.telegram_id if is_user else r.chat_id)
            try:
                await self._send_update_content(self.user_api,dest,msg,self.app.bot); success+=1
            except Forbidden:
                failure+=1;blocked+=1
                if is_user:
                    await self.db.mark_blocked(dest,True)
                    await self.db.queue_admin_notification("USER_BLOCKED",dest,{"reason":"Broadcast delivery returned Forbidden."})
                else: await self.db.set_group_active(dest,False)
            except TelegramError: failure+=1
        await self.db.log("BROADCAST_SENT",actor_id=uid,details=f"target={target_label};success={success};failure={failure};blocked={blocked}")
        await self.app.bot.send_message(uid,t(lang,"done",target=target_label,success=success,failure=failure,blocked=blocked),parse_mode=ParseMode.HTML,reply_markup=self.panel_keyboard(lang))

    @staticmethod
    def _content_type(msg):
        if msg.photo:return "photo"
        if msg.document:return "document"
        if msg.audio:return "audio"
        if msg.voice:return "voice"
        if msg.video:return "video"
        return "text"

    async def _send_update_content(self, bot: Bot, destination: int, msg, source_bot: Bot):
        caption=msg.caption
        if msg.text:
            return await bot.send_message(destination,msg.text)
        if msg.photo:
            return await bot.send_photo(destination, await self._download_media(source_bot,msg.photo[-1].file_id,"photo.jpg"), caption=caption)
        if msg.document:
            return await bot.send_document(destination, await self._download_media(source_bot,msg.document.file_id,msg.document.file_name or "file"), caption=caption)
        if msg.audio:
            return await bot.send_audio(destination, await self._download_media(source_bot,msg.audio.file_id,"audio"), caption=caption)
        if msg.voice:
            return await bot.send_voice(destination, await self._download_media(source_bot,msg.voice.file_id,"voice.ogg"), caption=caption)
        if msg.video:
            return await bot.send_video(destination, await self._download_media(source_bot,msg.video.file_id,"video.mp4"), caption=caption)
        return await bot.send_message(destination,caption or "")

    async def _download_media(self, source_bot: Bot, file_id: str, name: str):
        tg_file=await source_bot.get_file(file_id);buf=io.BytesIO();await tg_file.download_to_memory(buf);buf.seek(0);buf.name=name;return buf

    async def _notification_loop(self):
        while True:
            try:
                for uid in tuple(self.authenticated):
                    await self.flush_notifications(uid)
            except asyncio.CancelledError:
                return
            except Exception:
                log.exception("Admin notification loop failed")
            await asyncio.sleep(8)

    async def flush_notifications(self,uid):
        if uid not in self.authenticated:return
        rows=await self.db.pending_admin_notifications(uid,30)
        if not rows:return
        lang=await self.lang(uid); delivered=[]
        for row in rows:
            try:
                payload={}
                try:
                    import json;payload=json.loads(row.payload or "{}")
                except Exception: pass
                user=await self.db.user_card(row.user_id) if row.user_id else None
                if row.event_type=="NEW_USER" and user:
                    text=(f"{t(lang,'new_user')}\n━━━━━━━━━━━━━━\n👤 <b>{escape(user.display_name)}</b>\n"
                          f"Username: @{escape(user.username) if user.username else '—'}\n🆔 <code>{user.telegram_id}</code>\n"
                          f"🌐 Language: {user.language}\n🕐 First start: {user.first_start_at or '—'}\n\n📌 User has opened the User Bot for the first time.")
                    await self.app.bot.send_message(uid,text,parse_mode=ParseMode.HTML,reply_markup=self.panel_keyboard(lang))
                elif row.event_type=="USER_BLOCKED" and user:
                    text=(f"{t(lang,'blocked')}\n━━━━━━━━━━━━━━\n👤 <b>{escape(user.display_name)}</b>\n"
                          f"Username: @{escape(user.username) if user.username else '—'}\n🆔 <code>{user.telegram_id}</code>\n\n"
                          f"Reason: {escape(payload.get('reason','Telegram Forbidden'))}")
                    await self.app.bot.send_message(uid,text,parse_mode=ParseMode.HTML,reply_markup=self.panel_keyboard(lang))
                elif row.event_type=="TICKET_CREATED" and user:
                    tid=payload.get("ticket_id","—")
                    text=(f"🎫 <b>New support ticket #{tid}</b>\n━━━━━━━━━━━━━━\n"
                          f"👤 <b>{escape(user.display_name)}</b>\nUsername: @{escape(user.username) if user.username else '—'}\n"
                          f"🆔 <code>{user.telegram_id}</code>\n📎 Type: <b>{escape(str(payload.get('type','text')))}</b>\n"
                          f"💬 {escape(str(payload.get('text') or 'No text'))[:1200]}")
                    await self.app.bot.send_message(uid,text,parse_mode=ParseMode.HTML,reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(t(lang,"open_ticket"),callback_data=f"admin:ticket:{tid}")],[InlineKeyboardButton(t(lang,"back"),callback_data="admin:refresh")]]))
                else:
                    await self.app.bot.send_message(uid,f"🔔 {escape(row.event_type)}\n{escape(str(row.payload or ''))}")
                delivered.append(row.id)
            except TelegramError:
                break
        if delivered: await self.db.mark_admin_notifications_delivered(uid,delivered)
