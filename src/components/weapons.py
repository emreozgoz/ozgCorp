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

# === NEW WEAPONS (Sprint 14) ===

SOUL_REAVER = WeaponData(
    id="soul_reaver",
    name="Soul Reaver",
    description="Dark energy beams that drain life from enemies",
    icon="👻",
    max_level=5,
    damage_per_level=[14, 22, 34, 50, 72],
    cooldown_per_level=[2.2, 2.0, 1.8, 1.5, 1.2],
    range_per_level=[300, 350, 400, 450, 500],
    projectile_count_per_level=[1, 2, 2, 3, 4],
    weapon_type="projectile",
    color=(140, 70, 200)  # Dark purple
)

BONE_STORM = WeaponData(
    id="bone_storm",
    name="Bone Storm",
    description="Whirling bones orbit rapidly around you",
    icon="🦴",
    max_level=5,
    damage_per_level=[10, 16, 24, 35, 52],
    cooldown_per_level=[0.8, 0.75, 0.7, 0.6, 0.5],  # Very fast attacks
    range_per_level=[90, 110, 130, 150, 180],
    projectile_count_per_level=[2, 3, 4, 5, 6],  # Many orbiting bones
    weapon_type="melee",
    color=(220, 220, 200)  # Bone white
)

CURSED_TOME = WeaponData(
    id="cursed_tome",
    name="Cursed Tome",
    description="Summons dark sigils that explode on contact",
    icon="📖",
    max_level=5,
    damage_per_level=[22, 35, 52, 75, 110],
    cooldown_per_level=[3.5, 3.2, 2.8, 2.4, 2.0],
    range_per_level=[250, 300, 350, 400, 450],
    projectile_count_per_level=[1, 1, 2, 2, 3],  # Sigil count
    weapon_type="special",
    color=(80, 40, 100)  # Dark violet
)

POISON_DAGGER = WeaponData(
    id="poison_dagger",
    name="Venom Fang",
    description="Rapid poison daggers that deal damage over time",
    icon="🗡️",
    max_level=5,
    damage_per_level=[8, 13, 20, 30, 45],  # Low per hit, but DoT
    cooldown_per_level=[0.6, 0.55, 0.5, 0.4, 0.3],  # Very rapid fire
    range_per_level=[200, 230, 260, 300, 350],
    projectile_count_per_level=[1, 2, 2, 3, 4],
    weapon_type="projectile",
    color=(80, 200, 80)  # Toxic green
)

VOID_LANCE = WeaponData(
    id="void_lance",
    name="Void Lance",
    description="Massive slow projectile that pierces everything",
    icon="🌑",
    max_level=5,
    damage_per_level=[35, 55, 80, 115, 165],  # High damage
    cooldown_per_level=[4.0, 3.7, 3.4, 3.0, 2.5],  # Slow but powerful
    range_per_level=[600, 650, 700, 800, 900],  # Long range
    projectile_count_per_level=[1, 1, 1, 2, 2],  # Few but strong
    weapon_type="projectile",
    color=(40, 40, 80)  # Void dark
)

# === EVOLVED WEAPONS (Sprint 12) ===

REAPERS_EMBRACE = WeaponData(
    id="reapers_embrace",
    name="Reaper's Embrace",
    description="💀 EVOLVED: Scythe storm of obliteration",
    icon="💀",
    max_level=1,  # Evolved weapons don't level further
    damage_per_level=[210],  # 3x base max (70 * 3)
    cooldown_per_level=[0.35],  # 0.5x base (0.7 * 0.5)
    range_per_level=[300],  # 2x base (150 * 2)
    projectile_count_per_level=[6],  # 2x base (3 + 3)
    weapon_type="melee",
    color=(60, 10, 80)  # Deeper dark purple
)

COSMIC_ANNIHILATION = WeaponData(
    id="cosmic_annihilation",
    name="Cosmic Annihilation",
    description="🌌 EVOLVED: Devastating cosmic barrage",
    icon="🌌",
    max_level=1,
    damage_per_level=[125],  # 2.5x base (50 * 2.5)
    cooldown_per_level=[0.6],  # 0.6x base (1.0 * 0.6)
    range_per_level=[900],  # 1.5x base (600 * 1.5)
    projectile_count_per_level=[10],  # 2x base (5 + 5)
    weapon_type="projectile",
    color=(200, 100, 255)  # Bright cosmic purple
)

