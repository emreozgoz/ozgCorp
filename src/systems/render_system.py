"""
DARK SANCTUM - Rendering System
Matrix Team: UI/UX Designer + Developer

Dark gothic aesthetic with minimal HUD
"""

import pygame
from src.core.ecs import System
from src.components.components import *
from config.settings import *


class RenderSystem(System):
    """Render all visible entities"""

    def __init__(self, world, screen: pygame.Surface):
        super().__init__(world)
        self.priority = 100  # Render last
        self.screen = screen
        self.font = None

    def update(self, dt: float):
        """Render frame"""
        # Clear screen with dark background
        self.screen.fill(COLOR_BACKGROUND)

        # Render all sprites
        self._render_sprites()

        # Render health bars
        self._render_health_bars()

        # Render HUD
        self._render_hud()

        if SHOW_FPS:
            self._render_fps(1.0 / dt if dt > 0 else 0)

    def _render_sprites(self):
        """Render all entities with sprites"""
        entities = self.get_entities(Position, Sprite, Size)

        for entity in entities:
            pos = entity.get_component(Position)
            sprite = entity.get_component(Sprite)
            size = entity.get_component(Size)

            if sprite.radius:
                # Draw as circle
                pygame.draw.circle(
                    self.screen,
                    sprite.color,
                    (int(pos.x), int(pos.y)),
                    int(sprite.radius)
                )
            else:
                # Draw as rectangle
                rect = pygame.Rect(
                    int(pos.x - size.width / 2),
                    int(pos.y - size.height / 2),
                    int(size.width),
                    int(size.height)
                )
                pygame.draw.rect(self.screen, sprite.color, rect)

    def _render_health_bars(self):
        """Render health bars above entities"""
        entities = self.get_entities(Position, Health, Size)

        for entity in entities:
            pos = entity.get_component(Position)
            health = entity.get_component(Health)
            size = entity.get_component(Size)

            # Skip if full health
            if health.percent >= 0.99:
                continue

            # Health bar position (above entity)
            bar_width = size.width
            bar_height = 4
            bar_x = int(pos.x - bar_width / 2)
            bar_y = int(pos.y - size.height / 2 - 10)

            # Background (dark red)
            bg_rect = pygame.Rect(bar_x, bar_y, bar_width, bar_height)
            pygame.draw.rect(self.screen, (40, 10, 10), bg_rect)

            # Foreground (blood red)
            fg_width = int(bar_width * health.percent)
            if fg_width > 0:
                fg_rect = pygame.Rect(bar_x, bar_y, fg_width, bar_height)
                pygame.draw.rect(self.screen, COLOR_BLOOD_RED, fg_rect)

            # Border
            pygame.draw.rect(self.screen, (80, 20, 20), bg_rect, 1)

    def _render_hud(self):
        """Render minimal HUD"""
        if not self.font:
            self.font = pygame.font.Font(None, 32)
            self.small_font = pygame.font.Font(None, 24)

        # Find player
        player_entities = self.get_entities(Player, Health, Experience)
        if not player_entities:
            return

        player = player_entities[0]
        health = player.get_component(Health)
        xp = player.get_component(Experience)

        # === HEALTH BAR (Bottom Left) ===
        health_text = f"HP: {int(health.current)}/{int(health.max_health)}"
        text_surf = self.small_font.render(health_text, True, COLOR_WHITE)
        self.screen.blit(text_surf, (20, WINDOW_HEIGHT - 80))

        # Health bar
        bar_width = 200
        bar_height = 20
        bar_x = 20
        bar_y = WINDOW_HEIGHT - 50

        # Background
        pygame.draw.rect(self.screen, (40, 10, 10),
                        (bar_x, bar_y, bar_width, bar_height))

        # Foreground
        fg_width = int(bar_width * health.percent)
        pygame.draw.rect(self.screen, COLOR_BLOOD_RED,
                        (bar_x, bar_y, fg_width, bar_height))

        # Border
        pygame.draw.rect(self.screen, (120, 40, 40),
                        (bar_x, bar_y, bar_width, bar_height), 2)

        # === XP BAR (Bottom of screen) ===
        xp_percent = xp.current_xp / xp.xp_to_next_level
        xp_bar_height = 10
        xp_bar_y = WINDOW_HEIGHT - 15

        # Background
        pygame.draw.rect(self.screen, (20, 20, 40),
                        (0, xp_bar_y, WINDOW_WIDTH, xp_bar_height))

        # Foreground
        xp_width = int(WINDOW_WIDTH * xp_percent)
        pygame.draw.rect(self.screen, COLOR_GOLD,
                        (0, xp_bar_y, xp_width, xp_bar_height))

        # === LEVEL (Top Left) ===
        level_text = f"LEVEL {xp.level}"
        level_surf = self.font.render(level_text, True, COLOR_GOLD)
        self.screen.blit(level_surf, (20, 20))

        # === ENEMY COUNT (Top Right) ===
        enemy_count = len(self.get_entities(Enemy))
        enemy_text = f"ENEMIES: {enemy_count}"
        enemy_surf = self.small_font.render(enemy_text, True, COLOR_WHITE)
        text_rect = enemy_surf.get_rect()
        text_rect.topright = (WINDOW_WIDTH - 20, 20)
        self.screen.blit(enemy_surf, text_rect)

    def _render_fps(self, fps: float):
        """Render FPS counter"""
        if not self.font:
            self.font = pygame.font.Font(None, 24)

        fps_text = f"FPS: {int(fps)}"
        fps_surf = self.font.render(fps_text, True, (100, 100, 100))
        text_rect = fps_surf.get_rect()
        text_rect.topright = (WINDOW_WIDTH - 20, WINDOW_HEIGHT - 30)
        self.screen.blit(fps_surf, text_rect)


# === UI/UX DESIGNER NOTE ===
# Dark gothic aesthetic achieved through:
# - Deep purple-black background
# - Blood red for health
# - Gold for XP/leveling
# - Minimal HUD keeps focus on gameplay
# - Health bars only show when damaged
# - Clean, readable fonts
