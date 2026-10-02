from __future__ import annotations

from datetime import datetime, timezone, timedelta
from typing import Any
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit
import json
import secrets
import string
from sqlalchemy import String, Integer, BigInteger, Boolean, DateTime, Text, ForeignKey, select, func, desc, inspect, text as sql_text
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import UniqueConstraint


def now() -> datetime:
    return datetime.now(timezone.utc)


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    telegram_id: Mapped[int] = mapped_column(BigInteger, unique=True, index=True)
    username: Mapped[str | None] = mapped_column(String(255), nullable=True)
    display_name: Mapped[str] = mapped_column(String(255), default="")
    language: Mapped[str] = mapped_column(String(2), default="ru")
    started_bot: Mapped[bool] = mapped_column(Boolean, default=False)
    rules_accepted: Mapped[bool] = mapped_column(Boolean, default=False)
    rules_accepted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    first_start_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    blocked_bot: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now)
    last_seen_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now)
    games_played: Mapped[int] = mapped_column(Integer, default=0)
    wins: Mapped[int] = mapped_column(Integer, default=0)
    losses: Mapped[int] = mapped_column(Integer, default=0)


class UserRoleStat(Base):
    __tablename__ = "user_role_stats"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    role: Mapped[str] = mapped_column(String(30))
    games: Mapped[int] = mapped_column(Integer, default=0)
    wins: Mapped[int] = mapped_column(Integer, default=0)
    losses: Mapped[int] = mapped_column(Integer, default=0)
    __table_args__ = (UniqueConstraint("user_id", "role", name="uq_user_role_stat"),)


class Group(Base):
    __tablename__ = "groups"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    chat_id: Mapped[int] = mapped_column(BigInteger, unique=True, index=True)
    title: Mapped[str] = mapped_column(String(255), default="")
    language: Mapped[str] = mapped_column(String(2), default="ru")
    games_count: Mapped[int] = mapped_column(Integer, default=0)
    bot_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now)
    last_seen_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now)


class Game(Base):
    __tablename__ = "games"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    chat_id: Mapped[int] = mapped_column(BigInteger, index=True)
    creator_id: Mapped[int] = mapped_column(BigInteger)
    language: Mapped[str] = mapped_column(String(2), default="ru")
    phase: Mapped[str] = mapped_column(String(40), default="LOBBY")
    phase_started_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now)
    phase_ends_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    night_number: Mapped[int] = mapped_column(Integer, default=0)
    day_number: Mapped[int] = mapped_column(Integer, default=0)
    voting_round: Mapped[int] = mapped_column(Integer, default=1)
    revote_candidates: Mapped[str | None] = mapped_column(Text, nullable=True)
    extra_time_used: Mapped[bool] = mapped_column(Boolean, default=False)
    active: Mapped[bool] = mapped_column(Boolean, default=True)
    winner: Mapped[str | None] = mapped_column(String(30), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now)
    finished_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    player_limit: Mapped[int] = mapped_column(Integer, default=10)
    room_code: Mapped[str] = mapped_column(String(12), unique=True, index=True, default="")
    role_config: Mapped[str] = mapped_column(Text, default='{"mafia":2,"doctor":1,"commissioner":1,"lover":1,"detective":0,"bodyguard":0,"civilian":5}')
    auto_start: Mapped[bool] = mapped_column(Boolean, default=False)
    ready_required: Mapped[bool] = mapped_column(Boolean, default=True)
    reveal_role_after_death: Mapped[bool] = mapped_column(Boolean, default=False)
    allow_skip_vote: Mapped[bool] = mapped_column(Boolean, default=True)
    doctor_self_heal: Mapped[bool] = mapped_column(Boolean, default=True)
    doctor_self_heal_uses: Mapped[int] = mapped_column(Integer, default=1)
    doctor_repeat_target: Mapped[bool] = mapped_column(Boolean, default=False)
    commissioner_eliminate: Mapped[bool] = mapped_column(Boolean, default=True)
    tie_revote: Mapped[bool] = mapped_column(Boolean, default=True)
    extra_time_enabled: Mapped[bool] = mapped_column(Boolean, default=False)
    night_timeout: Mapped[int] = mapped_column(Integer, default=120)
    mafia_timeout: Mapped[int] = mapped_column(Integer, default=120)
    doctor_timeout: Mapped[int] = mapped_column(Integer, default=60)
    commissioner_timeout: Mapped[int] = mapped_column(Integer, default=60)
    discussion_timeout: Mapped[int] = mapped_column(Integer, default=120)
    voting_timeout: Mapped[int] = mapped_column(Integer, default=60)
    last_word_timeout: Mapped[int] = mapped_column(Integer, default=30)
    extra_time_seconds: Mapped[int] = mapped_column(Integer, default=60)
    extra_time_approval_percent: Mapped[int] = mapped_column(Integer, default=80)


