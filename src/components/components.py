"""
DARK SANCTUM - Components
Matrix Team: Game Designer + Developer

All game components following ECS pattern
"""

from src.core.ecs import Component
import pygame
from typing import Optional, Callable


# === CORE COMPONENTS ===

class Position(Component):
    """Entity position in world space"""

    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y


class Velocity(Component):
    """Entity velocity (pixels per second)"""

    def __init__(self, vx: float = 0, vy: float = 0):
        self.vx = vx
        self.vy = vy


class Size(Component):
    """Entity size (for collision and rendering)"""

    def __init__(self, width: float, height: float):
        self.width = width
        self.height = height


class Sprite(Component):
    """Visual representation"""

    def __init__(self, color: tuple, radius: Optional[float] = None):
        self.color = color
        self.radius = radius  # If not None, draw as circle


# === COMBAT COMPONENTS ===

class Health(Component):
    """Health and damage tracking"""

    def __init__(self, max_health: float, current: Optional[float] = None):
        self.max_health = max_health
        self.current = current if current is not None else max_health
        self.regeneration = 0.0  # HP per second

    @property
    def is_alive(self) -> bool:
        return self.current > 0

    @property
    def percent(self) -> float:
        return self.current / self.max_health if self.max_health > 0 else 0

    def damage(self, amount: float):
        """Take damage"""
        self.current = max(0, self.current - amount)

    def heal(self, amount: float):
        """Heal"""
        self.current = min(self.max_health, self.current + amount)


class Damage(Component):
    """Damage dealer"""

    def __init__(self, amount: float):
        self.amount = amount


class Team(Component):
    """Team affiliation for combat"""

    def __init__(self, team: str):
        self.team = team  # "player" or "enemy"


# === PLAYER COMPONENTS ===

class Player(Component):
    """Marks entity as player"""

    def __init__(self, character_class_name: str = "Shadow Knight"):
        self.character_class_name = character_class_name
        self.move_speed = 250.0


class Experience(Component):
    """XP and leveling"""

    def __init__(self):
        self.current_xp = 0
        self.level = 1
        self.xp_to_next_level = 100

    def add_xp(self, amount: int) -> bool:
        """Add XP, return True if leveled up"""
        self.current_xp += amount
        if self.current_xp >= self.xp_to_next_level:
            return self._level_up()
        return False

    def _level_up(self) -> bool:
        """Level up"""
        self.current_xp -= self.xp_to_next_level
        self.level += 1
        self.xp_to_next_level = int(self.xp_to_next_level * 1.5)
        return True


class AutoAttack(Component):
    """Auto-attack system"""

    def __init__(self, damage: float, range_: float, cooldown: float, projectile_speed: float):
        self.damage = damage
        self.range = range_
        self.cooldown = cooldown
        self.projectile_speed = projectile_speed
        self.time_since_attack = 0.0

    def can_attack(self) -> bool:
        return self.time_since_attack >= self.cooldown

    def attack(self):
        """Reset cooldown"""
        self.time_since_attack = 0.0

    def update(self, dt: float):
        """Update cooldown"""
        self.time_since_attack += dt


class Abilities(Component):
    """4 ability slots (Q, W, E, R)"""

    def __init__(self):
        self.slots = {
            'Q': None,
            'W': None,
            'E': None,
            'R': None
        }
        self.cooldowns = {
            'Q': 0.0,
            'W': 0.0,
            'E': 0.0,
            'R': 0.0
        }

    def can_cast(self, key: str) -> bool:
        """Check if ability can be cast"""
        return self.cooldowns.get(key, float('inf')) <= 0.0

    def cast(self, key: str, cooldown: float):
        """Trigger ability cooldown"""
        self.cooldowns[key] = cooldown

    def update(self, dt: float):
        """Update all cooldowns"""
        for key in self.cooldowns:
            self.cooldowns[key] = max(0.0, self.cooldowns[key] - dt)


# === ENEMY COMPONENTS ===

class Enemy(Component):
    """Marks entity as enemy"""

    def __init__(self, xp_value: int, is_boss: bool = False, enemy_type: str = "basic"):
        self.xp_value = xp_value
        self.is_boss = is_boss
        self.enemy_type = enemy_type  # "basic", "fast", "tank", "ranged"


class AIChase(Component):
    """Simple chase AI - follow player"""

    def __init__(self, speed: float):
        self.speed = speed
        self.target_entity = None  # Will be set to player


class AIRanged(Component):
    """Ranged AI - keep distance and shoot"""

    def __init__(self, speed: float, keep_distance: float, attack_range: float, attack_cooldown: float):
        self.speed = speed
        self.keep_distance = keep_distance
        self.attack_range = attack_range
        self.attack_cooldown = attack_cooldown
        self.time_since_attack = 0.0


# === PROJECTILE COMPONENTS ===

