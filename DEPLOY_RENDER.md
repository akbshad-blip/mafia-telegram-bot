# Render + Supabase production setup

## Architecture

- Render Web Service runs both Telegram bots in one Python process.
- Telegram sends User Bot and Admin Bot updates to two separate webhook paths.
- Supabase PostgreSQL stores all persistent application data.
- Render's local filesystem is not used for the database.

## Render settings

Build Command:

```text
pip install -r requirements-postgres.txt
```

Start Command:

```text
python main.py
```

Health Check Path:

```text
/health
```

`WEBHOOK_MODE=true` is required in production. `RENDER_EXTERNAL_URL` is used automatically as the webhook base URL, so do not hardcode the Render URL in the repository.

## Required environment variables

```text
USER_BOT_TOKEN
ADMIN_BOT_TOKEN
ADMIN_IDS
ADMIN_PASSWORD
DATABASE_URL
USER_BOT_USERNAME
WEBHOOK_MODE=true
```

The app also reads `RENDER_EXTERNAL_URL` automatically from Render. `PORT` is read automatically from Render's `PORT` variable and defaults to 10000.

## Important persistence behavior

- `drop_pending_updates=False` is intentional. A normal restart/redeploy does not ask Telegram to discard pending updates.
- Telegram webhooks remain registered during normal process shutdown. This allows Telegram to retry delivery while Render restarts the service.
- Game/user/statistics/support data is stored in PostgreSQL, not on Render's local disk.
- If a service is down longer than Telegram's update retention window, old undelivered Telegram updates can no longer be recovered from Telegram. Database records already committed before the outage remain in PostgreSQL.

## Never commit

Do not commit `.env`, bot tokens, admin password, database passwords, or webhook secrets. Use Render Environment Variables.
