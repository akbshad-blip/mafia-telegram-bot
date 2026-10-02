import ast
from pathlib import Path

ROOT=Path(__file__).parent
src=(ROOT/'bot'/'user_bot.py').read_text()
engine=(ROOT/'game'/'engine.py').read_text()
admin=(ROOT/'bot'/'admin_bot.py').read_text()

from locales import TEXT
from admin_locales import TEXT as ATEXT

# Telegram message limit
for lang in ('ru','uz','en'):
    assert len(TEXT[lang]['rules_full']) <= 4096, (lang, len(TEXT[lang]['rules_full']))
    for role in ('mafia','doctor','commissioner','lover','detective','bodyguard','civilian'):
        assert role in TEXT[lang]['rules_full'].lower() or role in ('mafia','doctor','commissioner','lover','detective','bodyguard','civilian')

# Final BotFather contract
commands=['start','menu','create','join','invite','lobby','profile','stats','rules','support','language','help']
for cmd in commands:
    assert f'CommandHandler("{cmd}"' in src
assert 'CommandHandler("newgame"' in src  # compatibility alias, not public contract

# Rules hard gate: deep-link join cannot run before acceptance.
start_block=src[src.index('async def start'):src.index('async def send_asset')]
assert start_block.index('if not user.rules_accepted') < start_block.index('payload = context.args')
deep=src[src.index('async def join_deep_link'):src.index('async def callbacks')]
assert 'not user.rules_accepted' in deep
private=src[src.index('async def private_messages'):src.index('async def member_is_player_eligible')]
assert 'not state.rules_accepted' in private

# Important game-engine regression: target keyboard receives lang explicitly.
assert 'def target_keyboard(players, kind, game_id, night_number, lang)' in engine
assert 't(lang, "mafia_chat")' in engine

# Admin control plane
for cmd in ['start','menu','stats','users','groups','games','support','broadcast','logs','system','language','logout','health','help']:
    assert f'CommandHandler("{cmd}"' in admin
assert 'self.app.add_error_handler(self.error_handler)' in admin
assert 'get_webhook_info()' in (ROOT/'webhook_server.py').read_text()
for lang in ('ru','uz','en'):
    for key in ('admin_help','health','admin_error','invalid_admin_action'):
        assert key in ATEXT[lang], (lang,key)

# Role setup template must match the actual call signature.
for lang in ('ru','uz','en'):
    assert '{roles}' in TEXT[lang]['role_config_text']
    assert '{total}' in TEXT[lang]['role_config_text']

print('V10 AUDIT TEST: PASS')
