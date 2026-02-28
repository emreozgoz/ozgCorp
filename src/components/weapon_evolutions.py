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


# Evolution registry
WEAPON_EVOLUTIONS = {
    "sword": SWORD_EVOLUTION,
    "magic_missile": MAGIC_MISSILE_EVOLUTION,
    "garlic": GARLIC_EVOLUTION,
}


def get_evolution(weapon_id: str) -> Optional[EvolutionData]:
    """Get evolution data for a weapon"""
    return WEAPON_EVOLUTIONS.get(weapon_id)


def can_evolve(weapon_id: str) -> bool:
    """Check if weapon has an evolution available"""
    return weapon_id in WEAPON_EVOLUTIONS


# === GAME DESIGNER NOTE ===
# Weapon evolutions are the "endgame" power fantasy:
# - Reaper's Embrace: Melee DPS king, sustain through lifesteal
# - Cosmic Annihilation: Screen-clearing ranged destruction
# - Sacred Ward: Tank build enabler with immunity
# Each evolution fundamentally changes playstyle!
# Sprint 12: 3 initial evolutions (can expand later)
