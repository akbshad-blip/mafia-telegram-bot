from __future__ import annotations

from datetime import datetime, timezone
from sqlalchemy import select

from database import Game


class RecoveryService:
    def __init__(self, db, engine):
        self.db = db
        self.engine = engine

    async def recover(self):
        async with self.db.session() as s:
            q = await s.execute(select(Game).where(Game.active.is_(True)))
            games = q.scalars().all()
        now = datetime.now(timezone.utc)
        for game in games:
            if game.phase == "ROLE_DISTRIBUTION":
                await self.engine.recover_role_distribution(game.id)
                continue
            if not game.phase_ends_at:
                continue
            if game.phase_ends_at <= now:
                mapping = {
                    "READY_CHECK": self.engine.ready_check,
                    "NIGHT": self.engine.resolve_night,
                    "DISCUSSION": self.engine.start_voting,
                    "EXTRA_TIME": self.engine.resolve_extra_time,
                    "VOTING": self.engine.resolve_vote,
                    "VOTING_REVOTE": self.engine.resolve_revote,
                    "LAST_WORD": self.engine.finish_last_word,
                }
                callback = mapping.get(game.phase)
                if callback:
                    await callback(game.id)
            else:
                remaining = max(1, int((game.phase_ends_at - now).total_seconds()))
                mapping = {
                    "READY_CHECK": self.engine.ready_check,
                    "NIGHT": self.engine.resolve_night,
                    "DISCUSSION": self.engine.start_voting,
                    "EXTRA_TIME": self.engine.resolve_extra_time,
                    "VOTING": self.engine.resolve_vote,
                    "VOTING_REVOTE": self.engine.resolve_revote,
                    "LAST_WORD": self.engine.finish_last_word,
                }
                callback = mapping.get(game.phase)
                if callback:
                    await self.engine.schedule(game.id, callback, remaining)
