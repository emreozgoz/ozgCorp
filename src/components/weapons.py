"""
DARK SANCTUM - Weapon Definitions
Matrix Team: Game Designer

Vampire Survivors-style weapon progression
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class WeaponData:
    """Definition for a weapon type"""
    id: str
    name: str
    description: str
    icon: str  # Emoji for simple UI
    max_level: int

    # Stats per level (index 0 = level 1)
    damage_per_level: list[float]
    cooldown_per_level: list[float]
    range_per_level: list[float]
    projectile_count_per_level: list[int]

    # Weapon type
    weapon_type: str  # "projectile", "aura", "melee", "special"

    # Visual
    color: tuple[int, int, int]


# === WEAPON DEFINITIONS ===

SWORD = WeaponData(
    id="sword",
    name="Shadow Blade",
    description="Slashing sword that orbits around you",
    icon="⚔️",
    max_level=5,
    damage_per_level=[15, 20, 30, 45, 70],
    cooldown_per_level=[1.5, 1.3, 1.1, 0.9, 0.7],
    range_per_level=[80, 90, 100, 120, 150],
    projectile_count_per_level=[1, 1, 2, 2, 3],
    weapon_type="melee",
    color=(180, 180, 220)
)

MAGIC_MISSILE = WeaponData(
    id="magic_missile",
    name="Arcane Seeker",
    description="Homing magic missiles seek enemies",
    icon="🔮",
    max_level=5,
    damage_per_level=[12, 18, 25, 35, 50],
    cooldown_per_level=[2.0, 1.8, 1.5, 1.2, 1.0],
    range_per_level=[400, 450, 500, 550, 600],
    projectile_count_per_level=[1, 2, 3, 4, 5],
    weapon_type="projectile",
    color=(150, 100, 255)
)

LIGHTNING_CHAIN = WeaponData(
    id="lightning",
    name="Chain Lightning",
    description="Lightning that bounces between enemies",
    icon="⚡",
    max_level=5,
    damage_per_level=[20, 30, 45, 65, 90],
    cooldown_per_level=[3.0, 2.7, 2.4, 2.0, 1.5],
    range_per_level=[250, 280, 320, 360, 400],
    projectile_count_per_level=[1, 1, 1, 2, 2],  # Number of chains
    weapon_type="special",
    color=(255, 255, 100)
)

HOLY_WATER = WeaponData(
    id="holy_water",
    name="Blessed Vial",
    description="Creates damaging puddles on ground",
    icon="🧪",
    max_level=5,
    damage_per_level=[8, 12, 18, 26, 40],  # Damage per tick
    cooldown_per_level=[5.0, 4.5, 4.0, 3.5, 3.0],
    range_per_level=[150, 200, 250, 300, 350],  # Throw distance
    projectile_count_per_level=[1, 1, 2, 2, 3],  # Number of puddles
    weapon_type="aura",
    color=(100, 200, 255)
)

GARLIC = WeaponData(
    id="garlic",
    name="Garlic Aura",
    description="Defensive aura that damages nearby enemies",
    icon="🧄",
    max_level=5,
    damage_per_level=[5, 8, 12, 18, 28],  # Damage per second
    cooldown_per_level=[0.5, 0.5, 0.5, 0.5, 0.5],  # Constant tick
    range_per_level=[60, 80, 100, 120, 150],  # Aura radius
    projectile_count_per_level=[1, 1, 1, 1, 1],
    weapon_type="aura",
    color=(200, 200, 150)
)

# === NEW WEAPONS (Sprint 11) ===

SHADOW_SCYTHE = WeaponData(
    id="shadow_scythe",
    name="Death's Scythe",
    description="Massive rotating scythe that cleaves through enemies",
    icon="🗡️",
    max_level=5,
    damage_per_level=[25, 35, 50, 70, 100],
    cooldown_per_level=[2.0, 1.8, 1.6, 1.3, 1.0],
    range_per_level=[100, 120, 140, 170, 200],  # Rotation radius
    projectile_count_per_level=[1, 2, 2, 3, 3],  # Number of scythes
    weapon_type="melee",
    color=(120, 60, 180)  # Dark purple
)

FROST_NOVA = WeaponData(
    id="frost_nova",
    name="Frost Orb",
    description="Ice projectiles that slow and freeze enemies",
    icon="❄️",
    max_level=5,
    damage_per_level=[10, 16, 24, 35, 50],
    cooldown_per_level=[2.5, 2.3, 2.0, 1.7, 1.4],
    range_per_level=[300, 350, 400, 450, 500],
    projectile_count_per_level=[1, 2, 3, 4, 5],
    weapon_type="projectile",
    color=(100, 200, 255)  # Ice blue
)

BLOOD_LANCE = WeaponData(
    id="blood_lance",
    name="Crimson Spear",
    description="Piercing blood lances that penetrate multiple enemies",
    icon="🔱",
    max_level=5,
    damage_per_level=[18, 28, 42, 60, 85],
    cooldown_per_level=[1.8, 1.6, 1.4, 1.2, 1.0],
    range_per_level=[350, 400, 450, 500, 600],  # Pierce range
    projectile_count_per_level=[1, 1, 2, 3, 4],  # Number of lances
    weapon_type="projectile",
    color=(200, 30, 30)  # Blood red
)

# All available weapons
ALL_WEAPONS = [SWORD, MAGIC_MISSILE, LIGHTNING_CHAIN, HOLY_WATER, GARLIC,
               SHADOW_SCYTHE, FROST_NOVA, BLOOD_LANCE]

# Weapon pool for level up choices
WEAPON_POOL = {
    "sword": SWORD,
    "magic_missile": MAGIC_MISSILE,
    "lightning": LIGHTNING_CHAIN,
    "holy_water": HOLY_WATER,
    "garlic": GARLIC,
    "shadow_scythe": SHADOW_SCYTHE,
    "frost_nova": FROST_NOVA,
    "blood_lance": BLOOD_LANCE
}


def get_weapon_by_id(weapon_id: str) -> Optional[WeaponData]:
    """Get weapon data by ID"""
    return WEAPON_POOL.get(weapon_id)


# === GAME DESIGNER NOTE ===
# Weapon progression creates build variety:
# - Sword: Close-range orbital defense
# - Magic Missile: Reliable homing damage
# - Lightning: Crowd control for groups
# - Holy Water: Area denial and zone control
# - Garlic: Passive defense for tank builds
# - Shadow Scythe: High damage melee, slower but devastating
# - Frost Nova: Crowd control with slow effect
# - Blood Lance: Piercing projectiles for grouped enemies
# Each weapon has meaningful upgrades at each level
# Sprint 11: Added 3 new weapons (Total: 8 weapons)
