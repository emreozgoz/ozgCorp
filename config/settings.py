"""
DARK SANCTUM - Game Configuration
Matrix Team: Game Designer + Technical Director

Gothic action-roguelike settings optimized for 60 FPS
"""

# === WINDOW SETTINGS ===
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
WINDOW_TITLE = "DARK SANCTUM - Survive. Evolve. Dominate."
FPS = 60

# === COLORS (Gothic Theme) ===
COLOR_BACKGROUND = (15, 10, 25)      # Deep purple-black
COLOR_BLOOD_RED = (180, 20, 20)      # Health
COLOR_ARCANE_BLUE = (80, 120, 255)   # Abilities/Mana
COLOR_DARK_PURPLE = (60, 20, 80)     # UI elements
COLOR_SHADOW = (10, 5, 15)           # Shadows
COLOR_GOLD = (255, 215, 0)           # XP/Rewards
COLOR_WHITE = (255, 255, 255)        # Text
COLOR_GREEN = (50, 200, 50)          # Positive effects

# === PLAYER SETTINGS ===
PLAYER_SPEED = 250                   # Pixels per second
PLAYER_SIZE = 32                     # Square hitbox
PLAYER_MAX_HEALTH = 100
PLAYER_BASE_DAMAGE = 5               # Melee contact damage
PLAYER_HEALTH_REGEN = 0.5            # HP per second
PLAYER_COLOR = (150, 100, 200)       # Violet (placeholder)

# === AUTO-ATTACK SETTINGS ===
AUTO_ATTACK_DAMAGE = 10
AUTO_ATTACK_RANGE = 200              # Pixels
AUTO_ATTACK_COOLDOWN = 0.5           # Seconds
AUTO_ATTACK_SPEED = 400               # Projectile speed (pixels/sec)
AUTO_ATTACK_COLOR = (200, 200, 255)  # Light blue

# === ENEMY SETTINGS ===
ENEMY_BASE_HEALTH = 20
ENEMY_BASE_DAMAGE = 5
ENEMY_BASE_SPEED = 80                # Slower than player
ENEMY_SIZE = 28
ENEMY_COLOR = (180, 50, 50)          # Dark red
ENEMY_XP_VALUE = 10

# === WAVE SPAWNING ===
WAVE_SPAWN_INTERVAL = 10.0           # Seconds between waves
WAVE_INITIAL_ENEMIES = 5
WAVE_SCALING = 1.2                   # Multiply enemies by this each wave
SPAWN_DISTANCE_MIN = 400             # Minimum spawn distance from player
SPAWN_DISTANCE_MAX = 600             # Maximum spawn distance from player

# === EXPERIENCE & LEVELING ===
XP_BASE_REQUIREMENT = 100
XP_LEVEL_SCALING = 1.5               # Multiply XP needed per level
MAX_LEVEL = 50

# === ABILITIES (4 Slots: Q, W, E, R) ===
ABILITY_COOLDOWNS = {
    'Q': 5.0,   # Quick damage ability
    'W': 8.0,   # Area damage
    'E': 10.0,  # Utility/defensive
    'R': 15.0   # Ultimate
}

# === PERFORMANCE SETTINGS ===
MAX_ENTITIES = 500                   # Maximum entities at once
MAX_PROJECTILES = 200                # Maximum projectiles
CULLING_DISTANCE = 1000              # Don't render beyond this

# === GAME BALANCE (Game Designer) ===
DIFFICULTY_SCALING = 1.1             # Enemy stats multiply per minute
BOSS_WAVE_INTERVAL = 5               # Boss every N waves
BOSS_HEALTH_MULTIPLIER = 10
BOSS_DAMAGE_MULTIPLIER = 2

# === DEBUG ===
DEBUG_MODE = True
SHOW_FPS = True
SHOW_HITBOXES = False
GOD_MODE = False
