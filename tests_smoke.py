import asyncio
from pathlib import Path
from game.roles import composition
from locales import TEXT

async def main():
    assert Path("main.py").exists()
    assert sum(composition(10).values())==10
    assert set(TEXT["ru"])==set(TEXT["uz"])==set(TEXT["en"])
    print("SMOKE TEST: PASS")
asyncio.run(main())