class Player(Base):
    __tablename__ = "players"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    game_id: Mapped[int] = mapped_column(ForeignKey("games.id"), index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    role: Mapped[str | None] = mapped_column(String(30), nullable=True)
    alive: Mapped[bool] = mapped_column(Boolean, default=True)
    ready: Mapped[bool] = mapped_column(Boolean, default=False)
    warned: Mapped[int] = mapped_column(Integer, default=0)
    final_word_used: Mapped[bool] = mapped_column(Boolean, default=False)
    doctor_self_heal_used: Mapped[bool] = mapped_column(Boolean, default=False)
    doctor_self_heal_count: Mapped[int] = mapped_column(Integer, default=0)
    last_doctor_target: Mapped[int | None] = mapped_column(BigInteger, nullable=True)
    last_vote: Mapped[int | None] = mapped_column(BigInteger, nullable=True)
    joined_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now)
    eliminated_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    __table_args__ = (UniqueConstraint("game_id", "user_id", name="uq_game_player"),)


class Action(Base):
    __tablename__ = "actions"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    game_id: Mapped[int] = mapped_column(ForeignKey("games.id"), index=True)
    user_id: Mapped[int] = mapped_column(BigInteger, index=True)
    kind: Mapped[str] = mapped_column(String(40))
    target_user_id: Mapped[int | None] = mapped_column(BigInteger, nullable=True)
    value: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now)


class ExtraVote(Base):
    __tablename__ = "extra_votes"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    game_id: Mapped[int] = mapped_column(ForeignKey("games.id"), index=True)
    user_id: Mapped[int] = mapped_column(BigInteger)
    value: Mapped[bool] = mapped_column(Boolean)
    __table_args__ = (UniqueConstraint("game_id", "user_id", name="uq_extra_vote"),)


class SupportTicket(Base):
    __tablename__ = "support_tickets"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(BigInteger, index=True)
    subject: Mapped[str] = mapped_column(String(255), default="Support")
    status: Mapped[str] = mapped_column(String(30), default="NEW", index=True)
    assigned_admin_id: Mapped[int | None] = mapped_column(BigInteger, nullable=True, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now)
    closed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)


class SupportMessage(Base):
    __tablename__ = "support_messages"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    ticket_id: Mapped[int] = mapped_column(ForeignKey("support_tickets.id"), index=True)
    sender_id: Mapped[int] = mapped_column(BigInteger, index=True)
    direction: Mapped[str] = mapped_column(String(20))
    content_type: Mapped[str] = mapped_column(String(30), default="text")
    telegram_message_id: Mapped[int | None] = mapped_column(BigInteger, nullable=True)
    text: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now)


class Broadcast(Base):
    __tablename__ = "broadcasts"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    actor_id: Mapped[int] = mapped_column(BigInteger)
    target: Mapped[str] = mapped_column(String(30))
    target_id: Mapped[int | None] = mapped_column(BigInteger, nullable=True)
    status: Mapped[str] = mapped_column(String(30), default="DRAFT")
    content_type: Mapped[str] = mapped_column(String(30), default="text")
    source_chat_id: Mapped[int | None] = mapped_column(BigInteger, nullable=True)
    source_message_id: Mapped[int | None] = mapped_column(BigInteger, nullable=True)
    success_count: Mapped[int] = mapped_column(Integer, default=0)
    failure_count: Mapped[int] = mapped_column(Integer, default=0)
    blocked_count: Mapped[int] = mapped_column(Integer, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now)
    finished_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)


class AdminNotification(Base):
    __tablename__ = "admin_notifications"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    admin_id: Mapped[int] = mapped_column(BigInteger, index=True)
    event_type: Mapped[str] = mapped_column(String(60), index=True)
    user_id: Mapped[int | None] = mapped_column(BigInteger, nullable=True, index=True)
    payload: Mapped[str | None] = mapped_column(Text, nullable=True)
    delivered: Mapped[bool] = mapped_column(Boolean, default=False, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now, index=True)


