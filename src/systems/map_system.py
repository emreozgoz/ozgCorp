"""
DARK SANCTUM - Map & Environmental Hazard Systems
Matrix Team: Game Designer + Developer + Level Designer

Handles map initialization, hazards, and map-specific logic
"""

import random
import math
from src.core.ecs import System
from src.components.components import *
from config.settings import *
from config.maps import *


class MapManager(System):
    """Manages current map and spawns hazards"""

    def __init__(self, world):
        super().__init__(world)
        self.priority = 5  # Early, before game logic
        self.current_map_id = DEFAULT_MAP
        self.hazards_spawned = False

    def update(self, dt: float):
        """Map management (mostly initialization)"""
        # Spawn hazards if needed
        if not self.hazards_spawned:
            self._spawn_hazards()
            self.hazards_spawned = True

    def set_map(self, map_id: str):
        """Change current map"""
        self.current_map_id = map_id
        self.hazards_spawned = False

        # Update background color
        map_data = get_map(map_id)
        # Background color will be used by render system

        print(f"🗺️  Map changed to: {map_data.name}")

    def _spawn_hazards(self):
        """Spawn environmental hazards for current map"""
        map_data = get_map(self.current_map_id)

        if map_data.hazard_type is None or map_data.hazard_count == 0:
            return  # No hazards on this map

        hazard_data = get_hazard_data(map_data.hazard_type)
        if not hazard_data:
            return

        print(f"🔥 Spawning {map_data.hazard_count} {map_data.hazard_type} hazards")

        # Spawn hazards in random positions (avoid center)
        for i in range(map_data.hazard_count):
            # Random position (avoid center spawn area)
            angle = random.uniform(0, 2 * math.pi)
            distance = random.uniform(150, 400)  # Distance from center

            x = WINDOW_WIDTH / 2 + math.cos(angle) * distance
            y = WINDOW_HEIGHT / 2 + math.sin(angle) * distance

            # Clamp to screen bounds
            x = max(hazard_data.radius, min(WINDOW_WIDTH - hazard_data.radius, x))
            y = max(hazard_data.radius, min(WINDOW_HEIGHT - hazard_data.radius, y))

            # Create hazard entity
            hazard = self.world.create_entity()
            hazard.add_component(Position(x, y))
            hazard.add_component(Size(hazard_data.radius * 2, hazard_data.radius * 2))
            hazard.add_component(Sprite(hazard_data.color, radius=hazard_data.radius))
            hazard.add_component(EnvironmentalHazard(
                hazard_type=map_data.hazard_type,
                damage=hazard_data.damage,
                damage_interval=hazard_data.damage_interval
            ))
            hazard.add_component(Tag("hazard"))

    def get_current_map_data(self) -> MapData:
        """Get current map data"""
        return get_map(self.current_map_id)


class EnvironmentalHazardSystem(System):
    """Handles hazard damage and effects"""

    def __init__(self, world):
        super().__init__(world)
        self.priority = 30  # After movement, before combat

    def update(self, dt: float):
        """Update all hazards"""
        hazards = self.get_entities(EnvironmentalHazard, Position)

        # Get player
        player_entities = self.get_entities(Player, Position, Health)
        if not player_entities:
            return

        player = player_entities[0]
        player_pos = player.get_component(Position)
        player_health = player.get_component(Health)

        for hazard_entity in hazards:
            hazard = hazard_entity.get_component(EnvironmentalHazard)
            hazard_pos = hazard_entity.get_component(Position)
            hazard_size = hazard_entity.get_component(Size)

            # Update hazard state
            hazard.time_since_damage += dt

            # Spike trap logic (toggle active/inactive)
            if hazard.hazard_type == "spike_trap":
                hazard.active_timer += dt
                # 2s active, 2s inactive cycle
                if hazard.active_timer >= 2.0:
                    hazard.is_active = not hazard.is_active
                    hazard.active_timer = 0.0

                    # Visual feedback (change sprite color)
                    sprite = hazard_entity.get_component(Sprite)
                    if hazard.is_active:
                        # Active = red warning
                        hazard_data = get_hazard_data(hazard.hazard_type)
                        sprite.color = hazard_data.warning_color
                    else:
                        # Inactive = gray
                        hazard_data = get_hazard_data(hazard.hazard_type)
                        sprite.color = hazard_data.color

            # Check if player is in hazard
            dx = player_pos.x - hazard_pos.x
            dy = player_pos.y - hazard_pos.y
            dist = math.sqrt(dx * dx + dy * dy)

            # Use hazard radius
            hazard_radius = hazard_size.width / 2 if hazard_size else 50

            if dist <= hazard_radius:
                # Player is in hazard!
                # For spike traps, only damage if active
                if hazard.hazard_type == "spike_trap" and not hazard.is_active:
                    continue

                # Apply damage at intervals
                if hazard.time_since_damage >= hazard.damage_interval:
                    # Check invulnerability
                    if not player.has_component(Invulnerable):
                        player_health.damage(hazard.damage)

                        # Track stats
                        from src.systems.stats_system import GameStats
                        if player.has_component(GameStats):
                            stats = player.get_component(GameStats)
                            stats.damage_taken += hazard.damage

                        # Damage number (disabled for hazards to reduce visual clutter)
                        # from src.systems.screen_effects import spawn_damage_number
                        # spawn_damage_number(self.world, player_pos.x, player_pos.y,
                        #                     int(hazard.damage), is_crit=False, is_heal=False)

                        # Visual feedback (small screen shake for hazard damage)
                        from src.systems.screen_effects import trigger_screen_shake
                        trigger_screen_shake(self.world, 3.0, 0.15)

                    hazard.time_since_damage = 0.0


# === GAME DESIGNER NOTE ===
# Environmental hazards add strategic positioning:
# - Blood pools: Constant danger zones (area denial)
# - Spike traps: Timing challenge (pattern recognition)
# Each map has unique hazard layout for variety!
