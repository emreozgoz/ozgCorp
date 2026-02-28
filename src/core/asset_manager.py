"""
DARK SANCTUM - Asset Management System
Matrix Team: Technical Director + Developer

Sprint 21: Sprite system foundation for visual enhancement
"""

import pygame
import os
from typing import Dict, List, Tuple, Optional


class SpriteSheet:
    """Sprite sheet parser for animated sprites"""

    def __init__(self, image: pygame.Surface, frame_width: int, frame_height: int):
        self.image = image
        self.frame_width = frame_width
        self.frame_height = frame_height

    def get_frames(self, row: int, num_frames: int) -> List[pygame.Surface]:
        """Extract frames from a row in the sprite sheet"""
        frames = []
        for i in range(num_frames):
            x = i * self.frame_width
            y = row * self.frame_height

            frame = pygame.Surface((self.frame_width, self.frame_height), pygame.SRCALPHA)
            frame.blit(self.image, (0, 0), (x, y, self.frame_width, self.frame_height))
            frames.append(frame)

        return frames

    def get_frame(self, row: int, col: int) -> pygame.Surface:
        """Get single frame from sprite sheet"""
        x = col * self.frame_width
        y = row * self.frame_height

        frame = pygame.Surface((self.frame_width, self.frame_height), pygame.SRCALPHA)
        frame.blit(self.image, (0, 0), (x, y, self.frame_width, self.frame_height))

        return frame


