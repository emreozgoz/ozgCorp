"""
DARK SANCTUM - Ability System
Matrix Team: Game Designer + Developer

Q/W/E/R ability casting and effects
"""

import math
import pygame
from src.core.ecs import System
from src.components.components import *
from config.settings import *


class AbilityInputSystem(System):
    """Handle Q/W/E/R key presses for abilities"""

    def __init__(self, world):
        super().__init__(world)
        self.priority = 6  # Right after player input

    def update(self, dt: float):
        """Check for ability key presses"""
        entities = self.get_entities(Player, Abilities, Position)

        for entity in entities:
            abilities = entity.get_component(Abilities)
            pos = entity.get_component(Position)
            vel = entity.get_component(Velocity)

            # Update cooldowns
            abilities.update(dt)

            # Get key presses
            keys = pygame.key.get_pressed()

            # Q - Shadow Dash
            if keys[pygame.K_q] and abilities.can_cast('Q'):
                self._cast_shadow_dash(entity, pos, vel)
                abilities.cast('Q', ABILITY_Q_COOLDOWN)
                self._play_ability_sound()

            # W - Blood Nova
            elif keys[pygame.K_w] and abilities.can_cast('W'):
                self._cast_blood_nova(entity, pos)
                abilities.cast('W', ABILITY_W_COOLDOWN)
                self._play_ability_sound()

            # E - Arcane Missiles
            elif keys[pygame.K_e] and abilities.can_cast('E'):
                self._cast_arcane_missiles(entity, pos)
                abilities.cast('E', ABILITY_E_COOLDOWN)
                self._play_ability_sound()

            # R - Time Freeze
            elif keys[pygame.K_r] and abilities.can_cast('R'):
                self._cast_time_freeze(entity)
                abilities.cast('R', ABILITY_R_COOLDOWN)
                self._play_ability_sound()

    def _play_ability_sound(self):
        """Play ability cast sound"""
        audio_event = self.world.create_entity()
        audio_event.add_component(AudioEvent('ability_cast'))

    def _cast_shadow_dash(self, player_entity, pos: Position, vel: Velocity):
        """Q - Dash in movement direction with invulnerability"""
        # Get dash direction (from current velocity)
        dx = vel.vx
        dy = vel.vy

        # If not moving, dash in last faced direction (or forward)
        if dx == 0 and dy == 0:
            dy = -1  # Default dash upward

        # Normalize
        dist = math.sqrt(dx * dx + dy * dy)
        if dist > 0:
            dx /= dist
            dy /= dist

        # Apply dash
        pos.x += dx * ABILITY_Q_DASH_DISTANCE
        pos.y += dy * ABILITY_Q_DASH_DISTANCE

        # Add invulnerability component (temporary)
        player_entity.add_component(Invulnerable(ABILITY_Q_INVULN_TIME))

        # Visual effect (create dash trail)
        self._create_dash_trail(pos.x, pos.y)

        print(f"💨 Shadow Dash!")

    def _cast_blood_nova(self, player_entity, pos: Position):
        """W - AoE damage explosion"""
        # Damage all enemies in radius
        enemies = self.get_entities(Enemy, Position, Health)

        hit_count = 0
        for enemy in enemies:
            enemy_pos = enemy.get_component(Position)

            # Check distance
            dx = enemy_pos.x - pos.x
            dy = enemy_pos.y - pos.y
            dist = math.sqrt(dx * dx + dy * dy)

            if dist <= ABILITY_W_RADIUS:
                # Deal damage
                health = enemy.get_component(Health)
                health.damage(ABILITY_W_DAMAGE)

                # Knockback
                if dist > 0:
                    enemy_vel = enemy.get_component(Velocity)
                    knockback_force = ABILITY_W_KNOCKBACK
                    enemy_vel.vx += (dx / dist) * knockback_force
                    enemy_vel.vy += (dy / dist) * knockback_force

                hit_count += 1

        # Visual effect
        self._create_nova_effect(pos.x, pos.y)

        print(f"💥 Blood Nova! Hit {hit_count} enemies")

    def _cast_arcane_missiles(self, player_entity, pos: Position):
        """E - Fire 3 homing missiles"""
        # Find 3 nearest enemies
        enemies = self.get_entities(Enemy, Position, Health)

        # Sort by distance
        enemy_distances = []
        for enemy in enemies:
            enemy_pos = enemy.get_component(Position)
            dx = enemy_pos.x - pos.x
            dy = enemy_pos.y - pos.y
            dist = math.sqrt(dx * dx + dy * dy)
            enemy_distances.append((dist, enemy))

        enemy_distances.sort(key=lambda x: x[0])

        # Fire at up to 3 closest enemies
        missiles_fired = 0
        for i in range(min(3, len(enemy_distances))):
            target_enemy = enemy_distances[i][1]
            self._create_homing_missile(pos.x, pos.y, target_enemy)
            missiles_fired += 1

        print(f"🔮 Arcane Missiles! Fired {missiles_fired} missiles")

    def _cast_time_freeze(self, player_entity):
        """R - Slow all enemies"""
        enemies = self.get_entities(Enemy)

        for enemy in enemies:
            # Add slow effect
            enemy.add_component(Slowed(
                slow_percent=ABILITY_R_SLOW_PERCENT,
                duration=ABILITY_R_DURATION
            ))

        # Visual effect
        self._create_time_freeze_effect()

        print(f"⏰ Time Freeze! Slowed all enemies")

    def _create_dash_trail(self, x: float, y: float):
        """Create visual dash trail effect"""
        trail = self.world.create_entity()
        trail.add_component(Position(x, y))
        trail.add_component(Sprite((150, 100, 255, 100), radius=20))
        trail.add_component(Lifetime(0.3))
        trail.add_component(Tag("effect"))

    def _create_nova_effect(self, x: float, y: float):
        """Create nova explosion effect"""
        nova = self.world.create_entity()
        nova.add_component(Position(x, y))
        nova.add_component(Sprite(COLOR_BLOOD_RED, radius=ABILITY_W_RADIUS))
        nova.add_component(Lifetime(0.2))
        nova.add_component(Tag("effect"))

    def _create_homing_missile(self, x: float, y: float, target_entity):
        """Create homing missile entity"""
        missile = self.world.create_entity()
        missile.add_component(Position(x, y))
        missile.add_component(Velocity(0, 0))
        missile.add_component(Size(12, 12))
        missile.add_component(Sprite(COLOR_ARCANE_BLUE, radius=6))
        missile.add_component(HomingProjectile(
            target=target_entity,
            damage=ABILITY_E_DAMAGE,
            speed=ABILITY_E_SPEED,
            lifetime=3.0
        ))
        missile.add_component(Tag("missile"))

    def _create_time_freeze_effect(self):
        """Create time freeze visual effect"""
        # This will be rendered as screen overlay
        effect = self.world.create_entity()
        effect.add_component(ScreenEffect(
            effect_type="time_freeze",
            duration=ABILITY_R_DURATION
        ))
        effect.add_component(Tag("screen_effect"))


