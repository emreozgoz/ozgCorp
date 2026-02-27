"""
DARK SANCTUM - Weapon System
Matrix Team: Game Designer + Developer

Vampire Survivors-style weapon progression
"""

import random
import math
from src.core.ecs import System
from src.components.components import *
from src.components.weapons import *
from config.settings import *


class WeaponFireSystem(System):
    """Fire player weapons automatically"""

    def __init__(self, world):
        super().__init__(world)
        self.priority = 32  # After auto-attack

    def update(self, dt: float):
        """Update and fire all active weapons"""
        # Find player
        player_entities = self.get_entities(Player, Position, WeaponInventory)
        if not player_entities:
            return

        player_entity = player_entities[0]
        player_pos = player_entity.get_component(Position)
        inventory = player_entity.get_component(WeaponInventory)

        # Fire each weapon in inventory
        for weapon_id, level in inventory.weapons.items():
            weapon_data = get_weapon_by_id(weapon_id)
            if not weapon_data:
                continue

            # Get weapon stats for current level
            level_idx = level - 1  # Level 1 = index 0
            damage = weapon_data.damage_per_level[level_idx]
            cooldown = weapon_data.cooldown_per_level[level_idx]
            range_ = weapon_data.range_per_level[level_idx]
            count = weapon_data.projectile_count_per_level[level_idx]

            # Check if weapon can fire (simple cooldown tracking per weapon type)
            weapon_key = f"weapon_{weapon_id}_cooldown"
            if not hasattr(self, weapon_key):
                setattr(self, weapon_key, 0.0)

            current_cooldown = getattr(self, weapon_key)
            current_cooldown -= dt
            setattr(self, weapon_key, current_cooldown)

            if current_cooldown > 0:
                continue

            # Fire weapon based on type
            if weapon_data.weapon_type == "projectile":
                self._fire_homing_missiles(player_pos, damage, range_, count, weapon_data.color)
            elif weapon_data.weapon_type == "melee":
                self._fire_orbiting_blades(player_entity, player_pos, damage, range_, count, weapon_data.color)
            elif weapon_data.weapon_type == "aura":
                self._activate_aura(player_pos, damage, range_, weapon_data.color, weapon_id)
            elif weapon_data.weapon_type == "special":
                self._fire_chain_lightning(player_pos, damage, range_, count, weapon_data.color)

            # Reset cooldown
            setattr(self, weapon_key, cooldown)

    def _fire_homing_missiles(self, player_pos: Position, damage: float, range_: float, count: int, color: tuple):
        """Fire homing missiles at nearest enemies"""
        # Find nearest enemies
        enemies = self.get_entities(Enemy, Position, Health)
        if not enemies:
            return

        # Sort by distance
        def distance_to_player(enemy):
            pos = enemy.get_component(Position)
            dx = pos.x - player_pos.x
            dy = pos.y - player_pos.y
            return math.sqrt(dx * dx + dy * dy)

        enemies.sort(key=distance_to_player)

        # Fire missiles at nearest enemies
        for i in range(min(count, len(enemies))):
            target = enemies[i]

            # Create homing missile
            missile = self.world.create_entity()
            missile.add_component(Position(player_pos.x, player_pos.y))
            missile.add_component(Velocity(0, 0))
            missile.add_component(Size(8, 8))
            missile.add_component(Sprite(color, radius=4))
            missile.add_component(HomingProjectile(target, damage, 250, 3.0))
            missile.add_component(Tag("projectile"))

    def _fire_orbiting_blades(self, player_entity, player_pos: Position, damage: float, range_: float, count: int, color: tuple):
        """Create orbiting blade entities"""
        # This would create persistent blade entities that orbit the player
        # For simplicity, we'll create projectiles that move in a circle
        for i in range(count):
            angle = (2 * math.pi / count) * i + (self.world.time if hasattr(self.world, 'time') else 0)

            # Calculate position on orbit
            x = player_pos.x + math.cos(angle) * range_
            y = player_pos.y + math.sin(angle) * range_

            # Calculate velocity (tangent to circle)
            vx = -math.sin(angle) * 200
            vy = math.cos(angle) * 200

            blade = self.world.create_entity()
            blade.add_component(Position(x, y))
            blade.add_component(Velocity(vx, vy))
            blade.add_component(Size(16, 16))
            blade.add_component(Sprite(color, radius=8))
            blade.add_component(Projectile("player", damage, lifetime=1.5))
            blade.add_component(Tag("weapon_blade"))

    def _activate_aura(self, player_pos: Position, damage: float, range_: float, color: tuple, weapon_id: str):
        """Damage all enemies in aura range"""
        enemies = self.get_entities(Enemy, Position, Health)

        for enemy in enemies:
            enemy_pos = enemy.get_component(Position)

            # Check distance
            dx = enemy_pos.x - player_pos.x
            dy = enemy_pos.y - player_pos.y
            dist = math.sqrt(dx * dx + dy * dy)

            if dist <= range_:
                # Deal damage
                health = enemy.get_component(Health)
                if not enemy.has_component(Invulnerable):
                    health.damage(damage)

    def _fire_chain_lightning(self, player_pos: Position, damage: float, range_: float, count: int, color: tuple):
        """Fire chain lightning that bounces between enemies"""
        # Find nearest enemy
        enemies = self.get_entities(Enemy, Position, Health)
        if not enemies:
            return

        # Sort by distance
        def distance_to_player(enemy):
            pos = enemy.get_component(Position)
            dx = pos.x - player_pos.x
            dy = pos.y - player_pos.y
            return math.sqrt(dx * dx + dy * dy)

        enemies.sort(key=distance_to_player)

        # Start chain from player position
        for chain_num in range(count):
            if not enemies:
                break

            current_pos = player_pos
            hit_enemies = set()

            # Chain up to 5 times
            for bounce in range(5):
                # Find nearest unaffected enemy
                nearest = None
                nearest_dist = float('inf')

                for enemy in enemies:
                    if enemy.id in hit_enemies:
                        continue

                    enemy_pos = enemy.get_component(Position)
                    dx = enemy_pos.x - current_pos.x
                    dy = enemy_pos.y - current_pos.y
                    dist = math.sqrt(dx * dx + dy * dy)

                    if dist <= range_ and dist < nearest_dist:
                        nearest = enemy
                        nearest_dist = dist

                if not nearest:
                    break

                # Damage enemy
                health = nearest.get_component(Health)
                health.damage(damage * (0.8 ** bounce))  # 20% less damage per bounce

                hit_enemies.add(nearest.id)
                current_pos = nearest.get_component(Position)


