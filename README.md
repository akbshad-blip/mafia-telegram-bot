# Mafia Telegram Bot — Final Build

Two Telegram bots share one authoritative SQL database:

- **User Bot** — onboarding, language/rules gate, profiles, statistics, lobby, role distribution, private actions, Mafia coordination, moderation and support tickets.
- **Admin Bot** — Telegram-ID allowlist, password authentication, dashboard, period statistics, user/group cards, ticket ownership, logs and confirmed broadcasts.
- **Languages** — RU / UZ / EN.
- **Database** — SQLite locally; PostgreSQL + asyncpg for production.

## User onboarding

`/start` → Telegram display name is stored as the profile name → language → full rules → explicit acceptance → main menu. The menu contains Create Game, Join Game, My Profile, My Statistics, Rules, Support and Language.

## Creating a game

1. In the target group, add User Bot as an administrator.
2. Give it **delete messages** and **restrict members** permissions.
3. Send `/newgame`.
4. The bot checks its permissions before creating the lobby. If a required permission is missing, it reports the missing permission and does not start the game.
5. Lobby size can be selected from 5–40, including presets and a custom count.
6. Automatic role balance is the default. The creator can choose Doctor self-save ×1 or ×2 and other safe game settings.

The production UI is intentionally text-only: no bundled photos, stickers or phase artwork are sent by the User Bot. **How to add bot** is delivered as a localized text guide.

## Starting role balance

The automatic composition is a starting balance, not a rigid rule. Core roles only: Mafia, Doctor, Commissioner and Civilian. One Doctor and one Commissioner are used by default; Mafia scales with player count.

- 5–6: 1 Mafia / 1 Doctor / 1 Commissioner / civilians
- 7–9: 2 Mafia / 1 Doctor / 1 Commissioner / civilians
- 10–14: 3 Mafia / 1 Doctor / 1 Commissioner / civilians
- 15–17: 4 Mafia / 1 Doctor / 1 Commissioner / civilians
- 18–20: 5 Mafia / 1 Doctor / 1 Commissioner / civilians
- 21–40: automatic scaling continues within the safe 1–9 Mafia range.

## Night

- Night group messages are moderated/removed.
- Civilian receives a private informational message and has no night action.
- Mafia receives the other Mafia members' names/usernames and chooses one shared target.
- When a Mafia player chooses a target, partners receive a private proposal and can select the same target or another one.
- If all active Mafia select the same target and Doctor/Commissioner required actions are already submitted, the night resolves early.
- If not all Mafia choose, the timeout resolver uses the strongest proposal. If several proposals tie, the attack is cancelled. If one Mafia proposed a target and another never acted, the proposed target can resolve.
- Mafia Chat is private, available only to Mafia during the night; one message is sent per chat submission and it is copied only to Mafia teammates.
- Doctor protects one living player. Self-save is configurable ×1 or ×2. Doctor protection can prevent both Mafia and Commissioner night elimination.
- Commissioner checks one living player every night. The result is immediate. From night 2, an additional elimination action is available. The Commissioner cannot target themself.

Default windows: Mafia 120s, Doctor 60s, Commissioner 60s, discussion 120s, voting 60s, last word 30s.

## Day and voting

- Discussion is 2 minutes by default. Living players can speak normally; dead players are restricted from discussion.
- Voting is private with inline buttons and lasts 1 minute by default.
- Only living players can vote. Self-voting is blocked. Votes can be changed until the timer expires.
- Skip is configurable. Ties can trigger one restricted revote.

## Death and roles

During the game, eliminated players do **not** reveal their role. They receive one 30-second last-word window, then become spectators. All roles are revealed only in the final result.

## Victory and statistics

- Civilians win when Mafia = 0.
- Mafia wins when Mafia >= all other living players.
- Every player receives exactly one win or loss for a finished game.
- Per-role statistics are stored separately from global statistics.

## Support

User Bot support contains New Ticket, My Ticket, FAQ and Contact Administrator. A ticket can contain text, photo, document, audio, voice or video. The ticket is delivered to admins; one admin can claim it and becomes the sole owner. That admin can reply with the same media types or close the ticket.

`ADMIN_CONTACT_URL` controls the direct administrator button.

## Admin Bot

