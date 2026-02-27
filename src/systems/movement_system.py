"""
DARK SANCTUM - Movement System
Matrix Team: Developer + Technical Director

Handles all entity movement with velocity and collision
"""

import pygame
from src.core.ecs import System
from src.components.components import Position, Velocity, Size
from config.settings import WINDOW_WIDTH, WINDOW_HEIGHT


class MovementSystem(System):
    """Moves entities based on their velocity"""

    def __init__(self, world):
        super().__init__(world)
        self.priority = 10  # Run early

    def update(self, dt: float):
        """Update all entities with Position and Velocity"""
        entities = self.get_entities(Position, Velocity)

        for entity in entities:
            pos = entity.get_component(Position)
            vel = entity.get_component(Velocity)
            size = entity.get_component(Size)

            # Update position
            pos.x += vel.vx * dt
            pos.y += vel.vy * dt

            # Screen bounds clamping
            if size:
                half_width = size.width / 2
                half_height = size.height / 2

                pos.x = max(half_width, min(WINDOW_WIDTH - half_width, pos.x))
                pos.y = max(half_height, min(WINDOW_HEIGHT - half_height, pos.y))


class PlayerInputSystem(System):
    """Handle player WASD input"""

    def __init__(self, world):
        super().__init__(world)
        self.priority = 5  # Run before movement

    def update(self, dt: float):
        """Update player velocity based on input"""
        from src.components.components import Player

        entities = self.get_entities(Player, Velocity, Position)

        for entity in entities:
            player = entity.get_component(Player)
            vel = entity.get_component(Velocity)

            # Get keyboard state
            keys = pygame.key.get_pressed()

            # Calculate movement direction
            dx = 0
            dy = 0

            if keys[pygame.K_w] or keys[pygame.K_UP]:
                dy -= 1
            if keys[pygame.K_s] or keys[pygame.K_DOWN]:
                dy += 1
            if keys[pygame.K_a] or keys[pygame.K_LEFT]:
                dx -= 1
            if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
                dx += 1

            # Normalize diagonal movement
            import math
            if dx != 0 and dy != 0:
                length = math.sqrt(dx * dx + dy * dy)
                dx /= length
                dy /= length

            # Apply velocity
            vel.vx = dx * player.move_speed
            vel.vy = dy * player.move_speed


# === TECHNICAL DIRECTOR NOTE ===
# Movement system is simple but efficient:
# - Decoupled from rendering
# - Easy to add more movement types (knockback, dash, etc)
# - Screen bounds handled cleanly
# - Diagonal movement normalized (no speed exploit)
