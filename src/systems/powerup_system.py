"""
DARK SANCTUM - Power-Up System
Matrix Team: Game Designer + Developer

Power-ups that drop from enemies
"""

import random
import math
from src.core.ecs import System
from src.components.components import *
from config.settings import *


class PowerUpSpawnSystem(System):
    """Spawn power-ups when enemies die"""

    def __init__(self, world):
        super().__init__(world)
        self.priority = 61  # After death system

    def update(self, dt: float):
        """Check for enemy deaths and spawn power-ups"""
        # This is handled by modifying DeathSystem to spawn power-ups
        pass


class PowerUpCollectionSystem(System):
    """Handle power-up collection by player"""

    def __init__(self, world):
        super().__init__(world)
        self.priority = 55  # Between spawning and death

    def update(self, dt: float):
        """Check for power-up collisions with player"""
        # Find player
        player_entities = self.get_entities(Player, Position, Health, Experience, Damage)
        if not player_entities:
            return

        player_entity = player_entities[0]
        player_pos = player_entity.get_component(Position)
        player_health = player_entity.get_component(Health)
        player_xp = player_entity.get_component(Experience)
        player_damage = player_entity.get_component(Damage)

        # Find power-ups
        powerup_entities = self.get_entities(PowerUp, Position, Size)

        for powerup_entity in powerup_entities:
            powerup = powerup_entity.get_component(PowerUp)
            pos = powerup_entity.get_component(Position)
            size = powerup_entity.get_component(Size)

            # Update lifetime
            if powerup.update(dt):
                self.world.destroy_entity(powerup_entity)
                continue

            # Check collision with player
            dx = pos.x - player_pos.x
            dy = pos.y - player_pos.y
            dist = math.sqrt(dx * dx + dy * dy)

            # Pickup radius (larger than visual size for easier pickup)
            pickup_radius = 30

            if dist < pickup_radius:
                self._apply_powerup(player_entity, powerup, player_health, player_xp, player_damage)

                # Track power-up collection
                from src.systems.stats_system import GameStats
                if player_entity.has_component(GameStats):
                    stats = player_entity.get_component(GameStats)
                    stats.power_ups_collected += 1

                self.world.destroy_entity(powerup_entity)

    def _apply_powerup(self, player_entity, powerup: PowerUp, health: Health, xp: Experience, damage: Damage):
        """Apply power-up effect to player"""
        if powerup.powerup_type == "health":
            health.heal(powerup.value)
            print(f"💚 +{int(powerup.value)} HP")

        elif powerup.powerup_type == "damage_boost":
            # Temporarily increase damage (would need a buff system for this)
            damage.amount += powerup.value
            print(f"⚔️  Damage Boost! +{int(powerup.value)} damage")

        elif powerup.powerup_type == "xp":
            if xp.add_xp(int(powerup.value)):
                # Level up particles
                pos = player_entity.get_component(Position)
                if pos:
                    from src.systems.particle_system import create_level_up_particles
                    create_level_up_particles(self.world, pos.x, pos.y, 40)

                # Level up sound
                audio_event = self.world.create_entity()
                audio_event.add_component(AudioEvent('level_up'))

                print(f"⬆️ LEVEL UP! Now level {xp.level}")
            else:
                print(f"✨ +{int(powerup.value)} XP")


def spawn_powerup(world, x: float, y: float):
    """Spawn random power-up at location"""
    # Random power-up type (50% health, 30% XP, 20% damage)
    roll = random.random()
    if roll < 0.50:
        powerup_type = "health"
        color = POWERUP_HEALTH_COLOR
        value = POWERUP_HEALTH_VALUE
    elif roll < 0.80:
        powerup_type = "xp"
        color = POWERUP_XP_COLOR
        value = POWERUP_XP_VALUE
    else:
        powerup_type = "damage_boost"
        color = POWERUP_DAMAGE_COLOR
        value = POWERUP_DAMAGE_BOOST_VALUE

    # Create power-up entity
    powerup = world.create_entity()
    powerup.add_component(Position(x, y))
    powerup.add_component(Size(12, 12))
    powerup.add_component(Sprite(color, radius=6))
    powerup.add_component(PowerUp(powerup_type, value, POWERUP_LIFETIME))
    powerup.add_component(Tag("powerup"))


# === GAME DESIGNER NOTE ===
# Power-ups add strategic depth:
# - Health: Encourages aggressive play to survive
# - Damage Boost: Temporary power spike
# - XP: Faster progression
# Drop rate balanced to not be too common
