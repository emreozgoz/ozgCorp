"""
DARK SANCTUM - Map Configurations
Matrix Team: Game Designer + Level Designer

3 unique maps with environmental hazards
"""

from config.settings import *


class MapData:
    """Map configuration data"""

    def __init__(self, map_id: str, name: str, description: str,
                 background_color: tuple, unlock_requirement: str = None,
                 hazard_type: str = None, hazard_count: int = 0):
        self.map_id = map_id
        self.name = name
        self.description = description
        self.background_color = background_color
        self.unlock_requirement = unlock_requirement  # Achievement ID or None
        self.hazard_type = hazard_type  # "blood_pool", "spike_trap", None
        self.hazard_count = hazard_count


# === MAP DEFINITIONS ===

MAPS = {
    "dark_sanctum": MapData(
        map_id="dark_sanctum",
        name="Dark Sanctum",
        description="The original arena. Open battlefield with no hazards.",
        background_color=COLOR_BACKGROUND,  # (10, 8, 20)
        unlock_requirement=None,  # Always unlocked
        hazard_type=None,
        hazard_count=0
    ),

    "blood_cathedral": MapData(
        map_id="blood_cathedral",
        name="Blood Cathedral",
        description="Gothic cathedral with blood pools. Take damage in pools!",
        background_color=(15, 5, 15),  # Darker purple
        unlock_requirement="survivor",  # Survive 5 minutes achievement
        hazard_type="blood_pool",
        hazard_count=8  # 8 blood pools scattered
    ),

    "cursed_crypts": MapData(
        map_id="cursed_crypts",
        name="Cursed Crypts",
        description="Ancient crypts with spike traps. Watch your step!",
        background_color=(8, 12, 8),  # Dark greenish
        unlock_requirement="boss_slayer",  # Defeat first boss achievement
        hazard_type="spike_trap",
        hazard_count=12  # 12 spike traps
    )
}


# Default map
DEFAULT_MAP = "dark_sanctum"


def get_map(map_id: str) -> MapData:
    """Get map data by ID"""
    return MAPS.get(map_id, MAPS[DEFAULT_MAP])


def is_map_unlocked(map_id: str, achievements: list) -> bool:
    """Check if map is unlocked based on achievements"""
    map_data = get_map(map_id)

    # No requirement = always unlocked
    if map_data.unlock_requirement is None:
        return True

    # Check if required achievement is unlocked
    return map_data.unlock_requirement in achievements


def get_unlocked_maps(achievements: list) -> list:
    """Get list of all unlocked map IDs"""
    unlocked = []
    for map_id in MAPS.keys():
        if is_map_unlocked(map_id, achievements):
            unlocked.append(map_id)
    return unlocked


# === HAZARD DATA ===

class HazardData:
    """Hazard configuration"""

    def __init__(self, hazard_type: str, damage: float, damage_interval: float,
                 color: tuple, radius: float, warning_color: tuple = None):
        self.hazard_type = hazard_type
        self.damage = damage
        self.damage_interval = damage_interval  # Seconds between damage ticks
        self.color = color
        self.radius = radius
        self.warning_color = warning_color or color


HAZARDS = {
    "blood_pool": HazardData(
        hazard_type="blood_pool",
        damage=5.0,
        damage_interval=1.0,  # 5 damage per second
        color=(120, 20, 20),  # Dark red
        radius=60.0,
        warning_color=(180, 30, 30)  # Brighter red for warning
    ),

    "spike_trap": HazardData(
        hazard_type="spike_trap",
        damage=20.0,
        damage_interval=2.0,  # 20 damage every 2 seconds
        color=(80, 80, 80),  # Gray
        radius=40.0,
        warning_color=(200, 50, 50)  # Red flash when active
    )
}


def get_hazard_data(hazard_type: str) -> HazardData:
    """Get hazard configuration"""
    return HAZARDS.get(hazard_type)


# === GAME DESIGNER NOTE ===
# Map design philosophy:
# - Dark Sanctum: Learning map, no hazards
# - Blood Cathedral: Positioning challenge (avoid pools)
# - Cursed Crypts: Timing challenge (dodge spike traps)
# Each map rewards different playstyles!
