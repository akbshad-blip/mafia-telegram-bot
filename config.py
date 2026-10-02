from __future__ import annotations

import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()


def env_bool(name: str, default: bool) -> bool:
    raw = os.getenv(name)
    return default if raw is None else raw.lower() in {"1", "true", "yes", "on"}


def env_int(name: str, default: int) -> int:
    try:
        return int(os.getenv(name, str(default)))
    except ValueError:
        return default


@dataclass(frozen=True)
class Settings:
    user_bot_token: str
    admin_bot_token: str
    user_bot_username: str
    admin_ids: tuple[int, ...]
    admin_password: str
    admin_contact_url: str
    database_url: str
    channel_url: str
    channel_id: str
    default_language: str
    min_players: int
    max_players: int
    ready_timeout: int
    night_timeout: int
    mafia_timeout: int
    doctor_timeout: int
    commissioner_timeout: int
    discussion_timeout: int
    voting_timeout: int
    last_word_timeout: int
    extra_time_seconds: int
    extra_time_approval_percent: int
    max_warnings: int
    lock_group: bool
    delete_forbidden_messages: bool
    doctor_self_heal: bool
    doctor_repeat_target: bool
    reveal_role_after_death: bool
    allow_skip_vote: bool
    commissioner_shoot_from_night_2: bool
    mafia_require_majority: bool
    tie_revote: bool
    webhook_mode: bool
    webhook_base_url: str
    user_webhook_path: str
    admin_webhook_path: str
    user_webhook_secret: str
    admin_webhook_secret: str
    port: int
    sticker_welcome: str
    sticker_rules: str
    sticker_lobby: str
    sticker_role: str
    sticker_night: str
    sticker_day: str


def load_settings() -> Settings:
    admin_ids = tuple(int(x.strip()) for x in os.getenv("ADMIN_IDS", "").split(",") if x.strip().lstrip("-").isdigit())
    return Settings(
        user_bot_token=os.getenv("USER_BOT_TOKEN", ""),
        admin_bot_token=os.getenv("ADMIN_BOT_TOKEN", ""),
        user_bot_username=os.getenv("USER_BOT_USERNAME", ""),
        admin_ids=admin_ids,
        admin_password=os.getenv("ADMIN_PASSWORD", ""),
        admin_contact_url=os.getenv("ADMIN_CONTACT_URL", ""),
        database_url=os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./mafia.db"),
        channel_url=os.getenv("CHANNEL_URL", ""),
        channel_id=os.getenv("CHANNEL_ID", ""),
        default_language=os.getenv("DEFAULT_LANGUAGE", "ru"),
        min_players=max(5, env_int("MIN_PLAYERS", 5)),
        max_players=min(40, max(5, env_int("MAX_PLAYERS", 40)), 40),
        ready_timeout=max(15, env_int("READY_TIMEOUT", 60)),
        night_timeout=max(30, env_int("NIGHT_TIMEOUT", 30)),
        mafia_timeout=max(30, env_int("MAFIA_TIMEOUT", 120)),
        doctor_timeout=max(20, env_int("DOCTOR_TIMEOUT", 60)),
        commissioner_timeout=max(20, env_int("COMMISSIONER_TIMEOUT", 60)),
        discussion_timeout=max(30, env_int("DISCUSSION_TIMEOUT", 120)),
        voting_timeout=max(15, env_int("VOTING_TIMEOUT", 60)),
        last_word_timeout=max(15, env_int("LAST_WORD_TIMEOUT", 30)),
        extra_time_seconds=max(30, env_int("EXTRA_TIME_SECONDS", 60)),
        extra_time_approval_percent=min(100, max(50, env_int("EXTRA_TIME_APPROVAL_PERCENT", 80))),
        max_warnings=max(0, env_int("MAX_WARNINGS", 1)),
        lock_group=env_bool("LOCK_GROUP", True),
        delete_forbidden_messages=env_bool("DELETE_FORBIDDEN_MESSAGES", True),
        doctor_self_heal=env_bool("DOCTOR_SELF_HEAL", True),
        doctor_repeat_target=env_bool("DOCTOR_REPEAT_TARGET", False),
        reveal_role_after_death=env_bool("REVEAL_ROLE_AFTER_DEATH", False),
        allow_skip_vote=env_bool("ALLOW_SKIP_VOTE", True),
        commissioner_shoot_from_night_2=env_bool("COMMISSIONER_SHOOT_FROM_NIGHT_2", True),
        mafia_require_majority=env_bool("MAFIA_REQUIRE_MAJORITY", True),
        tie_revote=env_bool("TIE_REVOTE", True),
        webhook_mode=env_bool("WEBHOOK_MODE", os.getenv("RENDER", "").lower() == "true"),
        webhook_base_url=os.getenv("WEBHOOK_BASE_URL", os.getenv("RENDER_EXTERNAL_URL", "")),
        user_webhook_path=os.getenv("USER_WEBHOOK_PATH", "/telegram/webhook/user"),
        admin_webhook_path=os.getenv("ADMIN_WEBHOOK_PATH", "/telegram/webhook/admin"),
        user_webhook_secret=os.getenv("USER_WEBHOOK_SECRET", ""),
        admin_webhook_secret=os.getenv("ADMIN_WEBHOOK_SECRET", ""),
        port=max(1, env_int("PORT", 10000)),
        sticker_welcome=os.getenv("STICKER_WELCOME", ""),
        sticker_rules=os.getenv("STICKER_RULES", ""),
        sticker_lobby=os.getenv("STICKER_LOBBY", ""),
        sticker_role=os.getenv("STICKER_ROLE", ""),
        sticker_night=os.getenv("STICKER_NIGHT", ""),
        sticker_day=os.getenv("STICKER_DAY", ""),
    )


settings = load_settings()

def validate_settings():
    missing = []
    if not settings.user_bot_token: missing.append("USER_BOT_TOKEN")
    if not settings.admin_bot_token: missing.append("ADMIN_BOT_TOKEN")
    if not settings.admin_password: missing.append("ADMIN_PASSWORD")
    if not settings.admin_ids: missing.append("ADMIN_IDS")
    if settings.webhook_mode and not settings.webhook_base_url:
        missing.append("WEBHOOK_BASE_URL (or Render's RENDER_EXTERNAL_URL)")
    if settings.webhook_mode and not settings.database_url.startswith("postgresql"):
        missing.append("DATABASE_URL must be PostgreSQL in webhook/production mode")
    if missing:
        raise RuntimeError("Missing environment variables: " + ", ".join(missing))
