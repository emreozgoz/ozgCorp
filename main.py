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
from src.systems.audio_system import AudioSystem
from src.systems.powerup_system import PowerUpCollectionSystem
from src.systems.weapon_system import WeaponFireSystem, LevelUpChoiceSystem
from src.systems.stats_system import (
    GameStats, PersistentStats, StatsTrackingSystem,
    AchievementSystem, calculate_score
)
from src.systems.screen_effects import (
    ScreenEffectsSystem, HitFlashSystem, DamageNumberSystem
)
from src.systems.map_system import MapManager, EnvironmentalHazardSystem
from src.systems.boss_abilities import BossAbilitySystem
from src.systems.simple_background import SimpleBackgroundSystem  # Sprint 27: Simplified background
from src.components.character_classes import *
from src.components.weapons import *
from config.settings import *
from config.difficulty import Difficulty, DifficultySettings
from config.maps import *
from config.ui_theme import *


class GameState:
    """Game state management"""
    MENU = "menu"
    CLASS_SELECT = "class_select"
    MAP_SELECT = "map_select"
    PLAYING = "playing"
    PAUSED = "paused"
    LEVEL_UP = "level_up"  # Weapon selection
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

        # Gothic UI Fonts (Sprint 24)
        self.title_font = pygame.font.Font(None, FONT_TITLE)
        self.large_font = pygame.font.Font(None, FONT_LARGE)
        self.medium_font = pygame.font.Font(None, FONT_MEDIUM)
        self.small_font = pygame.font.Font(None, FONT_SMALL)

        # Persistent stats
        self.persistent_stats = PersistentStats()

        # Stats (deprecated - now using GameStats component)
        self.survival_time = 0.0
        self.enemies_killed = 0
        self.current_wave = 0

        # Character selection
        self.selected_class_index = 0
        self.selected_class = ALL_CLASSES[0]

        # Difficulty selection
        self.selected_difficulty_index = 1  # Start on NORMAL
        self.difficulties = [Difficulty.EASY, Difficulty.NORMAL, Difficulty.HARD]

        # Map selection
        self.selected_map_index = 0
        self.selected_map_id = "dark_sanctum"  # Default: no hazards (change to "blood_cathedral" or "cursed_crypts" for hazards)

        # Level-up choices
        self.level_up_choices = []
        self.selected_choice_index = 0

        # Game over stats
        self.final_score = 0
        self.is_new_high_score = False

    def init_game(self):
        """Initialize new game"""
        # Clear world
        self.world = World()
        self.factory = EntityFactory(self.world)

        # Create systems
        self._init_systems()

        # Spawn player at center with selected class
        player = self.factory.create_player(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2, self.selected_class)

        # Add stats component to player
        player.add_component(GameStats())

        # Reset stats
        self.survival_time = 0.0
        self.enemies_killed = 0
        self.current_wave = 0
        self.final_score = 0
        self.is_new_high_score = False

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
        # Background (priority 1) - Sprint 27: Simple static background for clarity
        self.world.add_system(SimpleBackgroundSystem(self.world, self.screen))

        # Map System (priority 5)
        self.map_manager = MapManager(self.world)
        self.world.add_system(self.map_manager)
        self.map_manager.set_map(self.selected_map_id)

        # Screen Effects (priority 5)
        self.world.add_system(ScreenEffectsSystem(self.world))

        # Input (priority 5-6)
        self.world.add_system(PlayerInputSystem(self.world))
        self.world.add_system(AbilityInputSystem(self.world))

        # Movement (priority 10)
        self.world.add_system(MovementSystem(self.world))

        # Status Effects (priority 15)
        self.world.add_system(StatusEffectSystem(self.world))

        # AI (priority 25)
        self.world.add_system(AISystem(self.world))

        # Boss Abilities (priority 28)
        self.world.add_system(BossAbilitySystem(self.world))

        # Environmental Hazards (priority 30)
        self.world.add_system(EnvironmentalHazardSystem(self.world))

        # Combat (priority 30-40)
        self.world.add_system(AutoAttackSystem(self.world))
        self.world.add_system(WeaponFireSystem(self.world))  # Weapon system
        self.world.add_system(ProjectileSystem(self.world))
        self.world.add_system(HomingMissileSystem(self.world))
        self.world.add_system(DamageOnContactSystem(self.world))

        # Screen Effects (priority 41-42)
        self.world.add_system(HitFlashSystem(self.world))
        self.world.add_system(DamageNumberSystem(self.world))

        # Spawning (priority 50)
        self.world.add_system(WaveSpawnSystem(self.world))

        # Power-ups (priority 55)
        self.world.add_system(PowerUpCollectionSystem(self.world))

        # Death (priority 60)
        self.world.add_system(DeathSystem(self.world))

        # Lifetime (priority 65)
        self.world.add_system(LifetimeSystem(self.world))

        # Stats Tracking (priority 65-66)
        stats_system = StatsTrackingSystem(self.world)
        self.world.add_system(stats_system)
        self.world.add_system(AchievementSystem(self.world, self.persistent_stats))

        # Particles (priority 66)
        self.world.add_system(ParticleSystem(self.world))

        # Audio (priority 70)
        self.world.add_system(AudioSystem(self.world))

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
                self._check_level_up()
            elif self.state == GameState.PAUSED:
                self._render_pause()
            elif self.state == GameState.LEVEL_UP:
                self._render_level_up()
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

                # Pause menu controls
                if self.state == GameState.PAUSED:
                    if event.key == pygame.K_q:
                        self.state = GameState.MENU

                # Menu controls
                if self.state == GameState.MENU:
                    if event.key == pygame.K_LEFT:
                        self.selected_difficulty_index = (self.selected_difficulty_index - 1) % len(self.difficulties)
                    elif event.key == pygame.K_RIGHT:
                        self.selected_difficulty_index = (self.selected_difficulty_index + 1) % len(self.difficulties)
                    elif event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                        # Set difficulty
                        DifficultySettings.set_difficulty(self.difficulties[self.selected_difficulty_index])
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

                # Level-up controls
                elif self.state == GameState.LEVEL_UP:
                    if event.key == pygame.K_LEFT:
                        self.selected_choice_index = (self.selected_choice_index - 1) % len(self.level_up_choices)
                    elif event.key == pygame.K_RIGHT:
                        self.selected_choice_index = (self.selected_choice_index + 1) % len(self.level_up_choices)
                    elif event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                        self._apply_weapon_choice()

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
            # Calculate final stats and score
            player = player_entities[0]
            if player.has_component(GameStats):
                game_stats = player.get_component(GameStats)
                player_xp = player.get_component(Experience)
                player_level = player_xp.level if player_xp else 1

                # Calculate score
                self.final_score = calculate_score(game_stats, player_level)

                # Check if high score
                self.is_new_high_score = self.persistent_stats.is_high_score(self.final_score)

                # Save persistent stats
                self.persistent_stats.update_session_end(game_stats, player_level)

                # Add to high scores if qualifies
                if self.is_new_high_score:
                    self.persistent_stats.add_high_score(
                        self.selected_class.name,
                        self.final_score,
                        game_stats.highest_wave,
                        player_level
                    )

                print("\n" + "=" * 70)
                print("💀 GAME OVER 💀")
                print("=" * 70)
                print(f"Final Score: {self.final_score}")
                print(f"Kills: {game_stats.kills}")
                print(f"Highest Wave: {game_stats.highest_wave}")
                print(f"Survival Time: {game_stats.get_survival_time_str()}")
                if self.is_new_high_score:
                    print("🏆 NEW HIGH SCORE! 🏆")
                print("=" * 70 + "\n")

            self.state = GameState.GAME_OVER

    def _render_menu(self):
        """Render main menu with Gothic UI theme (Sprint 24)"""
        self.screen.fill(GOTHIC_BLACK)

        # Draw ornate border around screen
        draw_ornate_border(self.screen, GOTHIC_GOLD, BORDER_ORNATE)

        # Title with Gothic header
        GothicHeader.draw(self.screen, "DARK SANCTUM", 120, self.title_font, GLOW_CRIMSON, decoration=True)

        # Subtitle
        subtitle = self.medium_font.render("Survive. Evolve. Dominate.", True, GOTHIC_BONE)
        subtitle_rect = subtitle.get_rect(center=(WINDOW_WIDTH // 2, 200))
        self.screen.blit(subtitle, subtitle_rect)

        # Difficulty selection title
        diff_title = self.medium_font.render("SELECT DIFFICULTY", True, GOTHIC_GOLD)
        diff_title_rect = diff_title.get_rect(center=(WINDOW_WIDTH // 2, 280))
        self.screen.blit(diff_title, diff_title_rect)

        # Difficulty buttons using Gothic UI
        diff_names = ["EASY", "NORMAL", "HARD"]
        box_width = 180
        box_spacing = 40
        total_width = len(diff_names) * box_width + (len(diff_names) - 1) * box_spacing
        start_x = (WINDOW_WIDTH - total_width) // 2
        y = 340

        for i, name in enumerate(diff_names):
            x = start_x + i * (box_width + box_spacing)
            is_selected = (i == self.selected_difficulty_index)

            button_rect = pygame.Rect(x, y, box_width, 70)
            GothicButton.draw(
                self.screen, button_rect, name,
                self.medium_font,
                is_selected=is_selected
            )

        # Instructions panel
        inst_panel_rect = pygame.Rect(WINDOW_WIDTH // 2 - 250, 460, 500, 100)
        GothicPanel.draw(self.screen, inst_panel_rect, GOTHIC_SHADOW, GOTHIC_PURPLE, BORDER_THIN)

        instructions = [
            "LEFT/RIGHT to select difficulty",
            "Press SPACE to Continue"
        ]

        y_offset = 485
        for line in instructions:
            text = self.small_font.render(line, True, GOTHIC_SILVER)
            text_rect = text.get_rect(center=(WINDOW_WIDTH // 2, y_offset))
            self.screen.blit(text, text_rect)
            y_offset += 30

        # Credits
        credit = self.small_font.render("Created by Matrix AI Team", True, GOTHIC_MIST)
        credit_rect = credit.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT - 30))
        self.screen.blit(credit, credit_rect)

    def _render_class_select(self):
        """Render character class selection screen with Gothic UI (Sprint 24)"""
        self.screen.fill(GOTHIC_BLACK)

        # Draw ornate border
        draw_ornate_border(self.screen, GOTHIC_GOLD, BORDER_ORNATE)

        # Title with Gothic header
        GothicHeader.draw(self.screen, "SELECT CHARACTER", 60, self.title_font, GOTHIC_GOLD, decoration=True)

        # Display all classes
        class_width = 300
        class_spacing = 50
        total_width = len(ALL_CLASSES) * class_width + (len(ALL_CLASSES) - 1) * class_spacing
        start_x = (WINDOW_WIDTH - total_width) // 2

        for i, char_class in enumerate(ALL_CLASSES):
            x = start_x + i * (class_width + class_spacing)
            y = 140

            # Highlight selected class
            is_selected = (i == self.selected_class_index)

            # Gothic class panel
            box_color = char_class.color if is_selected else GOTHIC_SHADOW
            border_color = GOTHIC_GOLD if is_selected else GOTHIC_PURPLE
            border_width = BORDER_THICK if is_selected else BORDER_MEDIUM

            box_rect = pygame.Rect(x, y, class_width, 380)
            GothicPanel.draw(self.screen, box_rect, box_color, border_color, border_width)

            # Class name
            name_color = GOTHIC_BONE if is_selected else GOTHIC_SILVER
            name_surf = self.large_font.render(char_class.name, True, name_color)
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
                color = GOTHIC_GOLD if stat == char_class.passive_name else GOTHIC_BONE
                stat_surf = self.small_font.render(stat, True, color)
                stat_rect = stat_surf.get_rect(center=(x + class_width // 2, stat_y))
                self.screen.blit(stat_surf, stat_rect)
                stat_y += 30

            # Description (small font)
            desc_lines = self._wrap_text(char_class.passive_description, 35)
            desc_y = stat_y + 10
            for line in desc_lines:
                desc_surf = self.small_font.render(line, True, GOTHIC_MIST)
                desc_rect = desc_surf.get_rect(center=(x + class_width // 2, desc_y))
                self.screen.blit(desc_surf, desc_rect)
                desc_y += 25

        # Instructions panel
        inst_panel_rect = pygame.Rect(WINDOW_WIDTH // 2 - 350, WINDOW_HEIGHT - 90, 700, 60)
        GothicPanel.draw(self.screen, inst_panel_rect, GOTHIC_SHADOW, GOTHIC_PURPLE, BORDER_THIN)

        inst_text = "LEFT/RIGHT to Select | SPACE to Confirm | ESC to Back"
        inst_surf = self.medium_font.render(inst_text, True, GOTHIC_SILVER)
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
        """Render enhanced pause overlay with stats (Gothic UI - Sprint 24)"""
        # Darken screen
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
        overlay.fill(OVERLAY_DARK)
        self.screen.blit(overlay, (0, 0))

        # Gothic title
        GothicHeader.draw(self.screen, "PAUSED", 80, self.title_font, GOTHIC_GOLD, decoration=True)

        # Get player stats if available
        player_entities = self.world.get_entities_with_components(Player, Experience, Health)
        if player_entities:
            player = player_entities[0]
            xp = player.get_component(Experience)
            health = player.get_component(Health)

            # Get stats component if exists
            from src.systems.stats_system import GameStats
            if player.has_component(GameStats):
                game_stats = player.get_component(GameStats)

                # Gothic stats panel
                panel_width = 700
                panel_height = 400
                panel_x = (WINDOW_WIDTH - panel_width) // 2
                panel_y = 150

                # Gothic panel background
                panel_rect = pygame.Rect(panel_x, panel_y, panel_width, panel_height)
                GothicPanel.draw(self.screen, panel_rect, GOTHIC_SHADOW, GLOW_ARCANE, BORDER_ORNATE)

                # Character info
                char_name = player.get_component(Player).character_class_name
                char_text = self.large_font.render(f"⚔️  {char_name}", True, GOTHIC_GOLD)
                char_rect = char_text.get_rect(center=(WINDOW_WIDTH // 2, panel_y + 50))
                self.screen.blit(char_text, char_rect)

                # Player stats (2 columns)
                left_x = panel_x + 80
                right_x = panel_x + panel_width // 2 + 80
                stats_y = panel_y + 90

                left_stats = [
                    f"Level: {xp.level}",
                    f"HP: {int(health.current)}/{int(health.max_health)}",
                    f"Wave: {game_stats.highest_wave}",
                    f"Kills: {game_stats.kills}",
                    f"Bosses: {game_stats.bosses_killed}"
                ]

                for stat in left_stats:
                    stat_surf = self.medium_font.render(stat, True, GOTHIC_BONE)
                    stat_rect = stat_surf.get_rect(midleft=(left_x, stats_y))
                    self.screen.blit(stat_surf, stat_rect)
                    stats_y += 40

                stats_y = panel_y + 100
                right_stats = [
                    f"Time: {game_stats.get_survival_time_str()}",
                    f"Damage: {int(game_stats.damage_dealt)}",
                    f"Power-ups: {game_stats.power_ups_collected}",
                    f"Abilities: {game_stats.abilities_cast}",
                    f"Dmg Taken: {int(game_stats.damage_taken)}"
                ]

                for stat in right_stats:
                    stat_surf = self.medium_font.render(stat, True, GOTHIC_BONE)
                    stat_rect = stat_surf.get_rect(midleft=(right_x, stats_y))
                    self.screen.blit(stat_surf, stat_rect)
                    stats_y += 40

        # Instructions panel
        inst_panel_rect = pygame.Rect(WINDOW_WIDTH // 2 - 200, WINDOW_HEIGHT - 120, 400, 80)
        GothicPanel.draw(self.screen, inst_panel_rect, GOTHIC_SHADOW, GOTHIC_PURPLE, BORDER_THIN)

        inst_y = WINDOW_HEIGHT - 100
        instructions = [
            "ESC - Resume Game",
            "Q - Quit to Menu"
        ]

        for i, inst in enumerate(instructions):
            inst_surf = self.small_font.render(inst, True, GOTHIC_SILVER)
            inst_rect = inst_surf.get_rect(center=(WINDOW_WIDTH // 2, inst_y + i * 30))
            self.screen.blit(inst_surf, inst_rect)

    def _render_game_over(self):
        """Render game over screen with Gothic UI (Sprint 24)"""
        self.screen.fill(GOTHIC_BLACK)

        # Draw ornate border
        draw_ornate_border(self.screen, GLOW_CRIMSON, BORDER_ORNATE)

        # Gothic title
        GothicHeader.draw(self.screen, "DEFEATED", 50, self.title_font, GLOW_CRIMSON, decoration=True)

        # High score indicator
        if self.is_new_high_score:
            hs_text = self.large_font.render("🏆 NEW HIGH SCORE! 🏆", True, GOTHIC_GOLD)
            hs_rect = hs_text.get_rect(center=(WINDOW_WIDTH // 2, 120))
            self.screen.blit(hs_text, hs_rect)

        # Character info
        char_text = f"{self.selected_class.name}"
        char_surf = self.medium_font.render(char_text, True, self.selected_class.color)
        char_rect = char_surf.get_rect(center=(WINDOW_WIDTH // 2, 165))
        self.screen.blit(char_surf, char_rect)

        # Score panel
        score_panel_rect = pygame.Rect(WINDOW_WIDTH // 2 - 250, 200, 500, 70)
        GothicPanel.draw(self.screen, score_panel_rect, GOTHIC_SHADOW, GOTHIC_GOLD, BORDER_ORNATE)

        score_text = f"SCORE: {self.final_score:,}"
        score_surf = self.large_font.render(score_text, True, GOTHIC_GOLD)
        score_rect = score_surf.get_rect(center=(WINDOW_WIDTH // 2, 235))
        self.screen.blit(score_surf, score_rect)

        # Get player stats
        player_entities = self.world.get_entities_with_components(Player, GameStats, Experience)
        if player_entities:
            player = player_entities[0]
            game_stats = player.get_component(GameStats)
            xp = player.get_component(Experience)

            # Stats columns
            left_x = WINDOW_WIDTH // 2 - 200
            right_x = WINDOW_WIDTH // 2 + 200
            stats_y = 300

            # Left column
            left_stats = [
                f"⚔️  Kills: {game_stats.kills}",
                f"💀 Bosses: {game_stats.bosses_killed}",
                f"🌊 Wave: {game_stats.highest_wave}",
                f"⬆️  Level: {xp.level}",
            ]

            for stat in left_stats:
                stat_surf = self.small_font.render(stat, True, GOTHIC_BONE)
                stat_rect = stat_surf.get_rect(midleft=(left_x, stats_y))
                self.screen.blit(stat_surf, stat_rect)
                stats_y += 35

            # Right column
            stats_y = 300
            right_stats = [
                f"⏱️  Time: {game_stats.get_survival_time_str()}",
                f"✨ Power-ups: {game_stats.power_ups_collected}",
                f"🎯 Damage: {int(game_stats.damage_dealt)}",
                f"💥 Abilities: {game_stats.abilities_cast}",
            ]

            for stat in right_stats:
                stat_surf = self.small_font.render(stat, True, GOTHIC_BONE)
                stat_rect = stat_surf.get_rect(midleft=(right_x, stats_y))
                self.screen.blit(stat_surf, stat_rect)
                stats_y += 35

        # High scores panel
        hs_panel_rect = pygame.Rect(WINDOW_WIDTH // 2 - 300, 440, 600, 200)
        GothicPanel.draw(self.screen, hs_panel_rect, GOTHIC_SHADOW, GLOW_ARCANE, BORDER_MEDIUM)

        hs_title = self.medium_font.render("TOP SCORES", True, GLOW_ARCANE)
        hs_title_rect = hs_title.get_rect(center=(WINDOW_WIDTH // 2, 465))
        self.screen.blit(hs_title, hs_title_rect)

        high_scores = self.persistent_stats.data["high_scores"][:5]  # Top 5
        hs_y = 505
        for i, entry in enumerate(high_scores):
            rank = i + 1
            score_line = f"{rank}. {entry['character'][:12]:<12} {entry['score']:>6,}  Lv.{entry['level']:<2}  W{entry['wave']:<2}"
            color = GOTHIC_GOLD if rank == 1 else GOTHIC_SILVER
            score_surf = self.small_font.render(score_line, True, color)
            score_rect = score_surf.get_rect(center=(WINDOW_WIDTH // 2, hs_y))
            self.screen.blit(score_surf, score_rect)
            hs_y += 26

        # Instructions panel
        inst_panel_rect = pygame.Rect(WINDOW_WIDTH // 2 - 250, WINDOW_HEIGHT - 80, 500, 50)
        GothicPanel.draw(self.screen, inst_panel_rect, GOTHIC_SHADOW, GOTHIC_PURPLE, BORDER_THIN)

        inst_y = WINDOW_HEIGHT - 55
        inst1 = self.small_font.render("SPACE - Restart  |  ESC - Menu", True, GOTHIC_SILVER)
        inst1_rect = inst1.get_rect(center=(WINDOW_WIDTH // 2, inst_y))
        self.screen.blit(inst1, inst1_rect)

    def _check_level_up(self):
        """Check if player leveled up and needs weapon choice"""
        player_entities = self.world.get_entities_with_components(Player, LevelUpPending, WeaponInventory)

        if player_entities:
            player = player_entities[0]
            inventory = player.get_component(WeaponInventory)

            # Generate choices
            choice_system = LevelUpChoiceSystem(self.world)
            self.level_up_choices = choice_system.generate_choices(inventory)
            self.selected_choice_index = 0

            # Pause game for level-up
            self.state = GameState.LEVEL_UP

            # Remove pending component
            player.remove_component(LevelUpPending)

    def _apply_weapon_choice(self):
        """Apply selected weapon upgrade or evolution"""
        if not self.level_up_choices:
            self.state = GameState.PLAYING
            return

        choice = self.level_up_choices[self.selected_choice_index]
        weapon_id = choice['weapon_id']

        # Get player inventory
        player_entities = self.world.get_entities_with_components(Player, WeaponInventory)
        if not player_entities:
            self.state = GameState.PLAYING
            return

        inventory = player_entities[0].get_component(WeaponInventory)

        # Check if this is an evolution
        if choice.get('is_evolution', False):
            evolution_data = choice['evolution_data']

            # Evolve weapon
            inventory.evolve_weapon(weapon_id, evolution_data.evolved_id)

            # Track evolution stat (Sprint 19)
            from src.systems.stats_system import GameStats
            if player_entities[0].has_component(GameStats):
                stats = player_entities[0].get_component(GameStats)
                stats.weapons_evolved += 1

            # Create evolution announcement
            print(f"⚡ EVOLUTION! {evolution_data.evolved_icon} {evolution_data.base_weapon_id.upper()} → {evolution_data.evolved_name.upper()}")

            # Play evolution effect
            from src.systems.particle_system import create_level_up_particles
            player_pos = player_entities[0].get_component(Position)
            if player_pos:
                create_level_up_particles(self.world, player_pos.x, player_pos.y, 80)  # 2x particles

        else:
            # Regular upgrade
            inventory.upgrade_weapon(weapon_id)

            weapon_data = choice['weapon_data']
            new_level = inventory.get_level(weapon_id)

            print(f"🔼 {weapon_data.icon} {weapon_data.name} → Level {new_level}")

        # Resume game
        self.state = GameState.PLAYING
        self.level_up_choices = []

    def _render_level_up(self):
        """Render level-up weapon selection screen with Gothic UI (Sprint 24)"""
        # Render game in background (paused)
        self.world.update(0)

        # Gothic dark overlay
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
        overlay.fill(OVERLAY_DARK)
        self.screen.blit(overlay, (0, 0))

        # Gothic title
        GothicHeader.draw(self.screen, "LEVEL UP!", 60, self.large_font, GOTHIC_GOLD, decoration=True)

        # Instructions (Sprint 28: Replace arrow emojis with text)
        inst = self.small_font.render("LEFT/RIGHT to Select | SPACE to Choose", True, GOTHIC_SILVER)
        inst_rect = inst.get_rect(center=(WINDOW_WIDTH // 2, 115))
        self.screen.blit(inst, inst_rect)

        if not self.level_up_choices:
            return

        # Display weapon choices (3 cards)
        card_width = 280
        card_height = 320
        card_spacing = 40
        total_width = len(self.level_up_choices) * card_width + (len(self.level_up_choices) - 1) * card_spacing
        start_x = (WINDOW_WIDTH - total_width) // 2
        start_y = 200

        for i, choice in enumerate(self.level_up_choices):
            x = start_x + i * (card_width + card_spacing)
            is_selected = (i == self.selected_choice_index)

            # Check if this is an evolution choice
            is_evolution = choice.get('is_evolution', False)

            if is_evolution:
                # Evolution card rendering
                evolution_data = choice['evolution_data']
                from src.components.weapons import get_weapon_by_id
                evolved_weapon = get_weapon_by_id(evolution_data.evolved_id)

                # Gothic evolution card
                card_color = evolved_weapon.color if is_selected else GOTHIC_PURPLE
                border_color = GOTHIC_GOLD if is_selected else (200, 150, 50)  # Golden
                border_width = BORDER_ORNATE if is_selected else BORDER_THICK

                card_rect = pygame.Rect(x, start_y, card_width, card_height)
                GothicPanel.draw(self.screen, card_rect, card_color, border_color, border_width)

                # EVOLUTION banner
                evo_banner = self.medium_font.render("⚡ EVOLUTION ⚡", True, (255, 215, 0))
                evo_rect = evo_banner.get_rect(center=(x + card_width // 2, start_y + 30))
                self.screen.blit(evo_banner, evo_rect)

                # Evolved icon (Sprint 28: Pixel art sprite)
                from src.core.asset_manager import asset_manager
                weapon_icon = asset_manager.get_sprite(f'weapon_{choice["weapon_id"]}')
                if weapon_icon:
                    # Scale up 2x for better visibility (32x32 → 64x64)
                    scaled_icon = pygame.transform.scale(weapon_icon, (64, 64))
                    icon_rect = scaled_icon.get_rect(center=(x + card_width // 2, start_y + 80))
                    self.screen.blit(scaled_icon, icon_rect)
                else:
                    # Fallback: emoji (if sprite not found)
                    icon_surf = self.title_font.render(evolution_data.evolved_icon, True, GOTHIC_BONE)
                    icon_rect = icon_surf.get_rect(center=(x + card_width // 2, start_y + 80))
                    self.screen.blit(icon_surf, icon_rect)

                # Evolved name
                name_surf = self.medium_font.render(evolution_data.evolved_name, True, GOTHIC_GOLD)
                name_rect = name_surf.get_rect(center=(x + card_width // 2, start_y + 130))
                self.screen.blit(name_surf, name_rect)

                # Stats preview
                damage = evolved_weapon.damage_per_level[0]
                cooldown = evolved_weapon.cooldown_per_level[0]

                stats_text = [
                    f"Damage: {int(damage)}",
                    f"Cooldown: {cooldown:.1f}s",
                ]

                stat_y = start_y + 170
                for stat in stats_text:
                    stat_surf = self.small_font.render(stat, True, (255, 215, 0))
                    stat_rect = stat_surf.get_rect(center=(x + card_width // 2, stat_y))
                    self.screen.blit(stat_surf, stat_rect)
                    stat_y += 25

                # Description
                desc_lines = self._wrap_text(evolution_data.evolved_description, 28)
                desc_y = stat_y + 10
                for line in desc_lines:
                    desc_surf = self.small_font.render(line, True, (220, 220, 220))
                    desc_rect = desc_surf.get_rect(center=(x + card_width // 2, desc_y))
                    self.screen.blit(desc_surf, desc_rect)
                    desc_y += 20

            else:
                # Regular weapon card with Gothic UI
                weapon_data = choice['weapon_data']
                current_level = choice['current_level']
                next_level = choice['next_level']
                is_new = choice['is_new']

                # Gothic card background
                card_color = weapon_data.color if is_selected else GOTHIC_SHADOW
                border_color = GOTHIC_GOLD if is_selected else GOTHIC_PURPLE
                border_width = BORDER_THICK if is_selected else BORDER_MEDIUM

                card_rect = pygame.Rect(x, start_y, card_width, card_height)
                GothicPanel.draw(self.screen, card_rect, card_color, border_color, border_width)

                # Weapon icon (Sprint 28: Pixel art sprite instead of emoji)
                from src.core.asset_manager import asset_manager
                weapon_icon = asset_manager.get_sprite(f'weapon_{choice["weapon_id"]}')
                if weapon_icon:
                    # Scale up 2x for better visibility (32x32 → 64x64)
                    scaled_icon = pygame.transform.scale(weapon_icon, (64, 64))
                    icon_rect = scaled_icon.get_rect(center=(x + card_width // 2, start_y + 60))
                    self.screen.blit(scaled_icon, icon_rect)
                else:
                    # Fallback: emoji (if sprite not found)
                    icon_surf = self.title_font.render(weapon_data.icon, True, GOTHIC_BONE)
                    icon_rect = icon_surf.get_rect(center=(x + card_width // 2, start_y + 60))
                    self.screen.blit(icon_surf, icon_rect)

                # Weapon name
                name_color = GOTHIC_BONE if is_selected else GOTHIC_SILVER
                name_surf = self.medium_font.render(weapon_data.name, True, name_color)
                name_rect = name_surf.get_rect(center=(x + card_width // 2, start_y + 120))
                self.screen.blit(name_surf, name_rect)

                # Level indicator
                if is_new:
                    level_text = "NEW!"
                    level_color = GOTHIC_GOLD
                else:
                    level_text = f"Lv {current_level} → {next_level}"
                    level_color = GLOW_ARCANE

                level_surf = self.small_font.render(level_text, True, level_color)
                level_rect = level_surf.get_rect(center=(x + card_width // 2, start_y + 155))
                self.screen.blit(level_surf, level_rect)

                # Stats
                level_idx = next_level - 1
                damage = weapon_data.damage_per_level[level_idx]
                cooldown = weapon_data.cooldown_per_level[level_idx]

                stats_text = [
                    f"Damage: {int(damage)}",
                    f"Cooldown: {cooldown:.1f}s",
                ]

                stat_y = start_y + 190
                for stat in stats_text:
                    stat_surf = self.small_font.render(stat, True, GOTHIC_BONE)
                    stat_rect = stat_surf.get_rect(center=(x + card_width // 2, stat_y))
                    self.screen.blit(stat_surf, stat_rect)
                    stat_y += 25

                # Description
                desc_lines = self._wrap_text(weapon_data.description, 28)
                desc_y = stat_y + 10
                for line in desc_lines:
                    desc_surf = self.small_font.render(line, True, GOTHIC_MIST)
                    desc_rect = desc_surf.get_rect(center=(x + card_width // 2, desc_y))
                    self.screen.blit(desc_surf, desc_rect)
                    desc_y += 20

        # Sprint 28: Visual arrow indicators (pixel art triangles)
        arrow_y = start_y + card_height // 2
        arrow_size = 40

        # Left arrow (if not first card)
        if self.selected_choice_index > 0:
            # Draw left-pointing triangle
            left_arrow_x = start_x - 80
            left_points = [
                (left_arrow_x, arrow_y),                        # Left point
                (left_arrow_x + arrow_size, arrow_y - arrow_size // 2),  # Top
                (left_arrow_x + arrow_size, arrow_y + arrow_size // 2)   # Bottom
            ]
            pygame.draw.polygon(self.screen, GOTHIC_GOLD, left_points)
            pygame.draw.polygon(self.screen, GOTHIC_BONE, left_points, 3)  # Border

        # Right arrow (if not last card)
        if self.selected_choice_index < len(self.level_up_choices) - 1:
            # Draw right-pointing triangle
            right_arrow_x = start_x + (len(self.level_up_choices) * (card_width + card_spacing)) - card_spacing + 40
            right_points = [
                (right_arrow_x + arrow_size, arrow_y),          # Right point
                (right_arrow_x, arrow_y - arrow_size // 2),     # Top
                (right_arrow_x, arrow_y + arrow_size // 2)      # Bottom
            ]
            pygame.draw.polygon(self.screen, GOTHIC_GOLD, right_points)
            pygame.draw.polygon(self.screen, GOTHIC_BONE, right_points, 3)  # Border


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
