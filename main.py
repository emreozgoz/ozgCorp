"""
DARK SANCTUM - Main Game Loop
Matrix Team: Full Team Collaboration

A dark gothic survival game inspired by Vampire Survivors
with tactical abilities and positioning
"""

import pygame
import sys
from src.core.ecs import World
from src.entities.factory import EntityFactory
from src.components.components import *
from src.systems.movement_system import MovementSystem, PlayerInputSystem
from src.systems.combat_system import AutoAttackSystem, ProjectileSystem, DamageOnContactSystem
from src.systems.spawn_system import WaveSpawnSystem, AISystem, DeathSystem
from src.systems.render_system import RenderSystem
from src.systems.ability_system import (
    AbilityInputSystem, HomingMissileSystem,
    StatusEffectSystem, LifetimeSystem
)
from src.systems.particle_system import ParticleSystem
from src.components.character_classes import *
from config.settings import *


class GameState:
    """Game state management"""
    MENU = "menu"
    CLASS_SELECT = "class_select"
    PLAYING = "playing"
    PAUSED = "paused"
    GAME_OVER = "game_over"


class DarkSanctum:
    """Main game class"""

    def __init__(self):
        # Initialize Pygame
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("DARK SANCTUM")
        self.clock = pygame.time.Clock()

        # Game state
        self.state = GameState.MENU
        self.running = True

        # ECS World
        self.world = World()
        self.factory = EntityFactory(self.world)

        # Fonts
        self.title_font = pygame.font.Font(None, 72)
        self.large_font = pygame.font.Font(None, 48)
        self.medium_font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)

        # Stats
        self.survival_time = 0.0
        self.enemies_killed = 0
        self.current_wave = 0

        # Character selection
        self.selected_class_index = 0
        self.selected_class = ALL_CLASSES[0]

    def init_game(self):
        """Initialize new game"""
        # Clear world
        self.world = World()
        self.factory = EntityFactory(self.world)

        # Create systems
        self._init_systems()

        # Spawn player at center with selected class
        self.factory.create_player(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2, self.selected_class)

        # Reset stats
        self.survival_time = 0.0
        self.enemies_killed = 0
        self.current_wave = 0

        print("\n" + "=" * 70)
        print("🌙 DARK SANCTUM - Game Started 🌙")
        print("=" * 70)
        print("Controls:")
        print("  WASD / Arrow Keys - Move")
        print("  Q, W, E, R - Abilities (coming soon)")
        print("  ESC - Pause")
        print("=" * 70 + "\n")

    def _init_systems(self):
        """Initialize all game systems"""
        # Input (priority 5-6)
        self.world.add_system(PlayerInputSystem(self.world))
        self.world.add_system(AbilityInputSystem(self.world))

        # Movement (priority 10)
        self.world.add_system(MovementSystem(self.world))

        # Status Effects (priority 15)
        self.world.add_system(StatusEffectSystem(self.world))

        # AI (priority 25)
        self.world.add_system(AISystem(self.world))

        # Combat (priority 30-40)
        self.world.add_system(AutoAttackSystem(self.world))
        self.world.add_system(ProjectileSystem(self.world))
        self.world.add_system(HomingMissileSystem(self.world))
        self.world.add_system(DamageOnContactSystem(self.world))

        # Spawning (priority 50)
        self.world.add_system(WaveSpawnSystem(self.world))

        # Death (priority 60)
        self.world.add_system(DeathSystem(self.world))

        # Lifetime (priority 65)
        self.world.add_system(LifetimeSystem(self.world))

        # Particles (priority 66)
        self.world.add_system(ParticleSystem(self.world))

        # Rendering (priority 100)
        self.world.add_system(RenderSystem(self.world, self.screen))

    def run(self):
        """Main game loop"""
        while self.running:
            dt = self.clock.tick(FPS) / 1000.0  # Delta time in seconds

            # Handle events
            self._handle_events()

            # Update based on state
            if self.state == GameState.MENU:
                self._render_menu()
            elif self.state == GameState.CLASS_SELECT:
                self._render_class_select()
            elif self.state == GameState.PLAYING:
                self._update_game(dt)
                self._check_game_over()
            elif self.state == GameState.PAUSED:
                self._render_pause()
            elif self.state == GameState.GAME_OVER:
                self._render_game_over()

            pygame.display.flip()

        pygame.quit()
        sys.exit()

    def _handle_events(self):
        """Handle input events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            elif event.type == pygame.KEYDOWN:
                # ESC key
                if event.key == pygame.K_ESCAPE:
                    if self.state == GameState.PLAYING:
                        self.state = GameState.PAUSED
                    elif self.state == GameState.PAUSED:
                        self.state = GameState.PLAYING

                # Menu controls
                if self.state == GameState.MENU:
                    if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                        self.state = GameState.CLASS_SELECT

                # Class selection controls
                elif self.state == GameState.CLASS_SELECT:
                    if event.key == pygame.K_LEFT:
                        self.selected_class_index = (self.selected_class_index - 1) % len(ALL_CLASSES)
                        self.selected_class = ALL_CLASSES[self.selected_class_index]
                    elif event.key == pygame.K_RIGHT:
                        self.selected_class_index = (self.selected_class_index + 1) % len(ALL_CLASSES)
                        self.selected_class = ALL_CLASSES[self.selected_class_index]
                    elif event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                        self.init_game()
                        self.state = GameState.PLAYING
                    elif event.key == pygame.K_ESCAPE:
                        self.state = GameState.MENU

                # Game over controls
                if self.state == GameState.GAME_OVER:
                    if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                        self.init_game()
                        self.state = GameState.PLAYING
                    elif event.key == pygame.K_ESCAPE:
                        self.state = GameState.MENU

    def _update_game(self, dt: float):
        """Update game logic"""
        # Update survival time
        self.survival_time += dt

        # Get current wave from spawn system
        from src.systems.spawn_system import WaveSpawnSystem
        for system in self.world.systems:
            if isinstance(system, WaveSpawnSystem):
                self.current_wave = system.current_wave
                break

        # Update ECS world
        self.world.update(dt)

    def _check_game_over(self):
        """Check if player is dead"""
        player_entities = self.world.get_entities_with_components(Player, Health)

        if not player_entities:
            self.state = GameState.GAME_OVER
            return

        player_health = player_entities[0].get_component(Health)
        if not player_health.is_alive:
            self.state = GameState.GAME_OVER

    def _render_menu(self):
        """Render main menu"""
        self.screen.fill(COLOR_BACKGROUND)

        # Title
        title = self.title_font.render("DARK SANCTUM", True, COLOR_BLOOD_RED)
        title_rect = title.get_rect(center=(WINDOW_WIDTH // 2, 150))
        self.screen.blit(title, title_rect)

        # Subtitle
        subtitle = self.medium_font.render("Survive. Evolve. Dominate.", True, COLOR_GOLD)
        subtitle_rect = subtitle.get_rect(center=(WINDOW_WIDTH // 2, 230))
        self.screen.blit(subtitle, subtitle_rect)

        # Instructions
        instructions = [
            "WASD / Arrow Keys - Move",
            "Auto-attack targets nearest enemy",
            "Survive waves of enemies",
            "Level up to gain power",
            "",
            "Press SPACE to Start"
        ]

        y_offset = 320
        for line in instructions:
            text = self.small_font.render(line, True, COLOR_WHITE)
            text_rect = text.get_rect(center=(WINDOW_WIDTH // 2, y_offset))
            self.screen.blit(text, text_rect)
            y_offset += 35

        # Credits
        credit = self.small_font.render("Created by Matrix AI Team", True, (100, 100, 120))
        credit_rect = credit.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT - 40))
        self.screen.blit(credit, credit_rect)

    def _render_class_select(self):
        """Render character class selection screen"""
        self.screen.fill(COLOR_BACKGROUND)

        # Title
        title = self.title_font.render("SELECT CHARACTER", True, COLOR_GOLD)
        title_rect = title.get_rect(center=(WINDOW_WIDTH // 2, 80))
        self.screen.blit(title, title_rect)

        # Display all classes
        class_width = 300
        class_spacing = 50
        total_width = len(ALL_CLASSES) * class_width + (len(ALL_CLASSES) - 1) * class_spacing
        start_x = (WINDOW_WIDTH - total_width) // 2

        for i, char_class in enumerate(ALL_CLASSES):
            x = start_x + i * (class_width + class_spacing)
            y = 200

            # Highlight selected class
            is_selected = (i == self.selected_class_index)

            # Class box
            box_color = char_class.color if is_selected else (50, 50, 60)
            border_color = COLOR_GOLD if is_selected else (80, 80, 90)
            border_width = 4 if is_selected else 2

            box_rect = pygame.Rect(x, y, class_width, 300)
            pygame.draw.rect(self.screen, box_color, box_rect)
            pygame.draw.rect(self.screen, border_color, box_rect, border_width)

            # Class name
            name_surf = self.large_font.render(char_class.name, True, COLOR_WHITE)
            name_rect = name_surf.get_rect(center=(x + class_width // 2, y + 40))
            self.screen.blit(name_surf, name_rect)

            # Stats
            stats = [
                f"HP: {int(char_class.health)}",
                f"DMG: {int(char_class.damage)}",
                f"SPD: {int(char_class.speed)}",
                "",
                f"{char_class.passive_name}",
            ]

            stat_y = y + 100
            for stat in stats:
                color = COLOR_GOLD if stat == char_class.passive_name else COLOR_WHITE
                stat_surf = self.small_font.render(stat, True, color)
                stat_rect = stat_surf.get_rect(center=(x + class_width // 2, stat_y))
                self.screen.blit(stat_surf, stat_rect)
                stat_y += 30

            # Description (small font)
            desc_lines = self._wrap_text(char_class.passive_description, 35)
            desc_y = stat_y + 10
            for line in desc_lines:
                desc_surf = self.small_font.render(line, True, (180, 180, 180))
                desc_rect = desc_surf.get_rect(center=(x + class_width // 2, desc_y))
                self.screen.blit(desc_surf, desc_rect)
                desc_y += 25

        # Instructions
        inst_text = "← → to Select | SPACE to Confirm | ESC to Back"
        inst_surf = self.medium_font.render(inst_text, True, COLOR_WHITE)
        inst_rect = inst_surf.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT - 60))
        self.screen.blit(inst_surf, inst_rect)

    def _wrap_text(self, text: str, max_chars: int):
        """Simple text wrapping"""
        words = text.split()
        lines = []
        current_line = []
        current_length = 0

        for word in words:
            if current_length + len(word) + 1 <= max_chars:
                current_line.append(word)
                current_length += len(word) + 1
            else:
                if current_line:
                    lines.append(" ".join(current_line))
                current_line = [word]
                current_length = len(word)

        if current_line:
            lines.append(" ".join(current_line))

        return lines

    def _render_pause(self):
        """Render pause overlay"""
        # Darken screen
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))

        # Paused text
        text = self.large_font.render("PAUSED", True, COLOR_WHITE)
        text_rect = text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 40))
        self.screen.blit(text, text_rect)

        # Instructions
        instructions = self.small_font.render("Press ESC to Resume", True, COLOR_WHITE)
        instructions_rect = instructions.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 20))
        self.screen.blit(instructions, instructions_rect)

    def _render_game_over(self):
        """Render game over screen"""
        self.screen.fill(COLOR_BACKGROUND)

        # Game Over text
        title = self.title_font.render("DEFEATED", True, COLOR_BLOOD_RED)
        title_rect = title.get_rect(center=(WINDOW_WIDTH // 2, 100))
        self.screen.blit(title, title_rect)

        # Character info
        char_text = f"Playing as: {self.selected_class.name}"
        char_surf = self.medium_font.render(char_text, True, self.selected_class.color)
        char_rect = char_surf.get_rect(center=(WINDOW_WIDTH // 2, 170))
        self.screen.blit(char_surf, char_rect)

        # Stats
        minutes = int(self.survival_time // 60)
        seconds = int(self.survival_time % 60)

        stats = [
            ("", COLOR_WHITE),  # Empty line
            (f"⏱️  Survived: {minutes}m {seconds}s", COLOR_WHITE),
            (f"🌊 Waves Cleared: {self.current_wave}", COLOR_ARCANE_BLUE),
            ("", COLOR_WHITE),  # Empty line
        ]

        # Get player level if available
        player_entities = self.world.get_entities_with_components(Player, Experience)
        if player_entities:
            xp = player_entities[0].get_component(Experience)
            stats.append((f"⬆️  Final Level: {xp.level}", COLOR_GOLD))

        stats.extend([
            ("", COLOR_WHITE),
            ("", COLOR_WHITE),
            ("Press SPACE to Restart", (150, 150, 150)),
            ("Press ESC for Menu", (150, 150, 150))
        ])

        y_offset = 250
        for line, color in stats:
            text = self.medium_font.render(line, True, color)
            text_rect = text.get_rect(center=(WINDOW_WIDTH // 2, y_offset))
            self.screen.blit(text, text_rect)
            y_offset += 45


def main():
    """Entry point"""
    print("\n" + "=" * 70)
    print("🌙 DARK SANCTUM 🌙")
    print("=" * 70)
    print("A tactical survival game by Matrix AI Team")
    print("Inspired by Vampire Survivors with unique mechanics")
    print("=" * 70 + "\n")

    game = DarkSanctum()
    game.run()


if __name__ == "__main__":
    main()


# === MATRIX TEAM NOTES ===
# Game Designer: Clean game loop with proper state management
# Technical Director: Delta time ensures frame-rate independence
# UI/UX Designer: Dark gothic aesthetic maintained throughout UI
# Developer: ECS systems properly ordered by priority
# QA Tester: Easy to add debug modes and testing hooks