class AdminPreference(Base):
    __tablename__ = "admin_preferences"
    admin_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    language: Mapped[str] = mapped_column(String(2), default="en")


class Log(Base):
    __tablename__ = "logs"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    game_id: Mapped[int | None] = mapped_column(Integer, nullable=True, index=True)
    actor_id: Mapped[int | None] = mapped_column(BigInteger, nullable=True)
    event: Mapped[str] = mapped_column(String(100), index=True)
    details: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now, index=True)


    async def queue_admin_notification(self, event_type, user_id, payload):
        async with self.session() as s:
            for admin_id in __import__("config").settings.admin_ids:
                s.add(AdminNotification(admin_id=admin_id, event_type=event_type, user_id=user_id, payload=json.dumps(payload, ensure_ascii=False)))
            await s.commit()

    async def pending_admin_notifications(self, admin_id, limit=30):
        async with self.session() as s:
            return (await s.execute(select(AdminNotification).where(AdminNotification.admin_id==admin_id, AdminNotification.delivered.is_(False)).order_by(AdminNotification.created_at).limit(limit))).scalars().all()

    async def mark_admin_notifications_delivered(self, admin_id, ids):
        if not ids: return
        async with self.session() as s:
            rows=(await s.execute(select(AdminNotification).where(AdminNotification.admin_id==admin_id, AdminNotification.id.in_(ids)))).scalars().all()
            for row in rows: row.delivered=True
            await s.commit()

    async def admin_language(self, admin_id, default="en"):
        async with self.session() as s:
            row=await s.get(AdminPreference, admin_id)
            return row.language if row else default

    async def set_admin_language(self, admin_id, language):
        async with self.session() as s:
            row=await s.get(AdminPreference, admin_id)
            if row: row.language=language
            else: s.add(AdminPreference(admin_id=admin_id, language=language))
            await s.commit()


def normalize_database_url(url: str) -> tuple[str, dict]:
    """Normalize common PostgreSQL URLs for SQLAlchemy's asyncpg dialect."""
    if url.startswith("postgres://"):
        url = "postgresql://" + url[len("postgres://"): ]
    if url.startswith("postgresql://"):
        parts = urlsplit(url)
        query = dict(parse_qsl(parts.query, keep_blank_values=True))
        connect_args = {}
        # Supabase/Render connection strings commonly expose sslmode=require.
        # asyncpg expects this as its `ssl` connect argument instead.
        sslmode = query.pop("sslmode", None)
        if sslmode and sslmode.lower() in {"require", "verify-ca", "verify-full"}:
            connect_args["ssl"] = "require"
        clean_query = urlencode(query)
        url = urlunsplit(("postgresql+asyncpg", parts.netloc, parts.path, clean_query, parts.fragment))
        return url, connect_args
    return url, {}


