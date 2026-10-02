import ast, re
from pathlib import Path
from locales import TEXT, t
from admin_locales import TEXT as ADMIN_TEXT
from game.roles import composition, validate_custom, ROLE_ORDER

# 1) Every User Bot locale has exactly the same keys.
assert set(TEXT["ru"]) == set(TEXT["uz"]) == set(TEXT["en"])
for lang in ("en", "uz"):
    for key, value in TEXT[lang].items():
        assert not re.search(r"[А-Яа-яЁё]", value), f"Cyrillic leaked into {lang}:{key}"

# 2) Every Admin Bot locale contains all English keys.
for lang in ("ru", "uz"):
    assert set(ADMIN_TEXT["en"]).issubset(ADMIN_TEXT[lang])

# 3) Role compositions are valid for every supported size.
for n in range(5, 41):
    cfg = composition(n)
    assert sum(cfg.values()) == n
    assert cfg["mafia"] >= 1 and cfg["doctor"] == 1 and cfg["civilian"] >= 1
    validate_custom(n, cfg["mafia"], 1, cfg["commissioner"], cfg["lover"], cfg["detective"], cfg["bodyguard"])

# Commissioner can be removed while Mafia and Doctor remain mandatory.
cfg = validate_custom(10, 2, 1, 0, 1, 1, 0)
assert cfg["commissioner"] == 0 and cfg["doctor"] == 1 and cfg["mafia"] == 2

# 4) No bundled runtime artwork / bytecode belongs in production ZIP.
files = [p for p in Path('.').rglob('*') if p.is_file()]
assert not any(p.suffix.lower() in {'.png','.jpg','.jpeg','.gif','.mp4','.webm','.tgs'} for p in files)
assert all(p.suffix.lower() == '.webp' for p in files if 'assets/stickers' in str(p).replace('\\','/'))
# Production packaging check is performed immediately before ZIP creation; Python may create caches while tests run.

# 5) Critical user-facing hard-coded English labels are not present in source.
source = Path('bot/user_bot.py').read_text(encoding='utf-8') + Path('game/engine.py').read_text(encoding='utf-8')
for bad in ('Mafia Chat', 'Auto balance'):
    assert bad not in source

print('QUALITY TESTS: PASS')
