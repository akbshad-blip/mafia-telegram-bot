from __future__ import annotations
import secrets

# Core roles are mandatory: at least one Mafia and exactly one Doctor.
# Other roles are optional and can be enabled/disabled by the lobby creator.
ROLE_INFO = {
    "mafia": "role_mafia",
    "doctor": "role_doctor",
    "commissioner": "role_commissioner",
    "lover": "role_lover",
    "detective": "role_detective",
    "bodyguard": "role_bodyguard",
    "civilian": "role_civilian",
}

ROLE_ORDER = ["mafia", "doctor", "commissioner", "lover", "detective", "bodyguard", "civilian"]


def mafia_count_for(n: int) -> int:
    if not 5 <= n <= 40:
        raise ValueError("player count must be 5..40")
    if n <= 6: return 1
    if n <= 9: return 2
    if n <= 14: return 3
    if n <= 17: return 4
    if n <= 20: return 5
    return max(6, min(9, (n - 1) // 4))


def composition(n: int, mafia: int | None = None, doctor: int = 1,
                commissioner: int | None = None, lover: int | None = None,
                detective: int | None = None, bodyguard: int | None = None) -> dict[str, int]:
    if not 5 <= n <= 40:
        raise ValueError("player count must be 5..40")
    mafia = mafia_count_for(n) if mafia is None else mafia
    if commissioner is None: commissioner = 1
    if lover is None: lover = 1 if n >= 7 else 0
    if detective is None: detective = 1 if n >= 10 else 0
    if bodyguard is None: bodyguard = 1 if n >= 15 else 0
    if mafia < 1 or doctor != 1 or min(commissioner, lover, detective, bodyguard) < 0:
        raise ValueError("invalid role counts")
    used = mafia + doctor + commissioner + lover + detective + bodyguard
    civilians = n - used
    if civilians < 1:
        raise ValueError("at least one civilian is required")
    if mafia >= n - mafia:
        raise ValueError("Mafia cannot be a majority at game start")
    return {
        "mafia": mafia, "doctor": doctor, "commissioner": commissioner,
        "lover": lover, "detective": detective, "bodyguard": bodyguard,
        "civilian": civilians,
    }


def validate_custom(n: int, mafia: int, doctor: int, commissioner: int, lover: int = 0, detective: int = 0, bodyguard: int = 0) -> dict[str, int]:
    cfg = composition(n, mafia, doctor, commissioner, lover, detective, bodyguard)
    if sum(cfg.values()) != n:
        raise ValueError("role count does not match players")
    return cfg


def assign_roles(player_ids: list[int], config: dict[str, int] | None = None) -> dict[int, str]:
    cfg = config or composition(len(player_ids))
    roles: list[str] = []
    for role in ROLE_ORDER:
        roles.extend([role] * int(cfg.get(role, 0)))
    if len(roles) != len(player_ids):
        raise ValueError("role count does not match players")
    ids = list(player_ids)
    rng = secrets.SystemRandom()
    rng.shuffle(ids)
    rng.shuffle(roles)
    return dict(zip(ids, roles))