class HomingMissileSystem(System):
    """Handle homing missile movement and collision"""

    def __init__(self, world):
        super().__init__(world)
        self.priority = 36  # After projectiles

    def update(self, dt: float):
        """Update homing missiles"""
        missiles = self.get_entities(HomingProjectile, Position, Velocity)

        for missile_entity in missiles:
            homing = missile_entity.get_component(HomingProjectile)
            pos = missile_entity.get_component(Position)
            vel = missile_entity.get_component(Velocity)

            # Update lifetime
            if homing.update(dt):
                self.world.destroy_entity(missile_entity)
                continue

            # Check if target still exists
            if not homing.target or not homing.target.active:
                self.world.destroy_entity(missile_entity)
                continue

            # Get target position
            target_pos = homing.target.get_component(Position)
            if not target_pos:
                self.world.destroy_entity(missile_entity)
                continue

            # Move toward target
            dx = target_pos.x - pos.x
            dy = target_pos.y - pos.y
            dist = math.sqrt(dx * dx + dy * dy)

            if dist < 10:  # Hit target
                # Deal damage
                target_health = homing.target.get_component(Health)
                if target_health:
                    target_health.damage(homing.damage)

                # Destroy missile
                self.world.destroy_entity(missile_entity)
                continue

            if dist > 0:
                # Home in on target
                vel.vx = (dx / dist) * homing.speed
                vel.vy = (dy / dist) * homing.speed


class StatusEffectSystem(System):
    """Handle status effects like Slow, Invulnerable, etc."""

    def __init__(self, world):
        super().__init__(world)
        self.priority = 15  # Before movement

    def update(self, dt: float):
        """Update status effects"""
        # Handle Slowed
        slowed_entities = self.get_entities(Slowed, Velocity)
        for entity in slowed_entities:
            slowed = entity.get_component(Slowed)

            if slowed.update(dt):
                # Effect expired
                entity.remove_component(Slowed)
            else:
                # Apply slow
                vel = entity.get_component(Velocity)
                slow_multiplier = 1.0 - slowed.slow_percent
                vel.vx *= slow_multiplier
                vel.vy *= slow_multiplier

        # Handle Invulnerable
        invuln_entities = self.get_entities(Invulnerable)
        for entity in invuln_entities:
            invuln = entity.get_component(Invulnerable)

            if invuln.update(dt):
                # Effect expired
                entity.remove_component(Invulnerable)


class LifetimeSystem(System):
    """Handle entities with Lifetime component"""

    def __init__(self, world):
        super().__init__(world)
        self.priority = 65

    def update(self, dt: float):
        """Remove expired entities"""
        entities = self.get_entities(Lifetime)

        for entity in entities:
            lifetime = entity.get_component(Lifetime)

            if lifetime.update(dt):
                self.world.destroy_entity(entity)


# === GAME DESIGNER NOTES ===
# Ability design philosophy:
# Q - Mobility/Defense (short cooldown, tactical)
# W - AoE Damage (medium cooldown, positioning)
# E - Burst Damage (medium cooldown, precision)
# R - Ultimate (long cooldown, game-changing)
