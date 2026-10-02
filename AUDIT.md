# V10 Audit Summary

## High-priority fixes
1. Rules were not a universal gate: deep-link joins and several group commands could bypass the intended onboarding state. V10 blocks them until `rules_accepted=true`.
2. Lobby code visibility was improved: the room code is now always in the lobby message.
3. Contextual instructions were added for non-obvious controls.
4. Rules were expanded to cover all seven roles while staying under 4096 characters in all three languages.
5. Night-action keyboard had an undefined `lang` reference in `GameEngine.target_keyboard`; V10 passes the language explicitly.
6. Role composition text expected the wrong template variables; V10 aligns the template with the actual call signature.
7. Admin Bot now has explicit health diagnostics, error handling, command registration and webhook verification logs.
8. Admin ticket UI now handles reply cancellation and displays recent messages.

## Static verification
All V10 tests pass.

## Live verification limitation
A live Telegram -> Render -> Supabase test still requires deployment with the user's real BotFather tokens and production environment. The codebase does not claim that live test as completed.
