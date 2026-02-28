"""
DARK SANCTUM - Boss Ability System
Matrix Team: Game Designer + Developer

Sprint 17: Boss special abilities for unique encounters
"""

import random
import math
from src.core.ecs import System
from src.components.components import *
from config.settings import *
from config.bosses import *


class BossAbilitySystem(System):
    """Handles boss special abilities"""

    def __init__(self, world):
        super().__init__(world)
        self.priority = 28  # After AI, before combat

    def update(self, dt: float):
        """Update all boss abilities"""
        bosses = self.get_entities(Enemy, Position, Health)

        for boss_entity in bosses:
            enemy = boss_entity.get_component(Enemy)

            # Only process bosses with abilities
            if not enemy.is_boss or not enemy.boss_id:
                continue

            # Get boss data
            from config.bosses import get_boss_for_wave, ALL_BOSSES
            boss_data = None
            for b in ALL_BOSSES:
                if b.id == enemy.boss_id:
                    boss_data = b
                    break

            if not boss_data or not boss_data.special_ability:
                continue

            # Initialize ability component if needed
            if not boss_entity.has_component(BossAbility):
                boss_entity.add_component(BossAbility(
                    ability_type=boss_data.special_ability,
                    cooldown=3.0 if boss_data.special_ability == "teleport" else 5.0
                ))

            ability = boss_entity.get_component(BossAbility)
            ability.time_since_cast += dt

            # Cast ability if off cooldown
            if ability.time_since_cast >= ability.cooldown:
                self._cast_ability(boss_entity, boss_data, ability)
                ability.time_since_cast = 0.0

    def _cast_ability(self, boss_entity, boss_data, ability):
        """Cast boss ability"""
        if ability.ability_type == "teleport":
            self._teleport(boss_entity)
        elif ability.ability_type == "aura_slow":
            self._aura_slow(boss_entity)
        elif ability.ability_type == "summon":
            self._summon_minions(boss_entity)
        elif ability.ability_type == "rage":
            self._check_rage(boss_entity)

    def _teleport(self, boss_entity):
        """Void Reaver: Teleport to random position"""
        # Find player
        player_entities = self.get_entities(Player, Position)
        if not player_entities:
            return

        player_pos = player_entities[0].get_component(Position)
        boss_pos = boss_entity.get_component(Position)

        # Teleport to position near player (but not too close)
        angle = random.uniform(0, 2 * math.pi)
        distance = random.uniform(200, 350)  # Medium distance

        new_x = player_pos.x + math.cos(angle) * distance
        new_y = player_pos.y + math.sin(angle) * distance

        # Clamp to screen
        new_x = max(100, min(WINDOW_WIDTH - 100, new_x))
        new_y = max(100, min(WINDOW_HEIGHT - 100, new_y))

        # Teleport particles at old position
        from src.systems.particle_system import create_death_particles
        sprite = boss_entity.get_component(Sprite)
        create_death_particles(self.world, boss_pos.x, boss_pos.y, (80, 40, 120), 20)

        # Update position
        boss_pos.x = new_x
        boss_pos.y = new_y

        # Teleport particles at new position
        create_death_particles(self.world, new_x, new_y, (80, 40, 120), 20)

        # Brief invulnerability (0.5s)
        boss_entity.add_component(Invulnerable(0.5))

        # Teleport sound
        audio_event = self.world.create_entity()
        audio_event.add_component(AudioEvent('ability_cast'))

        print("👤 Void Reaver TELEPORTED!")

    def _aura_slow(self, boss_entity):
        """Frost Colossus: Slow all nearby entities"""
        boss_pos = boss_entity.get_component(Position)

        # Find player
        player_entities = self.get_entities(Player, Position)
        if not player_entities:
            return

        player_entity = player_entities[0]
        player_pos = player_entity.get_component(Position)

        # Check distance
        dx = player_pos.x - boss_pos.x
        dy = player_pos.y - boss_pos.y
        dist = math.sqrt(dx * dx + dy * dy)

        # Apply slow if in range (300px)
        if dist <= 300:
            # Add/refresh slow component
            if player_entity.has_component(Slowed):
                # Refresh duration
                slowed = player_entity.get_component(Slowed)
                slowed.elapsed = 0.0
            else:
                # Add new slow
                player_entity.add_component(Slowed(0.5, 1.5))  # 50% slow for 1.5s

    def _summon_minions(self, boss_entity):
        """Plague Herald: Summon 3 imp minions"""
        boss_pos = boss_entity.get_component(Position)

        # Spawn 3 imps around boss
        for i in range(3):
            angle = (2 * math.pi / 3) * i + random.uniform(-0.3, 0.3)
            distance = 80

            x = boss_pos.x + math.cos(angle) * distance
            y = boss_pos.y + math.sin(angle) * distance

            # Clamp to screen
            x = max(50, min(WINDOW_WIDTH - 50, x))
            y = max(50, min(WINDOW_HEIGHT - 50, y))

            # Create imp (weak fast enemy)
            from src.entities.factory import EntityFactory
            factory = EntityFactory(self.world)
            factory.create_enemy(x, y, enemy_type="fast", is_elite=False)

        # Summon particles
        from src.systems.particle_system import create_death_particles
        create_death_particles(self.world, boss_pos.x, boss_pos.y, (120, 200, 80), 30)

        # Summon sound
        audio_event = self.world.create_entity()
        audio_event.add_component(AudioEvent('enemy_spawn'))

        print("☠️ Plague Herald SUMMONED 3 imps!")

    def _check_rage(self, boss_entity):
        """Inferno Lord: Enrage when below 30% HP"""
        health = boss_entity.get_component(Health)
        damage = boss_entity.get_component(Damage)
        ai = boss_entity.get_component(AIChase)

        # Check if below 30% HP
        if health.percent <= 0.3:
            # Add rage component if not already enraged
            if not boss_entity.has_component(BossRage):
                boss_entity.add_component(BossRage())

                # Boost damage and speed by 50%
                damage.amount *= 1.5
                ai.speed *= 1.5

                # Visual feedback (change color to bright red)
                sprite = boss_entity.get_component(Sprite)
                sprite.color = (255, 80, 20)  # Bright burning orange
                sprite.glow_color = (255, 150, 50)

                # Rage particles
                boss_pos = boss_entity.get_component(Position)
                from src.systems.particle_system import create_death_particles
                create_death_particles(self.world, boss_pos.x, boss_pos.y, (255, 100, 20), 50)

                # Rage sound
                audio_event = self.world.create_entity()
                audio_event.add_component(AudioEvent('boss_spawn'))

                # Screen shake
                from src.systems.screen_effects import trigger_screen_shake
                trigger_screen_shake(self.world, 25.0, 0.6)

                print("🔥 Inferno Lord ENRAGED! (+50% damage & speed)")


class BossAbility(Component):
    """Boss ability state"""

    def __init__(self, ability_type: str, cooldown: float):
        self.ability_type = ability_type  # "teleport", "aura_slow", "summon", "rage"
        self.cooldown = cooldown
        self.time_since_cast = 0.0


class BossRage(Component):
    """Marks boss as enraged (for Inferno Lord)"""

    def __init__(self):
        pass


# === GAME DESIGNER NOTE ===
# Boss abilities create unique encounters:
# - Void Reaver: Unpredictable teleports, hard to pin down
# - Frost Colossus: Positioning challenge, can't escape easily
# - Plague Herald: Add management, kill minions or focus boss?
# - Inferno Lord: Phase 2 escalation, dangerous when low
#
# Each boss requires different tactics!
# Sprint 17: 4 unique boss mechanics
