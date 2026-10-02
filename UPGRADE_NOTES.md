# V10 Upgrade Notes

## User Bot
- Final BotFather command contract: `/start`, `/menu`, `/create`, `/join`, `/invite`, `/lobby`, `/profile`, `/stats`, `/rules`, `/support`, `/language`, `/help`.
- `/newgame` remains only as a backwards-compatible code alias and is not part of the public BotFather contract.
- Hard rules gate: all game, profile, stats, support and lobby functions are blocked until rules are accepted.
- Deep-link game invitations are also blocked until rules are accepted.
- Room code is always shown directly in the lobby.
- `/join CODE`, interactive `/join`, and personal deep-link invitations are supported.
- `/invite` sends the creator the room code and personal deep link in private chat.
- Complex buttons now expose contextual mini-guides: lobby, player count, settings, creation and joining.
- Seven roles are covered in the full rules and role guides.
- Rules remain under Telegram's 4096-character message limit in RU/UZ/EN.
- Six lightweight transparent WEBP sticker assets are bundled and sent before key UI/phase messages. Optional Telegram sticker file IDs can override them through env variables.
- Fixed night-action keyboard regression: the language parameter is now passed explicitly.
- Fixed role-setup localization placeholders.

## Admin Bot
- Added `/health` and `/help`.
- Admin commands are registered automatically on startup.
- Added explicit handler error logging and a user-facing error fallback.
- Webhook startup now verifies both User and Admin webhook registrations and logs pending updates and Telegram webhook errors.
- Added stale callback fallback so old buttons explain that the panel should be reopened.
- Ticket cancellation callback is handled correctly.
- Ticket details now show recent ticket messages and localized status labels.
- Broadcast text is sent without unsafe automatic HTML parsing.
- Logout now respects the admin allowlist.

## Verification
- `compileall`: PASS
- `tests_smoke.py`: PASS
- `tests_logic.py`: PASS
- `tests_quality.py`: PASS
- `tests_v10.py`: PASS
