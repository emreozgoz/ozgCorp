"""
DARK SANCTUM - Combat System
Matrix Team: Game Designer + Developer

Auto-attack, collision damage, projectiles
"""

import math
import pygame
from src.core.ecs import System
from src.components.components import *
from config.settings import *


class AutoAttackSystem(System):
    """Handle player auto-attack"""

    def __init__(self, world):
        super().__init__(world)
        self.priority = 30

    def update(self, dt: float):
        """Update auto-attack"""
        attackers = self.get_entities(AutoAttack, Position, Team)

        for attacker in attackers:
            auto_attack = attacker.get_component(AutoAttack)
            pos = attacker.get_component(Position)
            team = attacker.get_component(Team)

            # Update cooldown
            auto_attack.update(dt)

            if not auto_attack.can_attack():
                continue

            # Find nearest enemy
            target = self._find_nearest_enemy(pos, team.team, auto_attack.range)

            if target:
                target_pos = target.get_component(Position)
                self._create_projectile(pos, target_pos, auto_attack, team.team)
                auto_attack.attack()

    def _find_nearest_enemy(self, pos: Position, team: str, range_: float):
        """Find nearest enemy within range"""
        enemies = self.get_entities(Team, Position, Health)

        nearest = None
        nearest_dist = float('inf')

        for enemy in enemies:
            enemy_team = enemy.get_component(Team)
            if enemy_team.team == team:
                continue  # Same team

            enemy_health = enemy.get_component(Health)
            if not enemy_health.is_alive:
                continue

            enemy_pos = enemy.get_component(Position)
            dist = math.sqrt((pos.x - enemy_pos.x) ** 2 + (pos.y - enemy_pos.y) ** 2)

            if dist <= range_ and dist < nearest_dist:
                nearest = enemy
                nearest_dist = dist

        return nearest

    def _create_projectile(self, from_pos: Position, to_pos: Position,
                          auto_attack: AutoAttack, team: str):
        """Create projectile entity"""
        # Calculate direction
        dx = to_pos.x - from_pos.x
        dy = to_pos.y - from_pos.y
        dist = math.sqrt(dx * dx + dy * dy)

        if dist == 0:
            return

        dx /= dist
        dy /= dist

        # Create projectile entity
        projectile = self.world.create_entity()
        projectile.add_component(Position(from_pos.x, from_pos.y))
        projectile.add_component(Velocity(
            dx * auto_attack.projectile_speed,
            dy * auto_attack.projectile_speed
        ))
        projectile.add_component(Size(8, 8))
        projectile.add_component(Sprite(AUTO_ATTACK_COLOR, radius=4))
        projectile.add_component(Projectile(team, auto_attack.damage, lifetime=3.0))
        projectile.add_component(Tag("projectile"))


class ProjectileSystem(System):
    """Handle projectile collisions and lifetime"""

    def __init__(self, world):
        super().__init__(world)
        self.priority = 35

    def update(self, dt: float):
        """Update projectiles"""
        projectiles = self.get_entities(Projectile, Position, Size)

        for proj in projectiles:
            projectile = proj.get_component(Projectile)

            # Update lifetime
            if projectile.update(dt):
                self.world.destroy_entity(proj)
                continue

            # Check collision with enemies
            self._check_collision(proj)

    def _check_collision(self, projectile_entity):
        """Check if projectile hit an enemy"""
        proj_pos = projectile_entity.get_component(Position)
        proj_size = projectile_entity.get_component(Size)
        projectile = projectile_entity.get_component(Projectile)

        # Get potential targets
        entities = self.get_entities(Team, Position, Size, Health)

        for entity in entities:
            team = entity.get_component(Team)

            # Skip same team
            if team.team == projectile.owner_team:
                continue

            # Check collision
            entity_pos = entity.get_component(Position)
            entity_size = entity.get_component(Size)

            if self._aabb_collision(proj_pos, proj_size, entity_pos, entity_size):
                # Check if target is invulnerable
                if entity.has_component(Invulnerable):
                    continue

                # Deal damage
                health = entity.get_component(Health)
                health.damage(projectile.damage)

                # Create damage number
                from src.systems.screen_effects import create_damage_number
                entity_pos = entity.get_component(Position)
                create_damage_number(self.world, entity_pos.x, entity_pos.y, projectile.damage)

                # Track damage stats (if player projectile)
                if projectile.owner_team == "player":
                    from src.systems.stats_system import GameStats
                    player_entities = self.get_entities(Player, GameStats)
                    if player_entities:
                        stats = player_entities[0].get_component(GameStats)
                        stats.damage_dealt += projectile.damage

                # Destroy projectile
                self.world.destroy_entity(projectile_entity)
                break

    def _aabb_collision(self, pos1: Position, size1: Size,
                       pos2: Position, size2: Size) -> bool:
        """Simple AABB collision detection"""
        left1 = pos1.x - size1.width / 2
        right1 = pos1.x + size1.width / 2
        top1 = pos1.y - size1.height / 2
        bottom1 = pos1.y + size1.height / 2

        left2 = pos2.x - size2.width / 2
        right2 = pos2.x + size2.width / 2
        top2 = pos2.y - size2.height / 2
        bottom2 = pos2.y + size2.height / 2

        return (left1 < right2 and right1 > left2 and
                top1 < bottom2 and bottom1 > top2)


