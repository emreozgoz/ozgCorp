"""
DARK SANCTUM - Simple Background System
Matrix Team: UI/UX Designer + Technical Director

Sprint 27: Visual clarity improvements - tiled background
"""

import pygame
from src.core.ecs import System
from config.settings import WINDOW_WIDTH, WINDOW_HEIGHT


class SimpleBackgroundSystem(System):
    """Simple tiled background for maximum gameplay clarity (Vampire Survivors style)"""

    def __init__(self, world, screen: pygame.Surface):
        super().__init__(world)
        self.priority = 1  # Render first (before everything)
        self.screen = screen

        # Create gothic stone tile texture
        self.tile_size = 64
        self.tile = self._create_gothic_tile()

        # Pre-render tiled background surface for performance
        self.background_surface = self._create_tiled_background()

    def _create_gothic_tile(self) -> pygame.Surface:
        """Create a gothic stone tile texture"""
        tile = pygame.Surface((self.tile_size, self.tile_size))

        # Base dark stone color
        base_color = (20, 15, 25)  # Dark purple-gray
        tile.fill(base_color)

        # Add subtle texture variation
        import random
        random.seed(42)  # Consistent pattern

        for y in range(self.tile_size):
            for x in range(self.tile_size):
                # Add random slight color variation for texture
                if random.random() < 0.1:
                    variation = random.randint(-5, 5)
                    color = (
                        max(0, min(255, base_color[0] + variation)),
                        max(0, min(255, base_color[1] + variation)),
                        max(0, min(255, base_color[2] + variation))
                    )
                    tile.set_at((x, y), color)

        # Draw tile borders (subtle)
        border_color = (30, 25, 35)  # Slightly lighter
        pygame.draw.rect(tile, border_color, (0, 0, self.tile_size, self.tile_size), 1)

        # Add subtle cracks/details
        crack_color = (15, 10, 20)  # Darker
        # Horizontal crack
        pygame.draw.line(tile, crack_color, (10, self.tile_size // 2), (self.tile_size - 10, self.tile_size // 2), 1)
        # Vertical crack
        pygame.draw.line(tile, crack_color, (self.tile_size // 2, 10), (self.tile_size // 2, self.tile_size - 10), 1)

        return tile

    def _create_tiled_background(self) -> pygame.Surface:
        """Create full tiled background surface"""
        bg = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))

        # Tile across entire screen
        for y in range(0, WINDOW_HEIGHT, self.tile_size):
            for x in range(0, WINDOW_WIDTH, self.tile_size):
                bg.blit(self.tile, (x, y))

        return bg

    def update(self, dt: float):
        """Render static tiled background"""
        # Blit pre-rendered background (very fast)
        self.screen.blit(self.background_surface, (0, 0))


# === UI/UX DESIGNER NOTE ===
# Sprint 27: Background Simplification
# - Removed all animated particles (ash, embers, mist)
# - Removed parallax layers
# - Simple solid color background
# - Vampire Survivors approach: gameplay clarity > visual flair
# - Result: Players can easily see projectiles and enemies
