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
from config.settings import *


class GameState:
    """Game state management"""
    MENU = "menu"
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

    def init_game(self):
        """Initialize new game"""
        # Clear world
        self.world = World()
        self.factory = EntityFactory(self.world)

        # Create systems
        self._init_systems()

        # Spawn player at center
        self.factory.create_player(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)

        # Reset stats
        self.survival_time = 0.0
        self.enemies_killed = 0

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
                        self.init_game()
                        self.state = GameState.PLAYING

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
        title_rect = title.get_rect(center=(WINDOW_WIDTH // 2, 150))
        self.screen.blit(title, title_rect)

        # Stats
        minutes = int(self.survival_time // 60)
        seconds = int(self.survival_time % 60)
        time_text = f"Survived: {minutes}m {seconds}s"

        stats = [
            time_text,
            "",
            "Press SPACE to Restart",
            "Press ESC for Menu"
        ]

        y_offset = 280
        for line in stats:
            text = self.medium_font.render(line, True, COLOR_WHITE)
            text_rect = text.get_rect(center=(WINDOW_WIDTH // 2, y_offset))
            self.screen.blit(text, text_rect)
            y_offset += 50


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
