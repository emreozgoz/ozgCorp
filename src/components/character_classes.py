"""
DARK SANCTUM - Character Classes
Matrix Team: Game Designer + Developer

3 unique character classes with different playstyles
"""

from dataclasses import dataclass
from typing import Dict
from config.settings import *


@dataclass
class CharacterClass:
    """Character class definition"""
    name: str
    description: str
    health: float
    speed: float
    damage: float
    color: tuple
    passive_name: str
    passive_description: str

    # Passive bonuses
    ability_damage_mult: float = 1.0
    ability_cooldown_mult: float = 1.0
    damage_reduction: float = 0.0


# === CHARACTER CLASS DEFINITIONS ===

SHADOW_KNIGHT = CharacterClass(
    name="Shadow Knight",
    description="Balanced dark warrior with enhanced mobility",
    health=100,
    speed=250,
    damage=10,
    color=(150, 100, 200),  # Purple
    passive_name="Shadow Step",
    passive_description="Shadow Dash cooldown reduced by 25%",
    ability_cooldown_mult=0.75  # Only for Q ability
)

BLOOD_MAGE = CharacterClass(
    name="Blood Mage",
    description="Glass cannon caster with devastating abilities",
    health=70,
    speed=220,
    damage=15,
    color=(180, 40, 60),  # Crimson
    passive_name="Blood Magic",
    passive_description="All abilities deal 50% more damage",
    ability_damage_mult=1.5
)

VOID_GUARDIAN = CharacterClass(
    name="Void Guardian",
    description="Tanky defender who shrugs off damage",
    health=150,
    speed=200,
    damage=7,
    color=(60, 120, 160),  # Dark cyan
    passive_name="Iron Will",
    passive_description="Take 25% less damage from all sources",
    damage_reduction=0.25
)

NECROMANCER = CharacterClass(
    name="Necromancer",
    description="Death cultist who gains power from kills",
    health=85,
    speed=230,
    damage=12,
    color=(100, 50, 120),  # Dark purple
    passive_name="Soul Harvest",
    passive_description="Weapons deal 10% more damage (stacks 5x on kills)",
    ability_damage_mult=1.0  # Base, will be modified by kills in-game
)

TEMPEST_RANGER = CharacterClass(
    name="Tempest Ranger",
    description="Swift archer with enhanced projectile weapons",
    health=90,
    speed=270,
    damage=9,
    color=(80, 180, 140),  # Forest green
    passive_name="Wind Walker",
    passive_description="Projectile weapons fire 30% faster and fly further",
    ability_cooldown_mult=0.7  # Affects projectile weapon cooldowns
)


# All available classes
ALL_CLASSES = [SHADOW_KNIGHT, BLOOD_MAGE, VOID_GUARDIAN, NECROMANCER, TEMPEST_RANGER]


def get_class_by_name(name: str) -> CharacterClass:
    """Get class by name"""
    for char_class in ALL_CLASSES:
        if char_class.name == name:
            return char_class
    return SHADOW_KNIGHT  # Default


# === GAME DESIGNER NOTES ===
# Class balance philosophy:
# - Shadow Knight: Baseline, balanced mobility warrior
# - Blood Mage: High risk/reward glass cannon caster
# - Void Guardian: Forgiving tank for new players
# - Necromancer: Scaling damage dealer, rewards aggressive play
# - Tempest Ranger: Projectile specialist, fastest movement
#
# Sprint 14: Added Necromancer (kill-scaling) and Tempest Ranger (projectile focus)
# All 5 classes viable with distinct playstyles