class Projectile(Component):
    """Projectile that damages on hit"""

    def __init__(self, owner_team: str, damage: float, lifetime: float):
        self.owner_team = owner_team
        self.damage = damage
        self.lifetime = lifetime  # Seconds before auto-destroy
        self.time_alive = 0.0

    def update(self, dt: float) -> bool:
        """Update lifetime, return True if expired"""
        self.time_alive += dt
        return self.time_alive >= self.lifetime


# === UTILITY COMPONENTS ===

class Lifetime(Component):
    """Auto-destroy after time"""

    def __init__(self, duration: float):
        self.duration = duration
        self.elapsed = 0.0

    def update(self, dt: float) -> bool:
        """Return True if expired"""
        self.elapsed += dt
        return self.elapsed >= self.duration


class Tag(Component):
    """Generic tag for identification"""

    def __init__(self, tag: str):
        self.tag = tag


# === ABILITY COMPONENTS ===

class HomingProjectile(Component):
    """Projectile that homes in on target"""

    def __init__(self, target, damage: float, speed: float, lifetime: float):
        self.target = target  # Target entity
        self.damage = damage
        self.speed = speed
        self.lifetime = lifetime
        self.time_alive = 0.0

    def update(self, dt: float) -> bool:
        """Update lifetime, return True if expired"""
        self.time_alive += dt
        return self.time_alive >= self.lifetime


class Slowed(Component):
    """Slow effect (reduces movement speed)"""

    def __init__(self, slow_percent: float, duration: float):
        self.slow_percent = slow_percent  # 0.0 to 1.0 (0.7 = 70% slower)
        self.duration = duration
        self.elapsed = 0.0

    def update(self, dt: float) -> bool:
        """Return True if expired"""
        self.elapsed += dt
        return self.elapsed >= self.duration


class Invulnerable(Component):
    """Invulnerability effect (cannot take damage)"""

    def __init__(self, duration: float):
        self.duration = duration
        self.elapsed = 0.0

    def update(self, dt: float) -> bool:
        """Return True if expired"""
        self.elapsed += dt
        return self.elapsed >= self.duration


class ScreenEffect(Component):
    """Full-screen visual effect"""

    def __init__(self, effect_type: str, duration: float):
        self.effect_type = effect_type  # "time_freeze", etc.
        self.duration = duration
        self.elapsed = 0.0

    def update(self, dt: float) -> bool:
        """Return True if expired"""
        self.elapsed += dt
        return self.elapsed >= self.duration


class AudioEvent(Component):
    """Queued audio event to be played"""

    def __init__(self, event_type: str):
        self.event_type = event_type  # "player_hit", "enemy_death", etc.
        self.processed = False


class ParticleComponent(Component):
    """Visual particle effect"""

    def __init__(self, lifetime: float, color: tuple = (255, 255, 255)):
        self.lifetime = lifetime
        self.elapsed = 0.0
        self.color = color
        self.alpha = 255

    def update(self, dt: float) -> bool:
        """Return True if expired"""
        self.elapsed += dt
        # Fade out
        self.alpha = int(255 * (1.0 - self.elapsed / self.lifetime))
        return self.elapsed >= self.lifetime


class PowerUp(Component):
    """Power-up pickup"""

    def __init__(self, powerup_type: str, value: float, lifetime: float = 10.0):
        self.powerup_type = powerup_type  # "health", "damage_boost", "xp"
        self.value = value
        self.lifetime = lifetime
        self.elapsed = 0.0

    def update(self, dt: float) -> bool:
        """Return True if expired"""
        self.elapsed += dt
        return self.elapsed >= self.lifetime


# === WEAPON COMPONENTS ===

class WeaponInventory(Component):
    """Player's weapon collection"""

    def __init__(self):
        # weapon_id -> level (1-5)
        self.weapons = {}  # e.g., {"sword": 2, "magic_missile": 1}

    def has_weapon(self, weapon_id: str) -> bool:
        return weapon_id in self.weapons

    def get_level(self, weapon_id: str) -> int:
        return self.weapons.get(weapon_id, 0)

    def add_weapon(self, weapon_id: str):
        """Add new weapon at level 1"""
        self.weapons[weapon_id] = 1

    def upgrade_weapon(self, weapon_id: str):
        """Increase weapon level"""
        if weapon_id in self.weapons:
            self.weapons[weapon_id] += 1
        else:
            self.weapons[weapon_id] = 1


class WeaponInstance(Component):
    """Active weapon instance"""

    def __init__(self, weapon_id: str, level: int, owner_entity):
        self.weapon_id = weapon_id
        self.level = level
        self.owner_entity = owner_entity
        self.time_since_fire = 0.0


class LevelUpPending(Component):
    """Marks that player needs to choose upgrade"""

    def __init__(self):
        self.choices = []  # List of 3 weapon options


# === GAME DESIGNER NOTE ===
# Components are pure data - no logic
# Logic lives in Systems
# This separation keeps code clean and testable