class Database:
    def __init__(self, url: str):
        normalized_url, connect_args = normalize_database_url(url)
        self.engine = create_async_engine(normalized_url, echo=False, pool_pre_ping=True, connect_args=connect_args)
        self.session_factory = async_sessionmaker(self.engine, expire_on_commit=False)

    def session(self) -> AsyncSession:
        return self.session_factory()

    async def init(self):
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
            # Lightweight additive migration for the project's existing SQLite/Postgres DBs.
            # New deployments are handled by create_all; old deployments get nullable/default columns.
            if conn.dialect.name == "sqlite":
                existing = await conn.run_sync(lambda c: {x[1] for x in inspect(c).get_columns("users")})
                additions = {
                    "rules_accepted": "BOOLEAN DEFAULT 0", "rules_accepted_at": "DATETIME", "first_start_at": "DATETIME", "blocked_bot": "BOOLEAN DEFAULT 0"
                }
                for col, typ in additions.items():
                    if col not in existing: await conn.execute(sql_text(f"ALTER TABLE users ADD COLUMN {col} {typ}"))
                existing_g = await conn.run_sync(lambda c: {x[1] for x in inspect(c).get_columns("groups")})
                if "bot_active" not in existing_g: await conn.execute(sql_text("ALTER TABLE groups ADD COLUMN bot_active BOOLEAN DEFAULT 1"))
                existing_game = await conn.run_sync(lambda c: {x[1] for x in inspect(c).get_columns("games")})
                additions_g = {
                    "player_limit":"INTEGER DEFAULT 10","room_code":"VARCHAR(12) DEFAULT ''","role_config":"TEXT DEFAULT '{\"mafia\":2,\"doctor\":1,\"commissioner\":1,\"lover\":0,\"detective\":0,\"bodyguard\":0,\"civilian\":6}'","doctor_self_heal_uses":"INTEGER DEFAULT 1","mafia_timeout":"INTEGER DEFAULT 120","doctor_timeout":"INTEGER DEFAULT 60","commissioner_timeout":"INTEGER DEFAULT 60"
                }
                for col, typ in additions_g.items():
                    if col not in existing_game: await conn.execute(sql_text(f"ALTER TABLE games ADD COLUMN {col} {typ}"))
                existing_p = await conn.run_sync(lambda c: {x[1] for x in inspect(c).get_columns("players")})
                if "doctor_self_heal_count" not in existing_p: await conn.execute(sql_text("ALTER TABLE players ADD COLUMN doctor_self_heal_count INTEGER DEFAULT 0"))
            elif conn.dialect.name == "postgresql":
                statements = [
                    "ALTER TABLE users ADD COLUMN IF NOT EXISTS rules_accepted BOOLEAN DEFAULT FALSE",
                    "ALTER TABLE users ADD COLUMN IF NOT EXISTS rules_accepted_at TIMESTAMPTZ",
                    "ALTER TABLE users ADD COLUMN IF NOT EXISTS first_start_at TIMESTAMPTZ",
                    "ALTER TABLE users ADD COLUMN IF NOT EXISTS blocked_bot BOOLEAN DEFAULT FALSE",
                    "ALTER TABLE groups ADD COLUMN IF NOT EXISTS bot_active BOOLEAN DEFAULT TRUE",
                    "ALTER TABLE games ADD COLUMN IF NOT EXISTS player_limit INTEGER DEFAULT 10",
                    "ALTER TABLE games ADD COLUMN IF NOT EXISTS room_code VARCHAR(12) DEFAULT ''",
                    "ALTER TABLE games ADD COLUMN IF NOT EXISTS role_config TEXT DEFAULT '{\"mafia\":2,\"doctor\":1,\"commissioner\":1,\"lover\":0,\"detective\":0,\"bodyguard\":0,\"civilian\":6}'",
                    "ALTER TABLE games ADD COLUMN IF NOT EXISTS doctor_self_heal_uses INTEGER DEFAULT 1",
                    "ALTER TABLE games ADD COLUMN IF NOT EXISTS mafia_timeout INTEGER DEFAULT 120",
                    "ALTER TABLE games ADD COLUMN IF NOT EXISTS doctor_timeout INTEGER DEFAULT 60",
                    "ALTER TABLE games ADD COLUMN IF NOT EXISTS commissioner_timeout INTEGER DEFAULT 60",
                    "ALTER TABLE players ADD COLUMN IF NOT EXISTS doctor_self_heal_count INTEGER DEFAULT 0",
                    # Telegram user/chat/message IDs can exceed PostgreSQL INT32.
                    "ALTER TABLE users ALTER COLUMN telegram_id TYPE BIGINT",
                    "ALTER TABLE groups ALTER COLUMN chat_id TYPE BIGINT",
                    "ALTER TABLE games ALTER COLUMN chat_id TYPE BIGINT",
                    "ALTER TABLE games ALTER COLUMN creator_id TYPE BIGINT",
                    "ALTER TABLE players ALTER COLUMN last_doctor_target TYPE BIGINT",
                    "ALTER TABLE players ALTER COLUMN last_vote TYPE BIGINT",
                    "ALTER TABLE actions ALTER COLUMN user_id TYPE BIGINT",
                    "ALTER TABLE actions ALTER COLUMN target_user_id TYPE BIGINT",
                    "ALTER TABLE extra_votes ALTER COLUMN user_id TYPE BIGINT",
                    "ALTER TABLE support_tickets ALTER COLUMN user_id TYPE BIGINT",
                    "ALTER TABLE support_tickets ALTER COLUMN assigned_admin_id TYPE BIGINT",
                    "ALTER TABLE support_messages ALTER COLUMN sender_id TYPE BIGINT",
                    "ALTER TABLE support_messages ALTER COLUMN telegram_message_id TYPE BIGINT",
                    "ALTER TABLE broadcasts ALTER COLUMN actor_id TYPE BIGINT",
                    "ALTER TABLE broadcasts ALTER COLUMN target_id TYPE BIGINT",
                    "ALTER TABLE broadcasts ALTER COLUMN source_chat_id TYPE BIGINT",
                    "ALTER TABLE broadcasts ALTER COLUMN source_message_id TYPE BIGINT",
                    "ALTER TABLE logs ALTER COLUMN actor_id TYPE BIGINT",
                ]
                # Execute migration SQL directly so JSON defaults containing colons are not parsed as bind parameters.
                for statement in statements: await conn.exec_driver_sql(statement)

    async def close(self): await self.engine.dispose()

    async def get_or_create_user(self, tg_user, default_lang="ru", mark_started=False):
        async with self.session() as s:
            user = await s.scalar(select(User).where(User.telegram_id == tg_user.id))
            if user is None:
                user = User(telegram_id=tg_user.id, username=tg_user.username, display_name=tg_user.full_name, language=default_lang)
                s.add(user); await s.flush()
            else:
                user.username = tg_user.username; user.display_name = tg_user.full_name; user.last_seen_at = now()
            if mark_started:
                user.started_bot = True
                if user.first_start_at is None: user.first_start_at = now()
                user.blocked_bot = False
            await s.commit(); return user

    async def accept_rules(self, telegram_id: int):
        async with self.session() as s:
            u = await s.scalar(select(User).where(User.telegram_id == telegram_id))
            if u: u.rules_accepted = True; u.rules_accepted_at = now(); u.started_bot = True; u.last_seen_at = now()
            await s.commit()

    async def language(self, telegram_id: int, default="ru"):
        async with self.session() as s: return (await s.scalar(select(User.language).where(User.telegram_id == telegram_id))) or default
    async def set_language(self, telegram_id, lang):
        async with self.session() as s:
            u=await s.scalar(select(User).where(User.telegram_id==telegram_id))
            if u: u.language=lang; u.last_seen_at=now()
            await s.commit()
    async def user_stats(self, telegram_id):
        async with self.session() as s: return await s.scalar(select(User).where(User.telegram_id==telegram_id))
    async def role_stats(self, telegram_id):
        async with self.session() as s:
            u=await s.scalar(select(User.id).where(User.telegram_id==telegram_id))
            if not u: return []
            return (await s.execute(select(UserRoleStat).where(UserRoleStat.user_id==u).order_by(UserRoleStat.role))).scalars().all()

    async def active_game(self, chat_id):
        async with self.session() as s:
            q=await s.execute(select(Game).where(Game.chat_id==chat_id,Game.active.is_(True)).order_by(desc(Game.id)).limit(1)); return q.scalar_one_or_none()
    async def game(self, game_id):
        async with self.session() as s: return await s.scalar(select(Game).where(Game.id==game_id))
    async def game_by_code(self, code):
        async with self.session() as s: return await s.scalar(select(Game).where(Game.room_code==code.upper(),Game.active.is_(True),Game.phase=="LOBBY"))
    async def players(self, game_id):
        async with self.session() as s:
            return (await s.execute(select(Player,User).join(User,User.id==Player.user_id).where(Player.game_id==game_id).order_by(Player.joined_at))).all()
    async def player(self, game_id, telegram_id):
        async with self.session() as s:
            return (await s.execute(select(Player,User).join(User,User.id==Player.user_id).where(Player.game_id==game_id,User.telegram_id==telegram_id))).first()

    async def create_game(self, chat_id, creator_id, title, language="ru", player_limit=10, role_config=None):
        from game.roles import composition
        role_config = role_config or composition(player_limit)
        async with self.session() as s:
            group=await s.scalar(select(Group).where(Group.chat_id==chat_id))
            if group is None: group=Group(chat_id=chat_id,title=title,language=language); s.add(group)
            else: group.title=title; group.last_seen_at=now(); group.language=language; group.bot_active=True
            code=secrets.token_hex(3).upper()
            while await s.scalar(select(Game.id).where(Game.room_code==code)): code=secrets.token_hex(3).upper()
            game=Game(chat_id=chat_id,creator_id=creator_id,language=language,player_limit=player_limit,room_code=code,role_config=json.dumps(role_config),night_timeout=120,mafia_timeout=120,doctor_timeout=60,commissioner_timeout=60,discussion_timeout=120,voting_timeout=60,last_word_timeout=30)
            s.add(game); group.games_count+=1; await s.flush(); await s.commit(); return game

    async def join_game(self, game_id, telegram_id, tg_user):
        async with self.session() as s:
            user=await s.scalar(select(User).where(User.telegram_id==telegram_id))
            if user is None: user=User(telegram_id=telegram_id,username=tg_user.username,display_name=tg_user.full_name); s.add(user); await s.flush()
            else: user.username=tg_user.username; user.display_name=tg_user.full_name; user.last_seen_at=now()
            game=await s.get(Game,game_id)
            if not game or not game.active or game.phase!="LOBBY": return False,"inactive"
            existing=await s.scalar(select(Player).where(Player.game_id==game_id,Player.user_id==user.id))
            if existing:return False,"exists"
            count=await s.scalar(select(func.count(Player.id)).where(Player.game_id==game_id))
            if int(count or 0)>=game.player_limit:return False,"full"
            s.add(Player(game_id=game_id,user_id=user.id)); await s.commit(); return True,int(count or 0)+1

    async def leave_game(self, game_id, telegram_id):
        async with self.session() as s:
            p=await s.scalar(select(Player).join(User,User.id==Player.user_id).where(Player.game_id==game_id,User.telegram_id==telegram_id))
            if not p:return False
            await s.delete(p); await s.commit(); return True
    async def set_phase(self, game_id, phase, seconds):
        async with self.session() as s:
            g=await s.get(Game,game_id)
            if not g:return
            g.phase=phase; g.phase_started_at=now(); g.phase_ends_at=now()+timedelta(seconds=seconds) if seconds is not None else None; await s.commit()
    async def set_game_fields(self, game_id, **fields):
        async with self.session() as s:
            g=await s.get(Game,game_id)
            if g:
                for k,v in fields.items(): setattr(g,k,v)
                await s.commit()
    async def set_ready(self, game_id, telegram_id, value): await self.set_player(game_id,telegram_id,ready=value)
    async def assign_roles(self, game_id, assignments):
        async with self.session() as s:
            for tg,role in assignments.items():
                p=await s.scalar(select(Player).join(User,User.id==Player.user_id).where(Player.game_id==game_id,User.telegram_id==tg))
                if p:p.role=role
            await s.commit()
    async def record_action(self, game_id,user_id,kind,target_user_id=None,value=None):
        async with self.session() as s:
            rows=(await s.execute(select(Action).where(Action.game_id==game_id,Action.user_id==user_id,Action.kind==kind))).scalars().all()
            for r in rows: await s.delete(r)
            s.add(Action(game_id=game_id,user_id=user_id,kind=kind,target_user_id=target_user_id,value=value)); await s.commit()
    async def action_targets(self,game_id,kind):
        async with self.session() as s:return (await s.execute(select(Action).where(Action.game_id==game_id,Action.kind==kind))).scalars().all()
    async def clear_actions_for_user(self,game_id,telegram_id):
        async with self.session() as s:
            for r in (await s.execute(select(Action).where(Action.game_id==game_id,Action.user_id==telegram_id))).scalars().all(): await s.delete(r)
            await s.commit()
    async def clear_vote_for_user(self,game_id,telegram_id): await self.set_player(game_id,telegram_id,last_vote=None)
    async def clear_actions(self,game_id,kind=None):
        async with self.session() as s:
            stmt=select(Action).where(Action.game_id==game_id)
            if kind:stmt=stmt.where(Action.kind==kind)
            for r in (await s.execute(stmt)).scalars().all(): await s.delete(r)
            await s.commit()
    async def add_warning(self,game_id,telegram_id):
        async with self.session() as s:
            p=await s.scalar(select(Player).join(User,User.id==Player.user_id).where(Player.game_id==game_id,User.telegram_id==telegram_id))
            if not p:return 0
            p.warned+=1; await s.commit(); return p.warned
    async def set_player(self,game_id,telegram_id,**fields):
        async with self.session() as s:
            p=await s.scalar(select(Player).join(User,User.id==Player.user_id).where(Player.game_id==game_id,User.telegram_id==telegram_id))
            if p:
                for k,v in fields.items():setattr(p,k,v)
                await s.commit()
    async def get_role(self,game_id,telegram_id):
        r=await self.player(game_id,telegram_id);return r[0].role if r else None
    async def alive_ids(self,game_id):return [u.telegram_id for p,u in await self.players(game_id) if p.alive]
    async def eliminate(self,game_id,telegram_id):await self.set_player(game_id,telegram_id,alive=False,eliminated_at=now())
    async def set_vote(self,game_id,voter_id,target_id):await self.set_player(game_id,voter_id,last_vote=target_id)
    async def vote_counts(self,game_id):
        async with self.session() as s:
            counts={}
            for p in (await s.execute(select(Player).where(Player.game_id==game_id,Player.alive.is_(True)))).scalars().all():
                if p.last_vote is not None:counts[p.last_vote]=counts.get(p.last_vote,0)+1
            return counts
    async def clear_votes(self,game_id):
        async with self.session() as s:
            for p in (await s.execute(select(Player).where(Player.game_id==game_id))).scalars().all():p.last_vote=None
            await s.commit()
    async def add_extra_vote(self,game_id,telegram_id,value):
        async with self.session() as s:
            r=await s.scalar(select(ExtraVote).where(ExtraVote.game_id==game_id,ExtraVote.user_id==telegram_id))
            if r:r.value=value
            else:s.add(ExtraVote(game_id=game_id,user_id=telegram_id,value=value))
            await s.commit()
    async def extra_counts(self,game_id):
        async with self.session() as s:
            rows=(await s.execute(select(ExtraVote).where(ExtraVote.game_id==game_id))).scalars().all();return sum(x.value for x in rows),sum(not x.value for x in rows)
    async def clear_extra_votes(self,game_id):
        async with self.session() as s:
            for r in (await s.execute(select(ExtraVote).where(ExtraVote.game_id==game_id))).scalars().all():await s.delete(r)
            await s.commit()
    async def set_game_setting(self,game_id,field,value):
        allowed={"auto_start","ready_required","reveal_role_after_death","allow_skip_vote","doctor_self_heal","doctor_self_heal_uses","doctor_repeat_target","commissioner_eliminate","tie_revote","extra_time_enabled","night_timeout","mafia_timeout","doctor_timeout","commissioner_timeout","discussion_timeout","voting_timeout","last_word_timeout","extra_time_seconds","extra_time_approval_percent"}
        if field not in allowed:raise ValueError("Unsupported game setting")
        await self.set_game_fields(game_id,**{field:value})
    async def set_group_active(self,chat_id,active):
        async with self.session() as s:
            g=await s.scalar(select(Group).where(Group.chat_id==chat_id))
            if g:g.bot_active=active;g.last_seen_at=now()
            await s.commit()

    async def cancel(self,game_id):
        async with self.session() as s:
            g=await s.get(Game,game_id)
            if not g or not g.active:return False
            g.active=False;g.phase="CANCELLED";g.finished_at=now();await s.commit();return True
    async def finish(self,game_id,winner):
        async with self.session() as s:
            g=await s.get(Game,game_id)
            if not g or not g.active:return
            g.active=False;g.phase="FINISHED";g.winner=winner;g.finished_at=now()
            rows=(await s.execute(select(Player,User).join(User,User.id==Player.user_id).where(Player.game_id==game_id))).all()
            for p,u in rows:
                u.games_played+=1; win=(winner=="MAFIA" and p.role=="mafia") or (winner=="CIVILIANS" and p.role!="mafia")
                if win:u.wins+=1
                else:u.losses+=1
                if p.role:
                    st=await s.scalar(select(UserRoleStat).where(UserRoleStat.user_id==u.id,UserRoleStat.role==p.role))
                    if not st:st=UserRoleStat(user_id=u.id,role=p.role);s.add(st)
                    st.games+=1
                    if win:st.wins+=1
                    else:st.losses+=1
            await s.commit()
    async def log(self,event,game_id=None,actor_id=None,details=None):
        async with self.session() as s:s.add(Log(game_id=game_id,actor_id=actor_id,event=event,details=details));await s.commit()
    async def recent_logs(self,limit=20):
        async with self.session() as s:return (await s.execute(select(Log).order_by(desc(Log.created_at)).limit(limit))).scalars().all()

    async def create_ticket(self,user_id,subject="Support"):
        async with self.session() as s:
            t=SupportTicket(user_id=user_id,subject=subject,status="NEW");s.add(t);await s.flush();await s.commit();return t
    async def ticket_messages(self, ticket_id, limit=20):
        async with self.session() as s:
            return (await s.execute(select(SupportMessage).where(SupportMessage.ticket_id==ticket_id).order_by(desc(SupportMessage.created_at)).limit(limit))).scalars().all()
    async def ticket(self,ticket_id):
        async with self.session() as s:return await s.scalar(select(SupportTicket).where(SupportTicket.id==ticket_id))
    async def open_user_ticket(self,user_id):
        async with self.session() as s:return await s.scalar(select(SupportTicket).where(SupportTicket.user_id==user_id,SupportTicket.status.in_(["NEW","IN_PROGRESS","WAITING_USER"])).order_by(desc(SupportTicket.id)).limit(1))
    async def add_ticket_message(self,ticket_id,sender_id,direction,content_type,text_value=None,message_id=None):
        async with self.session() as s:
            s.add(SupportMessage(ticket_id=ticket_id,sender_id=sender_id,direction=direction,content_type=content_type,text=text_value,telegram_message_id=message_id))
            t=await s.get(SupportTicket,ticket_id);t.updated_at=now()
            if direction=="user":t.status="DELIVERED"
            elif direction=="admin":t.status="WAITING_USER"
            await s.commit()
    async def assign_ticket(self,ticket_id,admin_id):
        async with self.session() as s:
            t=await s.get(SupportTicket,ticket_id)
            if not t:return False
            if t.assigned_admin_id not in (None,admin_id):return False
            t.assigned_admin_id=admin_id;t.status="IN_PROGRESS";t.updated_at=now();await s.commit();return True
    async def close_ticket(self,ticket_id):
        async with self.session() as s:
            t=await s.get(SupportTicket,ticket_id)
            if t:t.status="CLOSED";t.closed_at=now();t.updated_at=now()
            await s.commit()
    async def tickets(self,limit=30):
        async with self.session() as s:return (await s.execute(select(SupportTicket).order_by(desc(SupportTicket.updated_at)).limit(limit))).scalars().all()

    async def admin_overview(self, since=None):
        async with self.session() as s:
            def filt(stmt, col): return stmt.where(col>=since) if since else stmt
            users=await s.scalar(select(func.count(User.id)));started=await s.scalar(select(func.count(User.id)).where(User.started_bot.is_(True)));accepted=await s.scalar(select(func.count(User.id)).where(User.rules_accepted.is_(True)));blocked=await s.scalar(select(func.count(User.id)).where(User.blocked_bot.is_(True)));groups=await s.scalar(select(func.count(Group.id)).where(Group.bot_active.is_(True)));games=await s.scalar(filt(select(func.count(Game.id)),Game.created_at));active=await s.scalar(select(func.count(Game.id)).where(Game.active.is_(True)));tickets=await s.scalar(filt(select(func.count(SupportTicket.id)),SupportTicket.created_at));errors=await s.scalar(filt(select(func.count(Log.id)).where(Log.event=="ERROR"),Log.created_at));
            mafia=await s.scalar(filt(select(func.count(Game.id)).where(Game.winner=="MAFIA"),Game.finished_at));civil=await s.scalar(filt(select(func.count(Game.id)).where(Game.winner=="CIVILIANS"),Game.finished_at))
            return dict(users=users or 0,started=started or 0,accepted=accepted or 0,blocked=blocked or 0,groups=groups or 0,games=games or 0,active_games=active or 0,tickets=tickets or 0,errors=errors or 0,mafia_wins=mafia or 0,civilian_wins=civil or 0)

    async def user_card(self, telegram_id):
        async with self.session() as s:return await s.scalar(select(User).where(User.telegram_id==telegram_id))
    async def users_for_broadcast(self):
        async with self.session() as s:return (await s.execute(select(User).where(User.started_bot.is_(True),User.blocked_bot.is_(False)))).scalars().all()
    async def groups_for_broadcast(self):
        async with self.session() as s:return (await s.execute(select(Group).where(Group.bot_active.is_(True)))).scalars().all()
    async def mark_blocked(self,telegram_id,blocked=True):
        async with self.session() as s:
            u=await s.scalar(select(User).where(User.telegram_id==telegram_id))
            if u:u.blocked_bot=blocked;u.last_seen_at=now()
            await s.commit()
    async def all_group(self,chat_id):
        async with self.session() as s:return await s.scalar(select(Group).where(Group.chat_id==chat_id))
