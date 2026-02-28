"""
DARK SANCTUM - Simple Background System
Matrix Team: UI/UX Designer + Technical Director

Sprint 27: Visual clarity improvements - static background
"""

import pygame
from src.core.ecs import System
from config.settings import WINDOW_WIDTH, WINDOW_HEIGHT


class SimpleBackgroundSystem(System):
    """Simple static background for maximum gameplay clarity"""

    def __init__(self, world, screen: pygame.Surface):
        super().__init__(world)
        self.priority = 1  # Render first (before everything)
        self.screen = screen

        # Very dark purple-black color for gothic aesthetic
        # This is similar to Vampire Survivors' simple background
        self.bg_color = (15, 10, 20)  # Dark purple-black

    def update(self, dt: float):
        """Render static background - just fill with dark color"""
        # Simple, fast, and clear - exactly what we need
        self.screen.fill(self.bg_color)


# === UI/UX DESIGNER NOTE ===
# Sprint 27: Background Simplification
# - Removed all animated particles (ash, embers, mist)
# - Removed parallax layers
# - Simple solid color background
# - Vampire Survivors approach: gameplay clarity > visual flair
# - Result: Players can easily see projectiles and enemies
