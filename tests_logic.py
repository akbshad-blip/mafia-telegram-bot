import ast
from pathlib import Path
from game.roles import composition, validate_custom, mafia_count_for
from locales import TEXT, t

for n in range(5, 41):
    roles=composition(n)
    assert sum(roles.values())==n
    assert roles["doctor"]==1 and roles["commissioner"]==1 and roles["civilian"]>=1
    assert roles["mafia"]==mafia_count_for(n)
assert validate_custom(10,3,1,1)["civilian"]==5

source=Path(__file__).with_name("game")/"engine.py"
tree=ast.parse(source.read_text(encoding="utf-8")); cls=next(n for n in tree.body if isinstance(n,ast.ClassDef) and n.name=="GameEngine"); method=next(n for n in cls.body if isinstance(n,ast.FunctionDef) and n.name=="_mafia_target")
ns={"Counter":__import__("collections").Counter};exec(compile(ast.Module(body=[method],type_ignores=[]),str(source),"exec"),ns)
mafia_target=ns["_mafia_target"]
class A:
    def __init__(self,target_user_id):self.target_user_id=target_user_id
assert mafia_target([A(10)],[10,20],1)==(10,True)
assert mafia_target([A(10),A(10)],[10,20],2)==(10,True)
assert mafia_target([A(10),A(20),A(10)],[10,20,30],3)==(10,False)
assert mafia_target([A(10),A(20)],[10,20],2)==(None,False)

base=set(TEXT["ru"])
for lang in ("ru","uz","en"):
    assert base==set(TEXT[lang]),(lang,base-set(TEXT[lang]),set(TEXT[lang])-base)
    assert t(lang,"lobby_v2",count=5,max=10,players="1. Test",roles="2/1/1/1",game_id=1,code="ABC123")
print("LOGIC TESTS: PASS")
