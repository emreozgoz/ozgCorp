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
    """Visual representation (Sprint 26: Now supports sprite images!)"""

    def __init__(self, color: tuple, radius: Optional[float] = None, sprite_key: Optional[str] = None):
        self.color = color
        self.radius = radius  # If not None, draw as circle (fallback)
        self.sprite_key = sprite_key  # Sprite key for asset_manager lookup


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
        # Apply difficulty multiplier
        from config.difficulty import DifficultySettings
        multipliers = DifficultySettings.get_multipliers()
        actual_xp = amount * multipliers['xp_gain']

        self.current_xp += actual_xp
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

    def __init__(self, xp_value: int, is_boss: bool = False, enemy_type: str = "basic", is_elite: bool = False, boss_id: str = None):
        self.xp_value = xp_value
        self.is_boss = is_boss
        self.enemy_type = enemy_type  # "basic", "fast", "tank", "ranged"
        self.is_elite = is_elite  # Elite variant (2x HP, 1.5x damage, guaranteed drop)
        self.boss_id = boss_id  # Boss type ID from bosses.py (Sprint 15)


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


class GuaranteedDrop(Component):
    """Marks entity to drop loot on death (Sprint 15)"""

    def __init__(self, drop_type: str = "powerup"):
        self.drop_type = drop_type  # "powerup", "weapon", etc.


# === WEAPON COMPONENTS ===

class WeaponInventory(Component):
    """Player's weapon collection"""

    def __init__(self):
        # weapon_id -> level (1-5)
        self.weapons = {}  # e.g., {"sword": 2, "magic_missile": 1}
        # Track evolved weapons
        self.evolved_weapons = set()  # e.g., {"reapers_embrace"}

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

    def is_evolved(self, weapon_id: str) -> bool:
        """Check if weapon has been evolved"""
        return weapon_id in self.evolved_weapons

    def evolve_weapon(self, base_weapon_id: str, evolved_id: str):
        """Evolve weapon to its final form"""
        # Remove base weapon, add evolved version
        if base_weapon_id in self.weapons:
            del self.weapons[base_weapon_id]
        self.weapons[evolved_id] = 6  # Evolved weapons are "level 6"
        self.evolved_weapons.add(evolved_id)

    def can_evolve_weapon(self, weapon_id: str) -> bool:
        """Check if weapon is at max level and can evolve"""
        return self.get_level(weapon_id) >= 5 and not self.is_evolved(weapon_id)


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


# === MAP COMPONENTS ===

class CurrentMap(Component):
    """Tracks current active map"""

    def __init__(self, map_id: str):
        self.map_id = map_id


class EnvironmentalHazard(Component):
    """Environmental hazard that damages player"""

    def __init__(self, hazard_type: str, damage: float, damage_interval: float):
        self.hazard_type = hazard_type  # "blood_pool", "spike_trap"
        self.damage = damage
        self.damage_interval = damage_interval
        self.time_since_damage = 0.0
        self.is_active = True  # For spike traps (toggle on/off)
        self.active_timer = 0.0  # Spike trap timing


# === SPRITE & ANIMATION COMPONENTS (Sprint 21) ===

class SpriteComponent(Component):
    """Sprite-based visual representation"""

    def __init__(self, sprite_key: str, size: int = 32):
        self.sprite_key = sprite_key  # Key for AssetManager lookup
        self.size = size
        self.flip_x = False
        self.flip_y = False
        self.alpha = 255  # 0-255 transparency
        self.rotation = 0.0  # Rotation angle in degrees

class AnimationComponent(Component):
    """Animation state and control"""

    def __init__(self, animation_name: str = "idle", frame_duration: float = 0.1):
        self.current_animation = animation_name
        self.animations = {}  # Dict[str, List[pygame.Surface]]
        self.current_frame = 0
        self.frame_duration = frame_duration  # Seconds per frame
        self.time_since_frame = 0.0
        self.loop = True
        self.playing = True

    def add_animation(self, name: str, frames: list):
        """Add animation frames"""
        self.animations[name] = frames

    def play(self, name: str, loop: bool = True):
        """Start playing an animation"""
        if name in self.animations and name != self.current_animation:
            self.current_animation = name
            self.current_frame = 0
            self.time_since_frame = 0.0
            self.loop = loop
            self.playing = True

    def get_current_frame(self):
        """Get current animation frame"""
        if self.current_animation in self.animations:
            frames = self.animations[self.current_animation]
            if frames:
                return frames[self.current_frame]
        return None


# === VFX COMPONENTS (Sprint 23) ===

class TrailEffect(Component):
    """Trail effect for projectiles and weapons"""

    def __init__(self, color: tuple, length: int = 5, fade_speed: float = 0.1):
        self.color = color
        self.length = length  # Number of trail segments
        self.fade_speed = fade_speed
        self.positions = []  # List of (x, y, alpha) tuples

    def add_position(self, x: float, y: float):
        """Add new position to trail"""
        self.positions.append([x, y, 255])
        if len(self.positions) > self.length:
            self.positions.pop(0)

    def update(self, dt: float):
        """Fade out trail segments"""
        for pos in self.positions:
            pos[2] = max(0, pos[2] - self.fade_speed * 255 * dt)


class GlowEffect(Component):
    """Pulsing glow effect"""

    def __init__(self, color: tuple, intensity: float = 1.0, pulse_speed: float = 2.0):
        self.color = color
        self.intensity = intensity  # 0.0 to 1.0
        self.pulse_speed = pulse_speed
        self.time = 0.0

    def update(self, dt: float):
        """Update pulse animation"""
        self.time += dt * self.pulse_speed

    def get_current_intensity(self) -> float:
        """Get pulsing intensity"""
        import math
        return self.intensity * (0.5 + 0.5 * math.sin(self.time))


class ImpactEffect(Component):
    """Hit impact visual effect"""

    def __init__(self, effect_type: str = "spark", duration: float = 0.2):
        self.effect_type = effect_type  # "spark", "explosion", "slash"
        self.duration = duration
        self.elapsed = 0.0
        self.scale = 1.0

    def update(self, dt: float) -> bool:
        """Return True if expired"""
        self.elapsed += dt
        # Scale up then fade
        if self.elapsed < self.duration * 0.3:
            self.scale = 1.0 + (self.elapsed / (self.duration * 0.3)) * 0.5
        return self.elapsed >= self.duration


class ScreenDistortion(Component):
    """Screen shake/distortion effect"""

    def __init__(self, intensity: float, duration: float):
        self.intensity = intensity
        self.duration = duration
        self.elapsed = 0.0

    def update(self, dt: float) -> bool:
        """Return True if expired"""
        self.elapsed += dt
        return self.elapsed >= self.duration

    def get_current_intensity(self) -> float:
        """Get decreasing intensity"""
        return self.intensity * (1.0 - self.elapsed / self.duration)


# === GAME DESIGNER NOTE ===
# Components are pure data - no logic
# Logic lives in Systems
# This separation keeps code clean and testable
#
# Sprint 21: Added sprite & animation components for visual enhancement
# Sprint 23: Added advanced VFX components (trails, glows, impacts, distortion)
