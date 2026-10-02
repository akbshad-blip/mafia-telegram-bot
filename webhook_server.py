from __future__ import annotations

import asyncio
import logging
import os
import secrets
from contextlib import suppress

from aiohttp import web
from telegram import Update

from config import settings

log = logging.getLogger(__name__)


class TelegramWebhookServer:
    """One Render HTTP service that receives webhooks for both project bots.

    Telegram sends each bot to a different route. The handler validates Telegram's
    X-Telegram-Bot-Api-Secret-Token header and pushes the decoded Update into the
    corresponding python-telegram-bot Application queue.
    """

    def __init__(self, user_bot, admin_bot):
        self.user_bot = user_bot
        self.admin_bot = admin_bot
        self.user_secret = settings.user_webhook_secret or secrets.token_hex(32)
        self.admin_secret = settings.admin_webhook_secret or secrets.token_hex(32)
        self.base_url = settings.webhook_base_url.rstrip("/")
        self.port = settings.port
        self.runner: web.AppRunner | None = None
        self.site: web.TCPSite | None = None

    @staticmethod
    async def _health(request: web.Request) -> web.Response:
        return web.json_response({"status": "ok", "service": "mafia-telegram-bot"})

    async def _receive(self, request: web.Request, application, expected_secret: str) -> web.Response:
        supplied = request.headers.get("X-Telegram-Bot-Api-Secret-Token", "")
        if not secrets.compare_digest(supplied, expected_secret):
            return web.Response(status=403, text="Forbidden")

        try:
            data = await request.json()
            update = Update.de_json(data=data, bot=application.bot)
            if update is None:
                return web.Response(status=400, text="Invalid Telegram update")
            await application.update_queue.put(update)
            return web.Response(status=200, text="OK")
        except Exception:
            log.exception("Failed to accept Telegram webhook update")
            return web.Response(status=400, text="Bad Request")

    async def _user(self, request: web.Request) -> web.Response:
        return await self._receive(request, self.user_bot.app, self.user_secret)

    async def _admin(self, request: web.Request) -> web.Response:
        return await self._receive(request, self.admin_bot.app, self.admin_secret)

    async def start(self) -> None:
        if not self.base_url:
            raise RuntimeError(
                "WEBHOOK_BASE_URL is required in webhook mode. "
                "On Render it is normally supplied automatically by RENDER_EXTERNAL_URL."
            )

        app = web.Application(client_max_size=2 * 1024 * 1024)
        app.router.add_get("/health", self._health)
        app.router.add_post(settings.user_webhook_path, self._user)
        app.router.add_post(settings.admin_webhook_path, self._admin)

        self.runner = web.AppRunner(app, access_log=None)
        await self.runner.setup()
        self.site = web.TCPSite(self.runner, "0.0.0.0", self.port)
        await self.site.start()

        await self.user_bot.app.bot.set_webhook(
            url=f"{self.base_url}{settings.user_webhook_path}",
            allowed_updates=Update.ALL_TYPES,
            drop_pending_updates=False,
            secret_token=self.user_secret,
            max_connections=40,
        )
        await self.admin_bot.app.bot.set_webhook(
            url=f"{self.base_url}{settings.admin_webhook_path}",
            allowed_updates=Update.ALL_TYPES,
            drop_pending_updates=False,
            secret_token=self.admin_secret,
            max_connections=40,
        )
        # Verify both registrations immediately. This makes a broken Admin webhook
        # visible in Render logs instead of silently looking like a dead bot.
        user_info = await self.user_bot.app.bot.get_webhook_info()
        admin_info = await self.admin_bot.app.bot.get_webhook_info()
        log.info("Webhook server listening on 0.0.0.0:%s", self.port)
        log.info("User webhook: %s%s | pending=%s | error=%s", self.base_url, settings.user_webhook_path, user_info.pending_update_count, user_info.last_error_message or "none")
        log.info("Admin webhook: %s%s | pending=%s | error=%s", self.base_url, settings.admin_webhook_path, admin_info.pending_update_count, admin_info.last_error_message or "none")

    async def stop(self) -> None:
        # Do not delete the Telegram webhooks during normal shutdown. Keeping them
        # registered lets Telegram retain/retry pending updates while Render restarts.
        if self.runner is not None:
            with suppress(Exception):
                await self.runner.cleanup()
        self.runner = None
        self.site = None
