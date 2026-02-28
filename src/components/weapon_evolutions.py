"""
DARK SANCTUM - Weapon Evolution Definitions
Matrix Team: Game Designer + Developer

Vampire Survivors-style weapon evolutions for max-level weapons
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class EvolutionData:
    """Definition for evolved weapon"""
    base_weapon_id: str  # The weapon that evolves
    evolved_id: str  # ID of evolved form
    evolved_name: str
    evolved_description: str
    evolved_icon: str

    # Evolved stats (typically 2-3x base stats)
    damage_multiplier: float
    cooldown_multiplier: float  # Lower = faster
    range_multiplier: float
    projectile_multiplier: int  # Additional projectiles

    # Visual
    evolved_color: tuple[int, int, int]

    # Special mechanics (optional)
    special_effect: Optional[str] = None  # "pierce", "chain", "immunity", etc.


# === WEAPON EVOLUTIONS ===

SWORD_EVOLUTION = EvolutionData(
    base_weapon_id="sword",
    evolved_id="reapers_embrace",
    evolved_name="Reaper's Embrace",
    evolved_description="Massive scythe storm that obliterates everything nearby",
    evolved_icon="💀",
    damage_multiplier=3.0,  # 70 → 210 damage at max
    cooldown_multiplier=0.5,  # 0.7s → 0.35s
    range_multiplier=2.0,  # 150 → 300 range
    projectile_multiplier=3,  # 3 → 6 scythes
    evolved_color=(60, 10, 80),  # Deeper purple/black
    special_effect="lifesteal"  # Heals 10% of damage dealt
)

MAGIC_MISSILE_EVOLUTION = EvolutionData(
    base_weapon_id="magic_missile",
    evolved_id="cosmic_annihilation",
    evolved_name="Cosmic Annihilation",
    evolved_description="Unleashes a devastating barrage of cosmic projectiles",
    evolved_icon="🌌",
    damage_multiplier=2.5,  # 50 → 125 damage
    cooldown_multiplier=0.6,  # 1.0s → 0.6s
    range_multiplier=1.5,  # 600 → 900 range
    projectile_multiplier=5,  # 5 → 10 missiles
    evolved_color=(200, 100, 255),  # Brighter cosmic purple
    special_effect="split"  # Each missile splits into 2 on hit
)

GARLIC_EVOLUTION = EvolutionData(
    base_weapon_id="garlic",
    evolved_id="sacred_ward",
    evolved_name="Sacred Ward",
    evolved_description="Holy barrier that damages enemies and grants brief invulnerability",
    evolved_icon="✨",
    damage_multiplier=4.0,  # 28 → 112 DPS
    cooldown_multiplier=1.0,  # Same tick rate
    range_multiplier=2.5,  # 150 → 375 range (massive aura)
    projectile_multiplier=0,  # Still 1 aura
    evolved_color=(255, 255, 200),  # Bright golden
    special_effect="immunity"  # Player immune while in aura
)

# === SPRINT 14 EVOLUTIONS ===

LIGHTNING_EVOLUTION = EvolutionData(
    base_weapon_id="lightning",
    evolved_id="storm_bringer",
    evolved_name="Storm Bringer",
    evolved_description="Apocalyptic lightning storm that chains infinitely",
    evolved_icon="⚡",
    damage_multiplier=2.8,  # 90 → 252 damage
    cooldown_multiplier=0.4,  # 1.5s → 0.6s (extremely fast)
    range_multiplier=2.0,  # 400 → 800 range
    projectile_multiplier=3,  # 2 → 5 simultaneous chains
    evolved_color=(255, 255, 50),  # Bright electric yellow
    special_effect="infinite_chain"  # Chains never stop (within range)
)

FROST_NOVA_EVOLUTION = EvolutionData(
    base_weapon_id="frost_nova",
    evolved_id="absolute_zero",
    evolved_name="Absolute Zero",
    evolved_description="Freezing blizzard that completely stops enemies in their tracks",
    evolved_icon="❄️",
    damage_multiplier=3.2,  # 50 → 160 damage
    cooldown_multiplier=0.5,  # 1.4s → 0.7s
    range_multiplier=1.8,  # 500 → 900 range
    projectile_multiplier=5,  # 5 → 10 projectiles
    evolved_color=(150, 230, 255),  # Bright ice blue
    special_effect="freeze"  # Enemies frozen for 2s on hit
)


# Evolution registry
WEAPON_EVOLUTIONS = {
    "sword": SWORD_EVOLUTION,
    "magic_missile": MAGIC_MISSILE_EVOLUTION,
    "garlic": GARLIC_EVOLUTION,
    # Sprint 14 evolutions
    "lightning": LIGHTNING_EVOLUTION,
    "frost_nova": FROST_NOVA_EVOLUTION,
}


def get_evolution(weapon_id: str) -> Optional[EvolutionData]:
    """Get evolution data for a weapon"""
    return WEAPON_EVOLUTIONS.get(weapon_id)


def can_evolve(weapon_id: str) -> bool:
    """Check if weapon has an evolution available"""
    return weapon_id in WEAPON_EVOLUTIONS


# === GAME DESIGNER NOTE ===
# Weapon evolutions are the "endgame" power fantasy:
#
# SPRINT 12 EVOLUTIONS (3):
# - Reaper's Embrace (Sword): Melee DPS king, sustain through lifesteal
# - Cosmic Annihilation (Magic Missile): Screen-clearing ranged destruction
# - Sacred Ward (Garlic): Tank build enabler with immunity
#
# SPRINT 14 EVOLUTIONS (2):
# - Storm Bringer (Lightning): Infinite chain lightning, ultimate crowd control
# - Absolute Zero (Frost Nova): Freezing blizzard, complete enemy lockdown
#
# Total: 5 evolutions (out of 13 base weapons)
# Each evolution fundamentally changes playstyle and enables new builds!
