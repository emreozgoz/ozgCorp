"""
DARK SANCTUM - Screen Effects System
Matrix Team: UI/UX Designer + Technical Director

Screen shake, flash effects, and visual polish
"""

import random
import math
from src.core.ecs import System, Component
from src.components.components import *


class ScreenShake(Component):
    """Screen shake effect"""
    def __init__(self, intensity: float, duration: float):
        self.intensity = intensity  # Max pixel offset
        self.duration = duration
        self.elapsed = 0.0

    def get_offset(self) -> tuple[float, float]:
        """Get current shake offset"""
        if self.elapsed >= self.duration:
            return (0, 0)

        # Decrease intensity over time
        progress = self.elapsed / self.duration
        current_intensity = self.intensity * (1.0 - progress)

        # Random offset
        angle = random.uniform(0, 2 * math.pi)
        offset_x = math.cos(angle) * current_intensity
        offset_y = math.sin(angle) * current_intensity

        return (offset_x, offset_y)

    def update(self, dt: float) -> bool:
        """Update shake, return True if finished"""
        self.elapsed += dt
        return self.elapsed >= self.duration


class HitFlash(Component):
    """Flash effect when entity is hit"""
    def __init__(self, duration: float = 0.1):
        self.duration = duration
        self.elapsed = 0.0
        self.active = True

    def update(self, dt: float) -> bool:
        """Update flash, return True if finished"""
        self.elapsed += dt
        if self.elapsed >= self.duration:
            self.active = False
            return True
        return False


class ScreenEffectsSystem(System):
    """Manage screen shake and visual effects"""

    def __init__(self, world):
        super().__init__(world)
        self.priority = 5  # Before rendering
        self.screen_shake = None
        self.camera_offset = (0, 0)

    def update(self, dt: float):
        """Update screen shake"""
        # Update active screen shake
        if self.screen_shake:
            self.camera_offset = self.screen_shake.get_offset()
            if self.screen_shake.update(dt):
                self.screen_shake = None
                self.camera_offset = (0, 0)
        else:
            self.camera_offset = (0, 0)

        # Update hit flash effects
        entities_with_flash = self.get_entities(HitFlash)
        for entity in entities_with_flash:
            flash = entity.get_component(HitFlash)
            if flash.update(dt):
                entity.remove_component(HitFlash)

    def add_shake(self, intensity: float, duration: float):
        """Add screen shake effect"""
        # If there's already a shake, use the stronger one
        if self.screen_shake:
            if intensity > self.screen_shake.intensity:
                self.screen_shake = ScreenShake(intensity, duration)
        else:
            self.screen_shake = ScreenShake(intensity, duration)

    def get_camera_offset(self) -> tuple[float, float]:
        """Get current camera offset for rendering"""
        return self.camera_offset


class HitFlashSystem(System):
    """Add flash effects when entities take damage"""

    def __init__(self, world):
        super().__init__(world)
        self.priority = 41  # After damage systems
        self.last_health = {}  # Track health changes

    def update(self, dt: float):
        """Check for damage and add flash effects"""
        entities_with_health = self.get_entities(Health, Sprite)

        for entity in entities_with_health:
            health = entity.get_component(Health)

            # Track health
            entity_id = entity.id
            if entity_id not in self.last_health:
                self.last_health[entity_id] = health.current

            # Check if damaged
            if health.current < self.last_health[entity_id]:
                # Add flash effect
                if not entity.has_component(HitFlash):
                    entity.add_component(HitFlash(0.1))

                # Screen shake for player hits
                if entity.has_component(Player):
                    # Get screen effects system
                    from src.systems.screen_effects import ScreenEffectsSystem
                    for system in self.world.systems:
                        if isinstance(system, ScreenEffectsSystem):
                            system.add_shake(3.0, 0.2)
                            break

            # Update tracked health
            self.last_health[entity_id] = health.current

            # Clean up dead entities
            if not health.is_alive and entity_id in self.last_health:
                del self.last_health[entity_id]


class DamageNumber(Component):
    """Floating damage number"""
    def __init__(self, damage: float, is_critical: bool = False):
        self.damage = damage
        self.is_critical = is_critical
        self.lifetime = 1.0
        self.elapsed = 0.0
        self.velocity_y = -50  # Float upward

    def update(self, dt: float) -> bool:
        """Update lifetime, return True if expired"""
        self.elapsed += dt
        return self.elapsed >= self.lifetime


class DamageNumberSystem(System):
    """Display floating damage numbers"""

    def __init__(self, world):
        super().__init__(world)
        self.priority = 42  # After hit flash

    def update(self, dt: float):
        """Update damage numbers"""
        damage_entities = self.get_entities(DamageNumber, Position)

        for entity in damage_entities:
            damage_num = entity.get_component(DamageNumber)
            pos = entity.get_component(Position)

            # Float upward
            pos.y += damage_num.velocity_y * dt

            # Check lifetime
            if damage_num.update(dt):
                self.world.destroy_entity(entity)


def create_damage_number(world, x: float, y: float, damage: float, is_critical: bool = False):
    """Create floating damage number"""
    entity = world.create_entity()
    entity.add_component(Position(x, y))
    entity.add_component(DamageNumber(damage, is_critical))
    entity.add_component(Tag("damage_number"))
    return entity


# Trigger screen shake on specific events
def trigger_screen_shake(world, intensity: float, duration: float):
    """Trigger screen shake effect"""
    for system in world.systems:
        from src.systems.screen_effects import ScreenEffectsSystem
        if isinstance(system, ScreenEffectsSystem):
            system.add_shake(intensity, duration)
            break


# === UI/UX DESIGNER NOTE ===
# Screen shake and hit flash create visceral feedback
# Damage numbers provide clear combat information
# These "game feel" elements make combat satisfying