SACRED_WARD = WeaponData(
    id="sacred_ward",
    name="Sacred Ward",
    description="✨ EVOLVED: Holy immunity barrier",
    icon="✨",
    max_level=1,
    damage_per_level=[112],  # 4x base (28 * 4)
    cooldown_per_level=[0.5],  # Same tick
    range_per_level=[375],  # 2.5x base (150 * 2.5)
    projectile_count_per_level=[1],
    weapon_type="aura",
    color=(255, 255, 200)  # Bright golden
)

# === SPRINT 14 EVOLVED WEAPONS ===

STORM_BRINGER = WeaponData(
    id="storm_bringer",
    name="Storm Bringer",
    description="⚡ EVOLVED: Infinite chain lightning storm",
    icon="⚡",
    max_level=1,
    damage_per_level=[252],  # 2.8x base (90 * 2.8)
    cooldown_per_level=[0.6],  # 0.4x base (1.5 * 0.4)
    range_per_level=[800],  # 2x base (400 * 2)
    projectile_count_per_level=[5],  # 2 + 3
    weapon_type="special",
    color=(255, 255, 50)  # Bright electric yellow
)

ABSOLUTE_ZERO = WeaponData(
    id="absolute_zero",
    name="Absolute Zero",
    description="❄️ EVOLVED: Freezing blizzard obliteration",
    icon="❄️",
    max_level=1,
    damage_per_level=[160],  # 3.2x base (50 * 3.2)
    cooldown_per_level=[0.7],  # 0.5x base (1.4 * 0.5)
    range_per_level=[900],  # 1.8x base (500 * 1.8)
    projectile_count_per_level=[10],  # 5 + 5
    weapon_type="projectile",
    color=(150, 230, 255)  # Bright ice blue
)

# All available weapons
ALL_WEAPONS = [SWORD, MAGIC_MISSILE, LIGHTNING_CHAIN, HOLY_WATER, GARLIC,
               SHADOW_SCYTHE, FROST_NOVA, BLOOD_LANCE,
               SOUL_REAVER, BONE_STORM, CURSED_TOME, POISON_DAGGER, VOID_LANCE,
               REAPERS_EMBRACE, COSMIC_ANNIHILATION, SACRED_WARD, STORM_BRINGER, ABSOLUTE_ZERO]

# Weapon pool for level up choices
WEAPON_POOL = {
    "sword": SWORD,
    "magic_missile": MAGIC_MISSILE,
    "lightning": LIGHTNING_CHAIN,
    "holy_water": HOLY_WATER,
    "garlic": GARLIC,
    "shadow_scythe": SHADOW_SCYTHE,
    "frost_nova": FROST_NOVA,
    "blood_lance": BLOOD_LANCE,
    # Sprint 14 weapons
    "soul_reaver": SOUL_REAVER,
    "bone_storm": BONE_STORM,
    "cursed_tome": CURSED_TOME,
    "poison_dagger": POISON_DAGGER,
    "void_lance": VOID_LANCE,
    # Evolved weapons (only accessible via evolution)
    "reapers_embrace": REAPERS_EMBRACE,
    "cosmic_annihilation": COSMIC_ANNIHILATION,
    "sacred_ward": SACRED_WARD,
    # Sprint 14 evolved weapons
    "storm_bringer": STORM_BRINGER,
    "absolute_zero": ABSOLUTE_ZERO
}


def get_weapon_by_id(weapon_id: str) -> Optional[WeaponData]:
    """Get weapon data by ID"""
    return WEAPON_POOL.get(weapon_id)


# === GAME DESIGNER NOTE ===
# Weapon progression creates build variety:
#
# ORIGINAL 8 WEAPONS:
# - Sword: Close-range orbital defense
# - Magic Missile: Reliable homing damage
# - Lightning: Crowd control for groups
# - Holy Water: Area denial and zone control
# - Garlic: Passive defense for tank builds
# - Shadow Scythe: High damage melee, slower but devastating
# - Frost Nova: Crowd control with slow effect
# - Blood Lance: Piercing projectiles for grouped enemies
#
# SPRINT 14 - NEW WEAPONS (5):
# - Soul Reaver: Life-drain projectiles (synergizes with Necromancer)
# - Bone Storm: Very fast orbiting melee (high DPS, close range)
# - Cursed Tome: Explosive sigils (high damage, slow cooldown)
# - Poison Dagger: Rapid-fire DoT projectiles (synergizes with Tempest Ranger)
# - Void Lance: Slow, massive piercing projectiles (sniper weapon)
#
# Total: 13 base weapons + 5 evolved = 18 total weapons
# Sprint 14: Now 18 total weapons (13 base + 5 evolutions)
# Each weapon has meaningful upgrades at each level