class AssetManager:
    """Centralized asset loading and caching system"""

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(AssetManager, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return

        self._initialized = True
        self.sprites: Dict[str, pygame.Surface] = {}
        self.sprite_sheets: Dict[str, SpriteSheet] = {}
        self.fonts: Dict[str, pygame.font.Font] = {}

        # Asset paths
        self.assets_dir = "assets"
        self.sprites_dir = os.path.join(self.assets_dir, "sprites")
        self.fonts_dir = os.path.join(self.assets_dir, "fonts")

        # Create directories if they don't exist
        os.makedirs(self.sprites_dir, exist_ok=True)
        os.makedirs(self.fonts_dir, exist_ok=True)

        # Pre-load all game sprites (Sprint 26)
        self._preload_sprites()

    def load_sprite(self, path: str, key: Optional[str] = None) -> pygame.Surface:
        """Load and cache a single sprite"""
        cache_key = key or path

        if cache_key in self.sprites:
            return self.sprites[cache_key]

        full_path = os.path.join(self.sprites_dir, path)

        try:
            sprite = pygame.image.load(full_path).convert_alpha()
            self.sprites[cache_key] = sprite
            return sprite
        except FileNotFoundError:
            print(f"⚠️  Sprite not found: {full_path}, using placeholder")
            return self._create_placeholder(32, 32)

    def load_sprite_sheet(self, path: str, frame_width: int, frame_height: int, key: Optional[str] = None) -> SpriteSheet:
        """Load and cache a sprite sheet"""
        cache_key = key or path

        if cache_key in self.sprite_sheets:
            return self.sprite_sheets[cache_key]

        full_path = os.path.join(self.sprites_dir, path)

        try:
            image = pygame.image.load(full_path).convert_alpha()
            sprite_sheet = SpriteSheet(image, frame_width, frame_height)
            self.sprite_sheets[cache_key] = sprite_sheet
            return sprite_sheet
        except FileNotFoundError:
            print(f"⚠️  Sprite sheet not found: {full_path}, using placeholder")
            # Create placeholder sprite sheet
            placeholder_image = self._create_placeholder(frame_width * 4, frame_height)
            sprite_sheet = SpriteSheet(placeholder_image, frame_width, frame_height)
            self.sprite_sheets[cache_key] = sprite_sheet
            return sprite_sheet

    def load_font(self, path: Optional[str], size: int, key: Optional[str] = None) -> pygame.font.Font:
        """Load and cache a font"""
        cache_key = key or f"{path}_{size}"

        if cache_key in self.fonts:
            return self.fonts[cache_key]

        if path:
            full_path = os.path.join(self.fonts_dir, path)
            try:
                font = pygame.font.Font(full_path, size)
                self.fonts[cache_key] = font
                return font
            except FileNotFoundError:
                print(f"⚠️  Font not found: {full_path}, using default")

        # Use default font
        font = pygame.font.Font(None, size)
        self.fonts[cache_key] = font
        return font

    def _create_placeholder(self, width: int, height: int, color: Tuple[int, int, int, int] = (255, 0, 255, 255)) -> pygame.Surface:
        """Create a placeholder sprite (magenta for visibility)"""
        surface = pygame.Surface((width, height), pygame.SRCALPHA)
        surface.fill(color)

        # Draw X pattern to indicate placeholder
        pygame.draw.line(surface, (0, 0, 0), (0, 0), (width, height), 2)
        pygame.draw.line(surface, (0, 0, 0), (width, 0), (0, height), 2)

        return surface

    def create_procedural_sprite(self, sprite_type: str, size: int = 32) -> pygame.Surface:
        """Create procedural sprites for entities (temporary until real assets)"""
        surface = pygame.Surface((size, size), pygame.SRCALPHA)

        if sprite_type == "player_shadow_knight":
            # Dark knight with purple glow
            pygame.draw.circle(surface, (45, 27, 61), (size // 2, size // 2), size // 2)
            pygame.draw.circle(surface, (120, 80, 160), (size // 2, size // 2), size // 2 - 2, 2)
            pygame.draw.circle(surface, (200, 200, 200), (size // 2, size // 3), 3)  # Helmet

        elif sprite_type == "player_blood_mage":
            # Red robed mage
            pygame.draw.circle(surface, (139, 0, 0), (size // 2, size // 2), size // 2)
            pygame.draw.circle(surface, (255, 50, 50), (size // 2, size // 2), size // 2 - 2, 2)
            pygame.draw.circle(surface, (100, 50, 0), (size // 2, size // 3), 4)  # Staff

        elif sprite_type == "player_void_guardian":
            # Heavy tank with shield
            pygame.draw.circle(surface, (70, 70, 70), (size // 2, size // 2), size // 2)
            pygame.draw.circle(surface, (150, 150, 150), (size // 2, size // 2), size // 2 - 2, 3)
            pygame.draw.rect(surface, (180, 180, 180), (size // 4, size // 4, size // 3, size // 2))  # Shield

        elif sprite_type == "player_necromancer":
            # Hooded dark figure
            pygame.draw.circle(surface, (40, 40, 40), (size // 2, size // 2), size // 2)
            pygame.draw.circle(surface, (80, 200, 80), (size // 2, size // 2), size // 2 - 2, 2)  # Green glow
            pygame.draw.circle(surface, (50, 50, 50), (size // 2, size // 3), 5)  # Hood

        elif sprite_type == "player_tempest_ranger":
            # Swift archer
            pygame.draw.circle(surface, (100, 120, 100), (size // 2, size // 2), size // 2)
            pygame.draw.circle(surface, (150, 200, 150), (size // 2, size // 2), size // 2 - 2, 2)
            pygame.draw.line(surface, (139, 69, 19), (size // 4, size // 2), (size * 3 // 4, size // 2), 3)  # Bow

        elif sprite_type == "enemy_basic":
            # Zombie/undead
            pygame.draw.circle(surface, (80, 100, 80), (size // 2, size // 2), size // 2)
            pygame.draw.circle(surface, (150, 255, 150, 100), (size // 2, size // 2), size // 2, 1)

        elif sprite_type == "enemy_imp":
            # Small demon
            pygame.draw.circle(surface, (150, 50, 50), (size // 2, size // 2), size // 2)
            pygame.draw.polygon(surface, (200, 0, 0), [(size // 4, size // 4), (size // 2, 0), (size * 3 // 4, size // 4)])  # Horns

        elif sprite_type == "enemy_golem":
            # Stone creature
            pygame.draw.rect(surface, (100, 100, 100), (size // 4, size // 4, size // 2, size // 2))
            pygame.draw.rect(surface, (150, 150, 150), (size // 4, size // 4, size // 2, size // 2), 2)

        elif sprite_type == "enemy_wraith":
            # Ghostly figure
            pygame.draw.circle(surface, (150, 150, 200, 150), (size // 2, size // 2), size // 2)
            pygame.draw.circle(surface, (200, 200, 255, 100), (size // 2, size // 2), size // 2 - 2, 2)

        elif sprite_type.startswith("boss_"):
            # Larger boss sprite with unique colors
            boss_colors = {
                "boss_blood_titan": (139, 0, 0),
                "boss_void_reaver": (80, 40, 120),
                "boss_frost_colossus": (100, 150, 200),
                "boss_plague_herald": (120, 200, 80),
                "boss_inferno_lord": (255, 100, 20)
            }
            color = boss_colors.get(sprite_type, (255, 0, 0))
            pygame.draw.circle(surface, color, (size // 2, size // 2), size // 2)
            pygame.draw.circle(surface, (255, 255, 255), (size // 2, size // 2), size // 2 - 4, 4)  # Crown/aura

        else:
            # Generic placeholder
            pygame.draw.circle(surface, (255, 0, 255), (size // 2, size // 2), size // 2)

        return surface

    def _preload_sprites(self):
        """Pre-load all game sprites (Sprint 26)"""
        sprite_map = {
            # Characters
            'shadow_knight': 'characters/shadow_knight.png',
            'blood_mage': 'characters/blood_mage.png',
            'void_guardian': 'characters/void_guardian.png',
            'necromancer': 'characters/necromancer.png',
            'tempest_ranger': 'characters/tempest_ranger.png',

            # Enemies
            'enemy_basic': 'enemies/basic.png',
            'enemy_imp': 'enemies/imp.png',
            'enemy_golem': 'enemies/golem.png',
            'enemy_wraith': 'enemies/wraith.png',

            # Bosses
            'boss_blood_titan': 'bosses/blood_titan.png',
            'boss_void_reaver': 'bosses/void_reaver.png',
            'boss_frost_colossus': 'bosses/frost_colossus.png',
            'boss_plague_herald': 'bosses/plague_herald.png',
            'boss_inferno_lord': 'bosses/inferno_lord.png',
        }

        print("🎨 Loading sprites...")
        loaded_count = 0
        for key, path in sprite_map.items():
            try:
                self.load_sprite(path, key)
                loaded_count += 1
            except Exception as e:
                print(f"⚠️  Failed to load {key}: {e}")

        print(f"✅ Loaded {loaded_count}/{len(sprite_map)} sprites")

    def get_sprite(self, key: str) -> Optional[pygame.Surface]:
        """Get a cached sprite by key"""
        return self.sprites.get(key)

    def clear_cache(self):
        """Clear all cached assets"""
        self.sprites.clear()
        self.sprite_sheets.clear()
        self.fonts.clear()


# Singleton instance
asset_manager = AssetManager()


# === TECHNICAL DIRECTOR NOTE ===
# Sprint 21: Asset management foundation
# - Singleton pattern for global access
# - Sprite caching for performance
# - Sprite sheet parsing for animations
# - Placeholder generation until real assets
# - Procedural sprites for immediate visual upgrade
# - Ready for Sprint 22 art asset integration
