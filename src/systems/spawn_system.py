"""
DARK SANCTUM - Enemy Spawning System
Matrix Team: Game Designer

Wave-based enemy spawning like Vampire Survivors but MORE tactical
"""

import math
import random
from src.core.ecs import System
from src.components.components import *
from config.settings import *


class WaveSpawnSystem(System):
    """Spawn waves of enemies"""

    def __init__(self, world):
        super().__init__(world)
        self.priority = 50
        self.time_since_wave = 0.0
        self.current_wave = 0
        self.enemies_this_wave = WAVE_INITIAL_ENEMIES

    def update(self, dt: float):
        """Update spawn timer"""
        self.time_since_wave += dt

        if self.time_since_wave >= WAVE_SPAWN_INTERVAL:
            self._spawn_wave()
            self.time_since_wave = 0.0

    def _spawn_wave(self):
        """Spawn a new wave of enemies"""
        self.current_wave += 1

        # Find player position
        player_entities = self.get_entities(Player, Position)
        if not player_entities:
            return

        player_pos = player_entities[0].get_component(Position)

        # Check if this is a boss wave
        is_boss_wave = (self.current_wave % BOSS_WAVE_INTERVAL == 0)

        if is_boss_wave:
            # Spawn boss
            self._spawn_boss(player_pos)
            print(f"💀 WAVE {self.current_wave} - BOSS WAVE!")
        else:
            # Spawn varied enemies (60% basic, 20% fast, 15% tank, 5% ranged)
            for i in range(int(self.enemies_this_wave)):
                roll = random.random()
                if roll < 0.60:
                    enemy_type = "basic"
                elif roll < 0.80:
                    enemy_type = "fast"
                elif roll < 0.95:
                    enemy_type = "tank"
                else:
                    enemy_type = "ranged"

                self._spawn_enemy(player_pos, enemy_type)

            # Scale difficulty
            self.enemies_this_wave *= WAVE_SCALING

            print(f"🌊 WAVE {self.current_wave} - {int(self.enemies_this_wave)} enemies")

    def _spawn_enemy(self, player_pos: Position, enemy_type: str = "basic"):
        """Spawn single enemy off-screen"""
        # Random angle
        angle = random.uniform(0, 2 * math.pi)

        # Random distance (spawn off-screen)
        distance = random.uniform(SPAWN_DISTANCE_MIN, SPAWN_DISTANCE_MAX)

        # Calculate position
        x = player_pos.x + math.cos(angle) * distance
        y = player_pos.y + math.sin(angle) * distance

        # Clamp to screen bounds with padding
        x = max(50, min(WINDOW_WIDTH - 50, x))
        y = max(50, min(WINDOW_HEIGHT - 50, y))

        # Create enemy using factory
        from src.entities.factory import EntityFactory
        factory = EntityFactory(self.world)
        factory.create_enemy(x, y, enemy_type=enemy_type)

    def _spawn_boss(self, player_pos: Position):
        """Spawn boss enemy"""
        # Spawn in front of player
        angle = random.uniform(0, 2 * math.pi)
        distance = 400  # Fixed distance

        x = player_pos.x + math.cos(angle) * distance
        y = player_pos.y + math.sin(angle) * distance

        # Clamp to screen bounds
        x = max(100, min(WINDOW_WIDTH - 100, x))
        y = max(100, min(WINDOW_HEIGHT - 100, y))

        # Create boss entity
        boss = self.world.create_entity()
        boss_size = ENEMY_SIZE * BOSS_SIZE_MULTIPLIER

        boss.add_component(Position(x, y))
        boss.add_component(Velocity(0, 0))
        boss.add_component(Size(boss_size, boss_size))
        boss.add_component(Sprite(BOSS_COLOR, radius=boss_size / 2))
        boss.add_component(Health(ENEMY_BASE_HEALTH * BOSS_HEALTH_MULTIPLIER))
        boss.add_component(Damage(ENEMY_BASE_DAMAGE * BOSS_DAMAGE_MULTIPLIER))
        boss.add_component(Team("enemy"))
        boss.add_component(Enemy(
            xp_value=ENEMY_XP_VALUE * BOSS_XP_MULTIPLIER,
            is_boss=True
        ))
        boss.add_component(AIChase(speed=ENEMY_BASE_SPEED * BOSS_SPEED_MULTIPLIER))
        boss.add_component(Tag("boss"))

        # Boss spawn sound
        audio_event = self.world.create_entity()
        audio_event.add_component(AudioEvent('boss_spawn'))

        print(f"💀 BLOOD TITAN SPAWNED! Health: {ENEMY_BASE_HEALTH * BOSS_HEALTH_MULTIPLIER}")


