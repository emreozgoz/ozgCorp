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
            sprite = pygame.image.load(full_path)
            # Try convert_alpha, fall back to plain surface if display not initialized
            try:
                sprite = sprite.convert_alpha()
            except pygame.error:
                # Display not initialized yet, use raw surface
                pass
            self.sprites[cache_key] = sprite
            return sprite
        except FileNotFoundError:
            print(f"⚠️  Sprite not found: {full_path}, using placeholder")
            return self._create_placeholder(32, 32)
        except Exception as e:
            print(f"⚠️  Failed to load {cache_key}: {e}")
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

    def create_weapon_icon(self, weapon_id: str, size: int = 32) -> pygame.Surface:
        """Create pixel art weapon icons for UI (Sprint 28)"""
        surface = pygame.Surface((size, size), pygame.SRCALPHA)
        center = (size // 2, size // 2)

        if weapon_id == "arcane_seeker":
            # Purple crystal orb with sparkles (BRIGHTER colors for visibility)
            # Outer glow
            pygame.draw.circle(surface, (120, 80, 220), center, 14)
            # Main crystal
            pygame.draw.circle(surface, (120, 80, 200), center, 12)
            pygame.draw.circle(surface, (180, 140, 255), center, 8)
            # Inner glow
            pygame.draw.circle(surface, (220, 200, 255), center, 4)
            # Sparkles at corners
            sparkle_positions = [(8, 8), (24, 8), (8, 24), (24, 24)]
            for pos in sparkle_positions:
                pygame.draw.circle(surface, (200, 180, 255), pos, 2)
                pygame.draw.circle(surface, (255, 255, 255), pos, 1)

        elif weapon_id == "blood_whip":
            # Red curved blade/whip (BRIGHTER for visibility)
            # Handle (bottom)
            pygame.draw.rect(surface, (80, 40, 40), (12, 20, 8, 10))
            # Blade curve (bright red)
            blade_points = [(16, 20), (20, 15), (24, 10), (26, 6), (24, 4)]
            pygame.draw.lines(surface, (220, 40, 40), False, blade_points, 4)
            pygame.draw.lines(surface, (255, 80, 80), False, blade_points, 2)
            # Blood drips
            pygame.draw.circle(surface, (200, 0, 0), (22, 12), 2)
            pygame.draw.circle(surface, (180, 20, 20), (18, 16), 1)

        elif weapon_id == "lightning_orb":
            # Yellow lightning bolt
            # Outer electric glow
            pygame.draw.circle(surface, (255, 255, 100, 80), center, 14)
            # Main lightning bolt (zigzag)
            bolt_points = [(16, 6), (14, 12), (18, 14), (15, 20), (20, 16), (17, 24)]
            pygame.draw.lines(surface, (255, 255, 100), False, bolt_points, 4)
            # White core
            pygame.draw.lines(surface, (255, 255, 255), False, bolt_points, 2)
            # Electric sparks
            spark_positions = [(10, 10), (22, 10), (10, 22), (22, 22)]
            for pos in spark_positions:
                pygame.draw.line(surface, (255, 255, 200), pos, (pos[0]+2, pos[1]+2), 1)

        elif weapon_id == "toxic_cloud":
            # Green poison flask with bubbles (BRIGHTER for visibility)
            # Flask body
            pygame.draw.rect(surface, (100, 200, 100), (10, 14, 12, 14), border_radius=2)
            # Flask neck
            pygame.draw.rect(surface, (80, 160, 80), (13, 10, 6, 6))
            # Cork/cap
            pygame.draw.rect(surface, (180, 120, 60), (13, 8, 6, 3))
            # Liquid inside (bright green)
            pygame.draw.rect(surface, (140, 255, 140), (11, 16, 10, 10))
            # Bubbles
            bubble_positions = [(14, 18), (18, 20), (15, 24)]
            for pos in bubble_positions:
                pygame.draw.circle(surface, (180, 255, 180), pos, 2)
                pygame.draw.circle(surface, (240, 255, 240), pos, 1)
            # Skull symbol (small)
            pygame.draw.circle(surface, (80, 140, 80), (16, 20), 3)

        elif weapon_id == "holy_barrier":
            # Golden shield with cross
            pygame.draw.circle(surface, (255, 215, 0), center, 14, 3)
            pygame.draw.circle(surface, (255, 200, 50), center, 11, 2)
            pygame.draw.line(surface, (255, 215, 0), (16, 8), (16, 24), 3)
            pygame.draw.line(surface, (255, 215, 0), (10, 16), (22, 16), 3)
            pygame.draw.circle(surface, (255, 255, 200), (13, 13), 3)
            pygame.draw.circle(surface, (255, 255, 255), (13, 13), 1)

        # Sprint 29: Add all remaining weapons
        elif weapon_id == "sword":
            # Silver sword
            pygame.draw.polygon(surface, (180, 180, 200), [(16, 6), (18, 6), (18, 22), (16, 22)])
            pygame.draw.polygon(surface, (220, 220, 240), [(15, 22), (19, 22), (17, 26)])
            pygame.draw.rect(surface, (150, 120, 80), (15, 22, 4, 4))
            pygame.draw.circle(surface, (255, 255, 255), (17, 10), 1)

        elif weapon_id == "magic_missile":
            # Purple magic missile
            missile_points = [(16, 8), (20, 16), (16, 24), (12, 16)]
            pygame.draw.polygon(surface, (150, 80, 200), missile_points)
            pygame.draw.polygon(surface, (200, 120, 255), missile_points, 2)
            pygame.draw.circle(surface, (255, 200, 255), center, 4)

        elif weapon_id == "lightning":
            # Yellow lightning (similar to lightning_orb)
            bolt_points = [(16, 6), (14, 12), (18, 14), (15, 20), (20, 16), (17, 24)]
            pygame.draw.lines(surface, (255, 255, 100), False, bolt_points, 4)
            pygame.draw.lines(surface, (255, 255, 255), False, bolt_points, 2)

        elif weapon_id == "holy_water":
            # Blue holy water bottle
            pygame.draw.rect(surface, (100, 150, 255), (12, 14, 8, 12), border_radius=2)
            pygame.draw.rect(surface, (80, 120, 200), (13, 10, 6, 5))
            pygame.draw.rect(surface, (150, 200, 255), (13, 16, 6, 8))
            pygame.draw.circle(surface, (200, 230, 255), (16, 18), 2)

        elif weapon_id == "garlic":
            # White garlic aura
            pygame.draw.circle(surface, (240, 240, 240), center, 12)
            pygame.draw.circle(surface, (255, 255, 255), center, 8)
            for angle in [0, 90, 180, 270]:
                import math
                x = int(center[0] + 10 * math.cos(math.radians(angle)))
                y = int(center[1] + 10 * math.sin(math.radians(angle)))
                pygame.draw.circle(surface, (255, 255, 240), (x, y), 3)

        elif weapon_id == "shadow_scythe":
            # Dark purple scythe
            pygame.draw.arc(surface, (80, 40, 120), (8, 8, 16, 16), 0, 3.14, 4)
            pygame.draw.line(surface, (60, 30, 90), (16, 16), (16, 26), 3)
            pygame.draw.polygon(surface, (100, 50, 150), [(24, 8), (16, 12), (20, 16)])

        elif weapon_id == "frost_nova":
            # Light blue frost
            pygame.draw.circle(surface, (150, 200, 255), center, 12)
            pygame.draw.circle(surface, (200, 230, 255), center, 8)
            # Snowflake pattern
            for angle in [0, 60, 120, 180, 240, 300]:
                import math
                x1 = int(center[0] + 4 * math.cos(math.radians(angle)))
                y1 = int(center[1] + 4 * math.sin(math.radians(angle)))
                x2 = int(center[0] + 10 * math.cos(math.radians(angle)))
                y2 = int(center[1] + 10 * math.sin(math.radians(angle)))
                pygame.draw.line(surface, (255, 255, 255), (x1, y1), (x2, y2), 2)

        elif weapon_id == "blood_lance":
            # Dark red lance
            pygame.draw.polygon(surface, (180, 40, 40), [(16, 4), (18, 4), (17, 24)])
            pygame.draw.polygon(surface, (220, 60, 60), [(16, 4), (17, 12), (18, 4)])
            pygame.draw.rect(surface, (100, 40, 40), (15, 24, 4, 4))

        elif weapon_id == "soul_reaver":
            # Purple soul energy
            pygame.draw.circle(surface, (140, 80, 180, 150), center, 12)
            pygame.draw.circle(surface, (180, 120, 220), center, 8)
            pygame.draw.circle(surface, (220, 160, 255), center, 4)
            # Wisps
            for pos in [(10, 10), (22, 10), (10, 22), (22, 22)]:
                pygame.draw.circle(surface, (200, 150, 255), pos, 2)

        elif weapon_id == "bone_storm":
            # White bones
            pygame.draw.rect(surface, (240, 240, 230), (14, 10, 4, 12))
            pygame.draw.rect(surface, (240, 240, 230), (10, 14, 12, 4))
            pygame.draw.circle(surface, (220, 220, 210), (12, 12), 2)
            pygame.draw.circle(surface, (220, 220, 210), (20, 20), 2)

        elif weapon_id == "cursed_tome":
            # Dark purple book
            pygame.draw.rect(surface, (80, 40, 100), (10, 12, 12, 8))
            pygame.draw.rect(surface, (120, 60, 140), (11, 13, 10, 6))
            pygame.draw.line(surface, (200, 150, 220), (16, 14), (16, 18), 1)

        elif weapon_id == "poison_dagger":
            # Green poison dagger
            pygame.draw.polygon(surface, (100, 200, 100), [(16, 8), (18, 8), (17, 20)])
            pygame.draw.polygon(surface, (140, 255, 140), [(16, 8), (17, 14), (18, 8)])
            pygame.draw.rect(surface, (80, 120, 60), (15, 20, 4, 4))
            pygame.draw.circle(surface, (120, 255, 120), (17, 12), 2)

        elif weapon_id == "void_lance":
            # Dark void lance
            pygame.draw.polygon(surface, (60, 40, 80), [(16, 4), (18, 4), (17, 24)])
            pygame.draw.circle(surface, (100, 80, 140), (17, 14), 6)
            pygame.draw.circle(surface, (140, 120, 180), (17, 14), 3)

        elif weapon_id == "reapers_embrace":
            # Dark scythe
            pygame.draw.arc(surface, (40, 40, 60), (6, 6, 20, 20), 0, 3.14, 5)
            pygame.draw.line(surface, (30, 30, 50), (16, 16), (16, 28), 4)
            pygame.draw.circle(surface, (100, 100, 120), (16, 10), 3)

        elif weapon_id == "cosmic_annihilation":
            # Cosmic purple/blue
            pygame.draw.circle(surface, (100, 80, 180), center, 14)
            pygame.draw.circle(surface, (140, 120, 220), center, 10)
            pygame.draw.circle(surface, (180, 160, 255), center, 6)
            pygame.draw.circle(surface, (255, 255, 255), center, 2)

        elif weapon_id == "sacred_ward":
            # Golden protection
            pygame.draw.circle(surface, (255, 215, 0), center, 13, 4)
            pygame.draw.circle(surface, (255, 235, 100), center, 9, 3)
            pygame.draw.circle(surface, (255, 255, 200), center, 5)

        elif weapon_id == "storm_bringer":
            # Lightning storm
            pygame.draw.circle(surface, (100, 100, 200, 100), center, 13)
            bolt_1 = [(12, 8), (14, 12), (12, 16), (14, 20)]
            bolt_2 = [(20, 8), (18, 12), (20, 16), (18, 20)]
            pygame.draw.lines(surface, (255, 255, 150), False, bolt_1, 2)
            pygame.draw.lines(surface, (255, 255, 150), False, bolt_2, 2)

        elif weapon_id == "absolute_zero":
            # Ice blue
            pygame.draw.circle(surface, (180, 220, 255), center, 12)
            pygame.draw.circle(surface, (220, 240, 255), center, 8)
            pygame.draw.circle(surface, (255, 255, 255), center, 4)
            # Ice crystals
            for angle in [0, 90, 180, 270]:
                import math
                x = int(center[0] + 9 * math.cos(math.radians(angle)))
                y = int(center[1] + 9 * math.sin(math.radians(angle)))
                pygame.draw.line(surface, (200, 230, 255), (x-2, y), (x+2, y), 2)
                pygame.draw.line(surface, (200, 230, 255), (x, y-2), (x, y+2), 2)

        else:
            # Fallback: magenta placeholder
            pygame.draw.rect(surface, (255, 0, 255), (4, 4, size-8, size-8))
            pygame.draw.line(surface, (0, 0, 0), (4, 4), (size-4, size-4), 2)
            pygame.draw.line(surface, (0, 0, 0), (size-4, 4), (4, size-4), 2)

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

        # Pre-generate weapon icons (Sprint 28-29: ALL 18 weapons)
        weapon_ids = [
            # Sprint 28 originals
            'arcane_seeker', 'blood_whip', 'lightning_orb', 'toxic_cloud', 'holy_barrier',
            # Sprint 29: All remaining weapons
            'sword', 'magic_missile', 'lightning', 'holy_water', 'garlic',
            'shadow_scythe', 'frost_nova', 'blood_lance', 'soul_reaver', 'bone_storm',
            'cursed_tome', 'poison_dagger', 'void_lance', 'reapers_embrace', 'cosmic_annihilation',
            'sacred_ward', 'storm_bringer', 'absolute_zero'
        ]
        print(f"🎨 Generating {len(weapon_ids)} weapon icons...")
        for weapon_id in weapon_ids:
            icon = self.create_weapon_icon(weapon_id, 32)
            self.sprites[f'weapon_{weapon_id}'] = icon
        print(f"✅ Generated {len(weapon_ids)} weapon icons")

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