class DamageOnContactSystem(System):
    """Handle melee damage (enemies touching player)"""

    def __init__(self, world):
        super().__init__(world)
        self.priority = 40
        self.damage_cooldown = {}  # Track cooldown per entity pair

    def update(self, dt: float):
        """Check for melee damage"""
        # Update cooldowns
        to_remove = []
        for key in self.damage_cooldown:
            self.damage_cooldown[key] -= dt
            if self.damage_cooldown[key] <= 0:
                to_remove.append(key)

        for key in to_remove:
            del self.damage_cooldown[key]

        # Check collisions
        entities = self.get_entities(Team, Position, Size, Health, Damage)

        for e1 in entities:
            for e2 in entities:
                if e1.id >= e2.id:  # Avoid duplicate checks
                    continue

                team1 = e1.get_component(Team)
                team2 = e2.get_component(Team)

                if team1.team == team2.team:
                    continue  # Same team

                # Check collision
                pos1 = e1.get_component(Position)
                size1 = e1.get_component(Size)
                pos2 = e2.get_component(Position)
                size2 = e2.get_component(Size)

                if self._circle_collision(pos1, size1, pos2, size2):
                    # Check cooldown
                    key = f"{e1.id}_{e2.id}"
                    if key in self.damage_cooldown:
                        continue

                    # Deal damage both ways
                    damage1 = e1.get_component(Damage)
                    damage2 = e2.get_component(Damage)
                    health1 = e1.get_component(Health)
                    health2 = e2.get_component(Health)

                    # Check invulnerability
                    if not e1.has_component(Invulnerable):
                        health1.damage(damage2.amount)
                        # Track damage taken if player
                        if e1.has_component(Player):
                            from src.systems.stats_system import GameStats
                            if e1.has_component(GameStats):
                                stats = e1.get_component(GameStats)
                                stats.damage_taken += damage2.amount

                    if not e2.has_component(Invulnerable):
                        health2.damage(damage1.amount)
                        # Track damage taken if player
                        if e2.has_component(Player):
                            from src.systems.stats_system import GameStats
                            if e2.has_component(GameStats):
                                stats = e2.get_component(GameStats)
                                stats.damage_taken += damage1.amount

                    # Set cooldown (0.5s between damage ticks)
                    self.damage_cooldown[key] = 0.5

    def _circle_collision(self, pos1: Position, size1: Size,
                         pos2: Position, size2: Size) -> bool:
        """Simple circle collision"""
        radius1 = size1.width / 2
        radius2 = size2.width / 2

        dx = pos1.x - pos2.x
        dy = pos1.y - pos2.y
        dist_sq = dx * dx + dy * dy
        radius_sum = radius1 + radius2

        return dist_sq < radius_sum * radius_sum


# === GAME DESIGNER NOTE ===
# Combat system implements:
# - Auto-targeting nearest enemy
# - Projectile-based ranged combat
# - Melee damage on contact
# - Cooldowns to prevent instant kills
# - Team-based combat (player vs enemy)