class LevelUpChoiceSystem(System):
    """Handle level-up weapon choices"""

    def __init__(self, world):
        super().__init__(world)
        self.priority = 62  # After death system

    def update(self, dt: float):
        """Check for level ups and create choices"""
        # This system waits for level-up events
        # When player levels up, it pauses the game and shows 3 weapon choices
        pass

    def generate_choices(self, inventory: WeaponInventory) -> list:
        """Generate 3 random weapon choices"""
        choices = []

        # Get available weapons (not maxed out)
        available = []
        for weapon_data in ALL_WEAPONS:
            current_level = inventory.get_level(weapon_data.id)
            if current_level < weapon_data.max_level:
                available.append(weapon_data)

        # If no weapons available, return empty
        if not available:
            return []

        # Select 3 random weapons
        num_choices = min(3, len(available))
        selected = random.sample(available, num_choices)

        for weapon_data in selected:
            current_level = inventory.get_level(weapon_data.id)
            next_level = current_level + 1

            choices.append({
                'weapon_id': weapon_data.id,
                'weapon_data': weapon_data,
                'current_level': current_level,
                'next_level': next_level,
                'is_new': current_level == 0
            })

        return choices


# === GAME DESIGNER NOTE ===
# Weapon system creates the core gameplay loop:
# 1. Player levels up
# 2. Choose weapon upgrade
# 3. Weapons fire automatically
# 4. Repeat
# Each weapon has unique behavior and upgrade path
