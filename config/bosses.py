"""
DARK SANCTUM - Boss Definitions
Matrix Team: Game Designer + Technical Director

Sprint 15: Boss variety with unique mechanics
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class BossData:
    """Boss definition"""
    id: str
    name: str
    description: str
    icon: str

    # Stats multipliers (vs regular enemies)
    health_multiplier: float
    damage_multiplier: float
    speed_multiplier: float
    size_multiplier: float

    # Visual
    color: tuple[int, int, int]
    glow_color: tuple[int, int, int]

    # Mechanics
    special_ability: Optional[str] = None  # "teleport", "summon", "shield", "rage"
    ability_description: str = ""

    # Loot
    xp_multiplier: float = 10.0  # How much XP boss gives
    guaranteed_powerup: bool = True  # Always drops power-up


# === BOSS DEFINITIONS ===

BLOOD_TITAN = BossData(
    id="blood_titan",
    name="Blood Titan",
    description="Massive crimson juggernaut that crushes everything in its path",
    icon="💀",
    health_multiplier=10.0,
    damage_multiplier=2.0,
    speed_multiplier=0.6,
    size_multiplier=2.0,
    color=(120, 20, 30),  # Dark blood red
    glow_color=(200, 30, 30),  # Blood red glow
    special_ability=None,  # Original boss, no special mechanics
    xp_multiplier=10.0,
    guaranteed_powerup=True
)

VOID_REAVER = BossData(
    id="void_reaver",
    name="Void Reaver",
    description="Shadowy assassin that teleports around the battlefield",
    icon="👤",
    health_multiplier=6.0,  # Less HP but harder to hit
    damage_multiplier=3.0,  # High damage
    speed_multiplier=1.2,  # Fast
    size_multiplier=1.5,
    color=(20, 10, 40),  # Deep void purple
    glow_color=(80, 40, 120),  # Purple glow
    special_ability="teleport",
    ability_description="Teleports every 3 seconds, becomes invulnerable briefly",
    xp_multiplier=12.0,  # More XP for difficulty
    guaranteed_powerup=True
)

FROST_COLOSSUS = BossData(
    id="frost_colossus",
    name="Frost Colossus",
    description="Frozen giant that slows everything around it",
    icon="❄️",
    health_multiplier=15.0,  # Tankiest boss
    damage_multiplier=1.5,
    speed_multiplier=0.4,  # Very slow
    size_multiplier=2.5,  # Huge
    color=(40, 80, 120),  # Ice blue
    glow_color=(100, 200, 255),  # Bright ice glow
    special_ability="aura_slow",
    ability_description="Slows all nearby players by 50% (300px radius)",
    xp_multiplier=15.0,
    guaranteed_powerup=True
)

PLAGUE_HERALD = BossData(
    id="plague_herald",
    name="Plague Herald",
    description="Toxic horror that summons lesser minions",
    icon="☠️",
    health_multiplier=8.0,
    damage_multiplier=1.8,
    speed_multiplier=0.7,
    size_multiplier=1.8,
    color=(60, 100, 40),  # Sickly green
    glow_color=(120, 200, 80),  # Toxic green glow
    special_ability="summon",
    ability_description="Summons 3 Imps every 5 seconds",
    xp_multiplier=10.0,
    guaranteed_powerup=True
)

INFERNO_LORD = BossData(
    id="inferno_lord",
    name="Inferno Lord",
    description="Burning demon with an enrage mechanic",
    icon="🔥",
    health_multiplier=12.0,
    damage_multiplier=2.5,
    speed_multiplier=0.8,
    size_multiplier=2.2,
    color=(150, 40, 10),  # Burning orange
    glow_color=(255, 100, 20),  # Fire glow
    special_ability="rage",
    ability_description="Gains 50% damage and speed when below 30% HP",
    xp_multiplier=12.0,
    guaranteed_powerup=True
)


# All bosses (Blood Titan is always first for wave 5)
ALL_BOSSES = [BLOOD_TITAN, VOID_REAVER, FROST_COLOSSUS, PLAGUE_HERALD, INFERNO_LORD]

# Boss rotation (which boss spawns on which boss wave)
# Wave 5 = Blood Titan (first boss)
# Wave 10 = Void Reaver
# Wave 15 = Frost Colossus
# Wave 20 = Plague Herald
# Wave 25+ = Inferno Lord (repeating)
BOSS_ROTATION = {
    1: BLOOD_TITAN,      # Wave 5
    2: VOID_REAVER,      # Wave 10
    3: FROST_COLOSSUS,   # Wave 15
    4: PLAGUE_HERALD,    # Wave 20
    5: INFERNO_LORD,     # Wave 25+
}


def get_boss_for_wave(boss_wave_number: int) -> BossData:
    """Get which boss to spawn based on boss wave number

    Args:
        boss_wave_number: 1 for first boss (wave 5), 2 for second (wave 10), etc.
    """
    if boss_wave_number in BOSS_ROTATION:
        return BOSS_ROTATION[boss_wave_number]
    else:
        # After all bosses, rotate through them (excluding Blood Titan)
        rotation_bosses = [VOID_REAVER, FROST_COLOSSUS, PLAGUE_HERALD, INFERNO_LORD]
        index = (boss_wave_number - 2) % len(rotation_bosses)  # Start from wave 2 pattern
        return rotation_bosses[index]


# === GAME DESIGNER NOTE ===
# Boss variety creates different challenges:
# - Blood Titan: Classic tank test, slow but unstoppable
# - Void Reaver: DPS check, need to burst before teleport
# - Frost Colossus: Positioning challenge, can't escape
# - Plague Herald: Add management, kill minions or boss?
# - Inferno Lord: Endurance test, dangerous when low
#
# Each boss requires different strategy!
# Sprint 15: 5 total boss types (was 1)
