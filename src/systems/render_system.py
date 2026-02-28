"""
DARK SANCTUM - Rendering System
Matrix Team: UI/UX Designer + Developer

Dark gothic aesthetic with minimal HUD
"""

import pygame
from src.core.ecs import System
from src.components.components import *
from config.settings import *
from src.core.asset_manager import asset_manager


class RenderSystem(System):
    """Render all visible entities"""

    def __init__(self, world, screen: pygame.Surface):
        super().__init__(world)
        self.priority = 100  # Render last
        self.screen = screen
        self.font = None
        # Initialize fonts
        self.small_font = pygame.font.Font(None, 20)
        self.medium_font = pygame.font.Font(None, 32)
        self.large_font = pygame.font.Font(None, 48)

    def update(self, dt: float):
        """Render frame"""
        # Get screen shake offset
        camera_offset = self._get_camera_offset()

        # Background is now handled by BackgroundSystem (priority 1) - Sprint 25
        # No need to fill screen here

        # Render all sprites (with camera offset)
        self._render_sprites(camera_offset)

        # Render health bars
        self._render_health_bars(camera_offset)

        # Render boss health bar (top of screen)
        self._render_boss_health()

        # Render damage numbers
        self._render_damage_numbers(camera_offset)

        # Render HUD (not affected by camera shake)
        self._render_hud()

        if SHOW_FPS:
            self._render_fps(1.0 / dt if dt > 0 else 0)

    def _get_camera_offset(self) -> tuple[float, float]:
        """Get camera offset from screen shake system"""
        from src.systems.screen_effects import ScreenEffectsSystem
        for system in self.world.systems:
            if isinstance(system, ScreenEffectsSystem):
                return system.get_camera_offset()
        return (0, 0)

    def _render_sprites(self, camera_offset: tuple[float, float] = (0, 0)):
        """Render all entities with sprites (Sprint 26: Real sprite images!)"""
        entities = self.get_entities(Position, Sprite, Size)

        for entity in entities:
            pos = entity.get_component(Position)
            sprite = entity.get_component(Sprite)
            size = entity.get_component(Size)

            # Apply camera offset for screen shake
            render_x = int(pos.x + camera_offset[0])
            render_y = int(pos.y + camera_offset[1])

            # Check for hit flash
            from src.systems.screen_effects import HitFlash
            hit_flash = entity.get_component(HitFlash) if entity.has_component(HitFlash) else None

            # Check if boss (render glow)
            enemy = entity.get_component(Enemy)
            is_boss = enemy and enemy.is_boss

            # Try to get sprite image from asset manager
            sprite_image = None
            if hasattr(sprite, 'sprite_key') and sprite.sprite_key:
                sprite_image = asset_manager.get_sprite(sprite.sprite_key)

            if sprite_image:
                # RENDER SPRITE IMAGE (Sprint 26: No more circles!)
                sprite_rect = sprite_image.get_rect(center=(render_x, render_y))

                # Apply hit flash effect
                if hit_flash and hit_flash.active:
                    # Create white flash surface
                    flash_surf = sprite_image.copy()
                    flash_surf.fill((255, 255, 255, 180), special_flags=pygame.BLEND_RGB_ADD)
                    self.screen.blit(flash_surf, sprite_rect)
                else:
                    # Boss glow effect
                    if is_boss:
                        # Render glow behind sprite
                        glow_size = (int(sprite_rect.width * 1.3), int(sprite_rect.height * 1.3))
                        glow_surf = pygame.Surface(glow_size, pygame.SRCALPHA)
                        pygame.draw.circle(
                            glow_surf,
                            BOSS_GLOW_COLOR + (120,),
                            (glow_size[0] // 2, glow_size[1] // 2),
                            glow_size[0] // 2
                        )
                        glow_rect = glow_surf.get_rect(center=(render_x, render_y))
                        self.screen.blit(glow_surf, glow_rect)

                    # Render sprite
                    self.screen.blit(sprite_image, sprite_rect)

            else:
                # FALLBACK: Old circle rendering (if sprite not found)
                flash_color = (255, 255, 255) if (hit_flash and hit_flash.active) else sprite.color

                if sprite.radius:
                    # Boss glow effect
                    if is_boss:
                        pygame.draw.circle(
                            self.screen,
                            BOSS_GLOW_COLOR,
                            (render_x, render_y),
                            int(sprite.radius + 5),
                            3
                        )

                    # Draw as circle (with hit flash)
                    pygame.draw.circle(
                        self.screen,
                        flash_color,
                        (render_x, render_y),
                        int(sprite.radius)
                    )
                else:
                    # Draw as rectangle
                    rect = pygame.Rect(
                        int(render_x - size.width / 2),
                        int(render_y - size.height / 2),
                        int(size.width),
                        int(size.height)
                    )
                    pygame.draw.rect(self.screen, sprite.color, rect)

    def _render_health_bars(self, camera_offset: tuple[float, float] = (0, 0)):
        """Render health bars above entities"""
        entities = self.get_entities(Position, Health, Size)

        for entity in entities:
            pos = entity.get_component(Position)
            health = entity.get_component(Health)
            size = entity.get_component(Size)

            # Skip if full health
            if health.percent >= 0.99:
                continue

            # Apply camera offset
            render_x = pos.x + camera_offset[0]
            render_y = pos.y + camera_offset[1]

            # Health bar position (above entity, with camera offset)
            bar_width = size.width
            bar_height = 4
            bar_x = int(render_x - bar_width / 2)
            bar_y = int(render_y - size.height / 2 - 10)

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

    def _render_boss_health(self):
        """Render boss health bar at top of screen"""
        # Find boss
        boss_entities = self.get_entities(Enemy, Health)
        boss = None
        for entity in boss_entities:
            enemy = entity.get_component(Enemy)
            if enemy.is_boss:
                boss = entity
                break

        if not boss:
            return

        # Get boss health
        health = boss.get_component(Health)

        # Boss health bar (top center)
        bar_width = 400
        bar_height = 30
        bar_x = (WINDOW_WIDTH - bar_width) // 2
        bar_y = 20

        # Background
        pygame.draw.rect(self.screen, (40, 10, 10),
                        (bar_x, bar_y, bar_width, bar_height))

        # Foreground
        fg_width = int(bar_width * health.percent)
        if fg_width > 0:
            pygame.draw.rect(self.screen, BOSS_GLOW_COLOR,
                            (bar_x, bar_y, fg_width, bar_height))

        # Border (thick)
        pygame.draw.rect(self.screen, COLOR_BLOOD_RED,
                        (bar_x, bar_y, bar_width, bar_height), 3)

        # Boss name
        if not self.font:
            self.font = pygame.font.Font(None, 32)

        boss_text = "💀 BLOOD TITAN 💀"
        boss_surf = self.font.render(boss_text, True, BOSS_GLOW_COLOR)
        boss_rect = boss_surf.get_rect(center=(WINDOW_WIDTH // 2, bar_y - 15))
        self.screen.blit(boss_surf, boss_rect)

        # Health text
        health_text = f"{int(health.current)}/{int(health.max_health)}"
        if not self.small_font:
            self.small_font = pygame.font.Font(None, 24)
        health_surf = self.small_font.render(health_text, True, COLOR_WHITE)
        health_rect = health_surf.get_rect(center=(WINDOW_WIDTH // 2, bar_y + bar_height // 2))
        self.screen.blit(health_surf, health_rect)

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

        # === WAVE & TIME (Top Center) ===
        # Get wave count from game
        # Note: This will be passed from main game loop

        # === ENEMY COUNT (Top Right) ===
        enemy_count = len(self.get_entities(Enemy))
        enemy_text = f"ENEMIES: {enemy_count}"
        enemy_surf = self.small_font.render(enemy_text, True, COLOR_WHITE)
        text_rect = enemy_surf.get_rect()
        text_rect.topright = (WINDOW_WIDTH - 20, 20)
        self.screen.blit(enemy_surf, text_rect)

        # === ABILITY COOLDOWNS (Bottom Center) ===
        abilities = player.get_component(Abilities)
        self._render_abilities(abilities)

    def _render_abilities(self, abilities: Abilities):
        """Render ability cooldowns"""
        ability_keys = ['Q', 'W', 'E', 'R']
        ability_names = ['Dash', 'Nova', 'Missiles', 'Freeze']
        ability_colors = [
            (150, 100, 255),  # Q - Purple (mobility)
            (180, 20, 20),    # W - Red (damage)
            (80, 120, 255),   # E - Blue (burst)
            (255, 215, 0)     # R - Gold (ultimate)
        ]

        # Position at bottom center
        slot_size = 50
        slot_spacing = 10
        total_width = len(ability_keys) * (slot_size + slot_spacing)
        start_x = (WINDOW_WIDTH - total_width) // 2
        y = WINDOW_HEIGHT - 80

        for i, key in enumerate(ability_keys):
            x = start_x + i * (slot_size + slot_spacing)

            # Background slot
            slot_rect = pygame.Rect(x, y, slot_size, slot_size)
            pygame.draw.rect(self.screen, (30, 20, 40), slot_rect)
            pygame.draw.rect(self.screen, ability_colors[i], slot_rect, 2)

            # Cooldown overlay
            cooldown = abilities.cooldowns[key]
            if cooldown > 0:
                # Calculate cooldown percentage
                max_cooldown = {
                    'Q': ABILITY_Q_COOLDOWN,
                    'W': ABILITY_W_COOLDOWN,
                    'E': ABILITY_E_COOLDOWN,
                    'R': ABILITY_R_COOLDOWN
                }[key]

                cd_percent = cooldown / max_cooldown
                overlay_height = int(slot_size * cd_percent)

                # Dark overlay
                if overlay_height > 0:
                    overlay_rect = pygame.Rect(x, y + (slot_size - overlay_height),
                                               slot_size, overlay_height)
                    overlay_surf = pygame.Surface((slot_size, overlay_height))
                    overlay_surf.set_alpha(180)
                    overlay_surf.fill((10, 5, 15))
                    self.screen.blit(overlay_surf, overlay_rect)

                # Cooldown text
                cd_text = f"{cooldown:.1f}"
                cd_surf = self.small_font.render(cd_text, True, COLOR_WHITE)
                cd_rect = cd_surf.get_rect(center=(x + slot_size // 2, y + slot_size // 2))
                self.screen.blit(cd_surf, cd_rect)
            else:
                # Ready - show key
                key_surf = self.font.render(key, True, ability_colors[i])
                key_rect = key_surf.get_rect(center=(x + slot_size // 2, y + slot_size // 2))
                self.screen.blit(key_surf, key_rect)

            # Ability name below
            name_surf = self.small_font.render(ability_names[i], True, (150, 150, 150))
            name_rect = name_surf.get_rect(center=(x + slot_size // 2, y + slot_size + 15))
            self.screen.blit(name_surf, name_rect)

    def _render_damage_numbers(self, camera_offset: tuple[float, float] = (0, 0)):
        """Render floating damage numbers"""
        from src.systems.screen_effects import DamageNumber
        damage_entities = self.get_entities(DamageNumber, Position)

        if not self.font:
            self.font = pygame.font.Font(None, 24)

        for entity in damage_entities:
            damage_num = entity.get_component(DamageNumber)
            pos = entity.get_component(Position)

            # Apply camera offset
            render_x = int(pos.x + camera_offset[0])
            render_y = int(pos.y + camera_offset[1])

            # Fade out over time
            alpha = int(255 * (1.0 - damage_num.elapsed / damage_num.lifetime))
            alpha = max(0, min(255, alpha))

            # Color based on damage type
            if damage_num.is_critical:
                color = (255, 215, 0)  # Gold for critical
                font_size = 32
            else:
                color = (255, 100, 100)  # Red for normal
                font_size = 24

            # Create font and render text
            damage_font = pygame.font.Font(None, font_size)
            damage_text = str(int(damage_num.damage))
            damage_surf = damage_font.render(damage_text, True, color)

            # Apply alpha
            damage_surf.set_alpha(alpha)

            # Center text on position
            text_rect = damage_surf.get_rect(center=(render_x, render_y))
            self.screen.blit(damage_surf, text_rect)

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