class AISystem(System):
    """Simple chase AI for enemies"""

    def __init__(self, world):
        super().__init__(world)
        self.priority = 25

    def update(self, dt: float):
        """Update AI"""
        # Find player
        player_entities = self.get_entities(Player, Position)
        if not player_entities:
            return

        player_pos = player_entities[0].get_component(Position)

        # Update all chase AI
        chase_entities = self.get_entities(AIChase, Position, Velocity)

        for entity in chase_entities:
            # Check if slowed
            slow_mult = 1.0
            if entity.has_component(Slowed):
                slowed = entity.get_component(Slowed)
                slow_mult = 1.0 - slowed.slow_percent

            ai = entity.get_component(AIChase)
            pos = entity.get_component(Position)
            vel = entity.get_component(Velocity)

            # Calculate direction to player
            dx = player_pos.x - pos.x
            dy = player_pos.y - pos.y
            dist = math.sqrt(dx * dx + dy * dy)

            if dist > 0:
                # Normalize and apply speed (with slow)
                vel.vx = (dx / dist) * ai.speed * slow_mult
                vel.vy = (dy / dist) * ai.speed * slow_mult

        # Update ranged AI
        ranged_entities = self.get_entities(AIRanged, Position, Velocity, Team, Damage)

        for entity in ranged_entities:
            # Check if slowed
            slow_mult = 1.0
            if entity.has_component(Slowed):
                slowed = entity.get_component(Slowed)
                slow_mult = 1.0 - slowed.slow_percent

            ai = entity.get_component(AIRanged)
            pos = entity.get_component(Position)
            vel = entity.get_component(Velocity)
            team = entity.get_component(Team)
            damage = entity.get_component(Damage)

            # Calculate distance to player
            dx = player_pos.x - pos.x
            dy = player_pos.y - pos.y
            dist = math.sqrt(dx * dx + dy * dy)

            if dist > 0:
                # If too close, move away
                if dist < ai.keep_distance:
                    # Move away from player
                    vel.vx = -(dx / dist) * ai.speed * slow_mult
                    vel.vy = -(dy / dist) * ai.speed * slow_mult
                # If far enough, stop
                elif dist > ai.keep_distance + 50:
                    # Move toward player (but slowly)
                    vel.vx = (dx / dist) * ai.speed * 0.5 * slow_mult
                    vel.vy = (dy / dist) * ai.speed * 0.5 * slow_mult
                else:
                    # Stay still
                    vel.vx = 0
                    vel.vy = 0

                # Attack if in range
                ai.time_since_attack += dt
                if dist <= ai.attack_range and ai.time_since_attack >= ai.attack_cooldown:
                    self._shoot_projectile(pos, player_pos, team.team, damage.amount)
                    ai.time_since_attack = 0.0

    def _shoot_projectile(self, from_pos: Position, to_pos: Position, team: str, damage: float):
        """Create enemy projectile"""
        # Calculate direction
        dx = to_pos.x - from_pos.x
        dy = to_pos.y - from_pos.y
        dist = math.sqrt(dx * dx + dy * dy)

        if dist == 0:
            return

        dx /= dist
        dy /= dist

        # Create projectile
        speed = 200  # Enemy projectile speed
        projectile = self.world.create_entity()
        projectile.add_component(Position(from_pos.x, from_pos.y))
        projectile.add_component(Velocity(dx * speed, dy * speed))
        projectile.add_component(Size(6, 6))
        projectile.add_component(Sprite(RANGED_ENEMY_COLOR, radius=3))
        projectile.add_component(Projectile(team, damage, lifetime=5.0))
        projectile.add_component(Tag("projectile"))


class DeathSystem(System):
    """Handle entity death"""

    def __init__(self, world):
        super().__init__(world)
        self.priority = 60

    def update(self, dt: float):
        """Remove dead entities"""
        entities = self.get_entities(Health)

        for entity in entities:
            health = entity.get_component(Health)

            if not health.is_alive:
                # Award XP if enemy
                enemy = entity.get_component(Enemy)
                if enemy:
                    self._award_xp(enemy.xp_value)

                    # Enemy death sound
                    audio_event = self.world.create_entity()
                    audio_event.add_component(AudioEvent('enemy_death'))

                    # Chance to spawn power-up
                    pos = entity.get_component(Position)
                    if pos and random.random() < POWERUP_DROP_CHANCE:
                        from src.systems.powerup_system import spawn_powerup
                        spawn_powerup(self.world, pos.x, pos.y)

                # Player death sound
                player = entity.get_component(Player)
                if player:
                    audio_event = self.world.create_entity()
                    audio_event.add_component(AudioEvent('player_hit'))

                # Create death particles
                pos = entity.get_component(Position)
                sprite = entity.get_component(Sprite)
                if pos and sprite:
                    from src.systems.particle_system import create_death_particles
                    particle_count = 30 if (enemy and enemy.is_boss) else 15
                    create_death_particles(self.world, pos.x, pos.y, sprite.color, particle_count)

                # Destroy entity
                self.world.destroy_entity(entity)

    def _award_xp(self, amount: int):
        """Give XP to player"""
        player_entities = self.get_entities(Player, Experience)

        for player in player_entities:
            xp = player.get_component(Experience)
            if xp.add_xp(amount):
                # Level up particles
                pos = player.get_component(Position)
                if pos:
                    from src.systems.particle_system import create_level_up_particles
                    create_level_up_particles(self.world, pos.x, pos.y, 40)

                # Level up sound
                audio_event = self.world.create_entity()
                audio_event.add_component(AudioEvent('level_up'))

                print(f"⬆️ LEVEL UP! Now level {xp.level}")


# === GAME DESIGNER NOTE ===
# Wave spawning creates escalating difficulty:
# - Enemies spawn off-screen (surprise factor)
# - Wave count scales exponentially
# - Simple chase AI keeps gameplay focused
# - Death system handles cleanup and XP rewards
