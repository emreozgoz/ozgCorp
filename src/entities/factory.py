"""
DARK SANCTUM - Entity Factory
Matrix Team: Game Designer + Developer

Clean entity creation helpers
"""

from src.core.ecs import Entity, World
from src.components.components import *
from src.components.character_classes import *
from config.settings import *


class EntityFactory:
    """Factory for creating game entities"""

    def __init__(self, world: World):
        self.world = world

    def create_player(self, x: float, y: float, character_class: CharacterClass = SHADOW_KNIGHT) -> Entity:
        """Create player entity with chosen class"""
        player = self.world.create_entity()

        # Core components (use class stats)
        player.add_component(Position(x, y))
        player.add_component(Velocity(0, 0))
        player.add_component(Size(PLAYER_SIZE, PLAYER_SIZE))
        player.add_component(Sprite(character_class.color, radius=PLAYER_SIZE / 2))

        # Combat components (use class stats)
        player.add_component(Health(character_class.health))
        player.add_component(Damage(character_class.damage))
        player.add_component(Team("player"))

        # Player-specific
        player_comp = Player(character_class.name)
        player_comp.move_speed = character_class.speed  # Apply class speed
        player.add_component(player_comp)
        player.add_component(Experience())
        player.add_component(AutoAttack(
            damage=AUTO_ATTACK_DAMAGE,
            range_=AUTO_ATTACK_RANGE,
            cooldown=AUTO_ATTACK_COOLDOWN,
            projectile_speed=AUTO_ATTACK_SPEED
        ))
        player.add_component(Abilities())

        # Tags
        player.add_component(Tag("player"))

        print(f"🎮 {character_class.name} spawned at ({x}, {y})")
        print(f"   HP: {character_class.health} | DMG: {character_class.damage} | SPD: {character_class.speed}")
        print(f"   Passive: {character_class.passive_name}")
        return player

    def create_enemy(self, x: float, y: float, health_multiplier: float = 1.0) -> Entity:
        """Create enemy entity with optional health scaling"""
        enemy = self.world.create_entity()

        # Core components
        enemy.add_component(Position(x, y))
        enemy.add_component(Velocity(0, 0))
        enemy.add_component(Size(ENEMY_SIZE, ENEMY_SIZE))
        enemy.add_component(Sprite(ENEMY_COLOR, radius=ENEMY_SIZE / 2))

        # Combat components
        scaled_health = ENEMY_BASE_HEALTH * health_multiplier
        enemy.add_component(Health(scaled_health))
        enemy.add_component(Damage(ENEMY_BASE_DAMAGE))
        enemy.add_component(Team("enemy"))

        # Enemy-specific
        enemy.add_component(Enemy(xp_value=ENEMY_XP_VALUE))
        enemy.add_component(AIChase(speed=ENEMY_BASE_SPEED))

        # Tags
        enemy.add_component(Tag("enemy"))

        return enemy

    def create_projectile(self, x: float, y: float, vx: float, vy: float,
                         team: str, damage: float, color: tuple) -> Entity:
        """Create projectile entity"""
        projectile = self.world.create_entity()

        projectile.add_component(Position(x, y))
        projectile.add_component(Velocity(vx, vy))
        projectile.add_component(Size(8, 8))
        projectile.add_component(Sprite(color, radius=4))
        projectile.add_component(Projectile(team, damage, lifetime=3.0))
        projectile.add_component(Tag("projectile"))

        return projectile


# === GAME DESIGNER NOTE ===
# Factory pattern keeps entity creation consistent and maintainable
# Easy to add new entity types (bosses, power-ups, etc.)
# Health multiplier allows scaling enemy difficulty over time
