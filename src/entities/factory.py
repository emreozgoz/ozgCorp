"""
DARK SANCTUM - Entity Factory
Matrix Team: Game Designer + Developer

Clean entity creation helpers
"""

from src.core.ecs import Entity, World
from src.components.components import *
from src.components.character_classes import *
from config.settings import *
from config.difficulty import DifficultySettings


class EntityFactory:
    """Factory for creating game entities"""

    def __init__(self, world: World):
        self.world = world

    def create_player(self, x: float, y: float, character_class: CharacterClass = SHADOW_KNIGHT) -> Entity:
        """Create player entity with chosen class"""
        player = self.world.create_entity()

        # Get difficulty multipliers
        multipliers = DifficultySettings.get_multipliers()

        # Core components (use class stats with difficulty multipliers)
        player.add_component(Position(x, y))
        player.add_component(Velocity(0, 0))
        player.add_component(Size(PLAYER_SIZE, PLAYER_SIZE))
        player.add_component(Sprite(character_class.color, radius=PLAYER_SIZE / 2))

        # Combat components (apply difficulty multipliers)
        player.add_component(Health(character_class.health * multipliers['player_health']))
        player.add_component(Damage(character_class.damage * multipliers['player_damage']))
        player.add_component(Team("player"))

        # Player-specific
        player_comp = Player(character_class.name)
        player_comp.move_speed = character_class.speed * multipliers['player_speed']  # Apply class speed + difficulty
        player.add_component(player_comp)
        player.add_component(Experience())
        player.add_component(AutoAttack(
            damage=AUTO_ATTACK_DAMAGE * multipliers['player_damage'],
            range_=AUTO_ATTACK_RANGE,
            cooldown=AUTO_ATTACK_COOLDOWN,
            projectile_speed=AUTO_ATTACK_SPEED
        ))
        player.add_component(Abilities())
        player.add_component(WeaponInventory())  # Weapon progression system

        # Tags
        player.add_component(Tag("player"))

        print(f"🎮 {character_class.name} spawned at ({x}, {y})")
        print(f"   HP: {character_class.health * multipliers['player_health']:.0f} | DMG: {character_class.damage * multipliers['player_damage']:.0f} | SPD: {character_class.speed * multipliers['player_speed']:.0f}")
        print(f"   Passive: {character_class.passive_name}")
        print(f"   Difficulty: {DifficultySettings.get_difficulty_name()}")
        return player

    def create_enemy(self, x: float, y: float, health_multiplier: float = 1.0, enemy_type: str = "basic") -> Entity:
        """Create enemy entity with optional health scaling and type"""
        enemy = self.world.create_entity()

        # Get difficulty multipliers
        multipliers = DifficultySettings.get_multipliers()

        # Type-specific stats
        if enemy_type == "fast":
            return self._create_fast_enemy(x, y, health_multiplier)
        elif enemy_type == "tank":
            return self._create_tank_enemy(x, y, health_multiplier)
        elif enemy_type == "ranged":
            return self._create_ranged_enemy(x, y, health_multiplier)
        else:
            # Basic enemy
            enemy.add_component(Position(x, y))
            enemy.add_component(Velocity(0, 0))
            enemy.add_component(Size(ENEMY_SIZE, ENEMY_SIZE))
            enemy.add_component(Sprite(ENEMY_COLOR, radius=ENEMY_SIZE / 2))

            # Combat components (apply difficulty)
            scaled_health = ENEMY_BASE_HEALTH * health_multiplier * multipliers['enemy_health']
            enemy.add_component(Health(scaled_health))
            enemy.add_component(Damage(ENEMY_BASE_DAMAGE * multipliers['enemy_damage']))
            enemy.add_component(Team("enemy"))

            # Enemy-specific
            enemy.add_component(Enemy(xp_value=ENEMY_XP_VALUE, enemy_type="basic"))
            enemy.add_component(AIChase(speed=ENEMY_BASE_SPEED * multipliers['enemy_speed']))

            # Tags
            enemy.add_component(Tag("enemy"))

            return enemy

    def _create_fast_enemy(self, x: float, y: float, health_multiplier: float = 1.0) -> Entity:
        """Create fast enemy (Imp)"""
        enemy = self.world.create_entity()

        multipliers = DifficultySettings.get_multipliers()
        size = ENEMY_SIZE * FAST_ENEMY_SIZE_MULT

        enemy.add_component(Position(x, y))
        enemy.add_component(Velocity(0, 0))
        enemy.add_component(Size(size, size))
        enemy.add_component(Sprite(FAST_ENEMY_COLOR, radius=size / 2))
        enemy.add_component(Health(ENEMY_BASE_HEALTH * FAST_ENEMY_HEALTH_MULT * health_multiplier * multipliers['enemy_health']))
        enemy.add_component(Damage(ENEMY_BASE_DAMAGE * FAST_ENEMY_DAMAGE_MULT * multipliers['enemy_damage']))
        enemy.add_component(Team("enemy"))
        enemy.add_component(Enemy(xp_value=int(ENEMY_XP_VALUE * FAST_ENEMY_XP_MULT), enemy_type="fast"))
        enemy.add_component(AIChase(speed=ENEMY_BASE_SPEED * FAST_ENEMY_SPEED_MULT * multipliers['enemy_speed']))
        enemy.add_component(Tag("enemy"))

        return enemy

    def _create_tank_enemy(self, x: float, y: float, health_multiplier: float = 1.0) -> Entity:
        """Create tank enemy (Golem)"""
        enemy = self.world.create_entity()

        multipliers = DifficultySettings.get_multipliers()
        size = ENEMY_SIZE * TANK_ENEMY_SIZE_MULT

        enemy.add_component(Position(x, y))
        enemy.add_component(Velocity(0, 0))
        enemy.add_component(Size(size, size))
        enemy.add_component(Sprite(TANK_ENEMY_COLOR, radius=size / 2))
        enemy.add_component(Health(ENEMY_BASE_HEALTH * TANK_ENEMY_HEALTH_MULT * health_multiplier * multipliers['enemy_health']))
        enemy.add_component(Damage(ENEMY_BASE_DAMAGE * TANK_ENEMY_DAMAGE_MULT * multipliers['enemy_damage']))
        enemy.add_component(Team("enemy"))
        enemy.add_component(Enemy(xp_value=int(ENEMY_XP_VALUE * TANK_ENEMY_XP_MULT), enemy_type="tank"))
        enemy.add_component(AIChase(speed=ENEMY_BASE_SPEED * TANK_ENEMY_SPEED_MULT * multipliers['enemy_speed']))
        enemy.add_component(Tag("enemy"))

        return enemy

    def _create_ranged_enemy(self, x: float, y: float, health_multiplier: float = 1.0) -> Entity:
        """Create ranged enemy (Wraith)"""
        enemy = self.world.create_entity()

        multipliers = DifficultySettings.get_multipliers()
        size = ENEMY_SIZE * RANGED_ENEMY_SIZE_MULT

        enemy.add_component(Position(x, y))
        enemy.add_component(Velocity(0, 0))
        enemy.add_component(Size(size, size))
        enemy.add_component(Sprite(RANGED_ENEMY_COLOR, radius=size / 2))
        enemy.add_component(Health(ENEMY_BASE_HEALTH * RANGED_ENEMY_HEALTH_MULT * health_multiplier * multipliers['enemy_health']))
        enemy.add_component(Damage(ENEMY_BASE_DAMAGE * RANGED_ENEMY_DAMAGE_MULT * multipliers['enemy_damage']))
        enemy.add_component(Team("enemy"))
        enemy.add_component(Enemy(xp_value=int(ENEMY_XP_VALUE * RANGED_ENEMY_XP_MULT), enemy_type="ranged"))
        enemy.add_component(AIRanged(
            speed=ENEMY_BASE_SPEED * RANGED_ENEMY_SPEED_MULT * multipliers['enemy_speed'],
            keep_distance=RANGED_ENEMY_KEEP_DISTANCE,
            attack_range=RANGED_ENEMY_ATTACK_RANGE,
            attack_cooldown=RANGED_ENEMY_ATTACK_COOLDOWN
        ))
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
