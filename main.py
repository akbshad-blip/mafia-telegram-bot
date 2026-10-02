import asyncio
import logging

from config import settings, validate_settings
from database import Database
from bot.user_bot import UserBot
from bot.admin_bot import AdminBot
from game.recovery import RecoveryService

logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(name)s | %(message)s")


async def main():
    validate_settings()
    db = Database(settings.database_url)
    await db.init()
    user_bot = UserBot(db)
    admin_bot = AdminBot(db)
    recovery = RecoveryService(db, user_bot.engine)

    await user_bot.initialize()
    await admin_bot.initialize()
    await recovery.recover()

    if not settings.webhook_mode:
        try:
            await asyncio.gather(user_bot.run(), admin_bot.run())
        finally:
            await db.close()
        return

    from webhook_server import TelegramWebhookServer

    server = TelegramWebhookServer(user_bot, admin_bot)
    await user_bot.app.start()
    await admin_bot.app.start()
    await server.start()
    try:
        await asyncio.Event().wait()
    finally:
        await server.stop()
        await admin_bot.app.stop()
        await user_bot.app.stop()
        await admin_bot.app.shutdown()
        await user_bot.app.shutdown()
        await db.close()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