1. `/start`
2. Telegram ID must be in `ADMIN_IDS`.
3. Password is requested only after the ID check.
4. Password message is deleted immediately.
5. Successful and failed logins are logged. Five failures cause a five-minute lock.
6. Dashboard includes users, rules accepted, blocked users, active groups, games, winners, tickets and errors.
7. Statistics support today / 7 days / current month / current year / all time.
8. User cards expose Telegram ID, username, display name, language, first start, last seen, rules timestamp, game statistics and blocked state.
9. Group cards show registered active groups and game counts.
10. Broadcasts support text/photo/document/audio/voice/video, all users, all groups, selected user or selected group. A preview, recipient count and confirmation are required before sending. Delivery failures mark blocked users or inactive groups.

## Logging

Important events are stored with timestamp, actor ID, game ID where relevant, event name and details: registration, rules acceptance, game creation/join/leave/start, role distribution, tickets, admin login/lock/logout, broadcasts and errors.

## Local setup

```powershell
python -m pip install -r requirements.txt
python main.py
```

For PostgreSQL:

```powershell
python -m pip install -r requirements-postgres.txt
```

Then configure `DATABASE_URL=postgresql+asyncpg://...`.

A live Telegram integration test still requires real tokens, a real group and real Telegram permissions. This package does not claim those external conditions were tested.

## Production deployment on Render

The production build is prepared for a Render Web Service using Telegram webhooks.
Both bots share one HTTP service and use separate webhook routes:

- `/telegram/webhook/user`
- `/telegram/webhook/admin`

The service also exposes `/health` for Render health checks.

Render supplies `RENDER_EXTERNAL_URL` automatically; the application uses it as the
webhook base URL. `PORT` is read from Render and defaults to `10000`.

Production must use PostgreSQL. `database.py` normalizes common `postgresql://` and
`postgres://` URLs to SQLAlchemy's `postgresql+asyncpg://` dialect and translates
`sslmode=require` to asyncpg's SSL setting.

Webhook delivery intentionally uses `drop_pending_updates=False`, so normal restarts
do not ask Telegram to discard pending updates. The service also does not delete the
webhook during normal shutdown. Persistent user/game/support/statistics data is stored
in PostgreSQL, not on Render's local filesystem.

See `DEPLOY_RENDER.md` for the deployment checklist.

## BotFather command contract (v9)

Configure these public User Bot commands in BotFather:

```text
start - Запустить бота
menu - Открыть главное меню
create - Создать игру в группе
join - Войти в игру по коду
invite - Получить код и ссылку приглашения
lobby - Показать лобби группы
profile - Мой профиль
stats - Моя статистика
rules - Правила игры
support - Поддержка
language - Изменить язык
help - Помощь
```

`/newgame` remains a backward-compatible internal alias for `/create` and should not be added to the public BotFather list.

### Lobby/join flow

1. Creator opens the User Bot in private chat, presses Start, selects a language and accepts the rules.
2. Creator adds the User Bot as an administrator in the game group and sends `/create`.
3. The lobby message visibly contains the generated room code.
4. Creator can press Invite or send `/invite`; the bot sends the room code and a personal deep link to the creator's private chat.
5. A player can join by opening the deep link, pressing Start, or by using `/join ROOMCODE` in private chat.
6. `/join` without an argument asks the player for the code. Sending the code as the next message also works.
7. `/lobby` refreshes the active lobby in the current group.


## V10 UX contract

### User Bot public commands
`/start`, `/menu`, `/create`, `/join`, `/invite`, `/lobby`, `/profile`, `/stats`, `/rules`, `/support`, `/language`, `/help`.

`/newgame` is retained only as a backwards-compatible internal alias.

### Rules gate
No game or account function is available until the user selects a language, reads the rules and presses **Accept rules**. This also applies to deep-link invitations.

### Room entry
A lobby always displays its room code. Players can join with `/join CODE`, by sending the code after pressing **Join game**, or through a personal invitation deep link.

### Contextual instructions
Non-obvious lobby controls include an `How it works` action with a short explanation and examples. Role setup has per-role descriptions.

### Visual UI
The production UI uses text, emoji and six bundled transparent WEBP sticker assets. No photos or video artwork are bundled.

### Admin Bot diagnostics
Admin Bot provides `/health`. Render startup logs verify both Telegram webhook registrations and report pending updates / Telegram webhook errors.
