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

# Q - Shadow Dash (Mobility/Defense)
ABILITY_Q_COOLDOWN = 8.0              # Seconds
ABILITY_Q_DASH_DISTANCE = 150         # Pixels
ABILITY_Q_INVULN_TIME = 0.3           # Invulnerability duration

# W - Blood Nova (AoE Damage)
ABILITY_W_COOLDOWN = 10.0             # Seconds
ABILITY_W_DAMAGE = 150                # Damage
ABILITY_W_RADIUS = 100                # Pixels
ABILITY_W_KNOCKBACK = 200             # Knockback force

# E - Arcane Missiles (Burst Damage)
ABILITY_E_COOLDOWN = 6.0              # Seconds
ABILITY_E_DAMAGE = 30                 # Damage per missile
ABILITY_E_SPEED = 300                 # Missile speed
ABILITY_E_MISSILES = 3                # Number of missiles

# R - Time Freeze (Ultimate)
ABILITY_R_COOLDOWN = 30.0             # Seconds
ABILITY_R_SLOW_PERCENT = 0.7          # 70% slow
ABILITY_R_DURATION = 3.0              # Seconds

# === PERFORMANCE SETTINGS ===
MAX_ENTITIES = 500                   # Maximum entities at once
MAX_PROJECTILES = 200                # Maximum projectiles
CULLING_DISTANCE = 1000              # Don't render beyond this

# === BOSS SETTINGS ===
BOSS_WAVE_INTERVAL = 5               # Boss every N waves
BOSS_HEALTH_MULTIPLIER = 10          # 10x normal health
BOSS_DAMAGE_MULTIPLIER = 2           # 2x damage
BOSS_SPEED_MULTIPLIER = 0.6          # Slower, more menacing
BOSS_SIZE_MULTIPLIER = 2.0           # Twice as large
BOSS_XP_MULTIPLIER = 10              # 10x XP reward
BOSS_COLOR = (120, 10, 10)           # Dark crimson
BOSS_GLOW_COLOR = (180, 20, 20)      # Blood red glow

# === ENEMY TYPES (Game Designer) ===
# 1. FAST ENEMY (Imp) - Fast, low health, swarms player
FAST_ENEMY_COLOR = (200, 100, 50)    # Orange
FAST_ENEMY_SPEED_MULT = 1.5          # 50% faster
FAST_ENEMY_HEALTH_MULT = 0.6         # 40% less health
FAST_ENEMY_DAMAGE_MULT = 0.8         # 20% less damage
FAST_ENEMY_SIZE_MULT = 0.7           # Smaller
FAST_ENEMY_XP_MULT = 0.8             # Less XP

# 2. TANK ENEMY (Golem) - Slow, high health, blocks path
TANK_ENEMY_COLOR = (80, 80, 120)     # Grey-blue
TANK_ENEMY_SPEED_MULT = 0.5          # 50% slower
TANK_ENEMY_HEALTH_MULT = 3.0         # 3x health
TANK_ENEMY_DAMAGE_MULT = 1.5         # 50% more damage
TANK_ENEMY_SIZE_MULT = 1.5           # Larger
TANK_ENEMY_XP_MULT = 2.0             # Double XP

# 3. RANGED ENEMY (Wraith) - Stays back, shoots projectiles
RANGED_ENEMY_COLOR = (120, 50, 150)  # Purple
RANGED_ENEMY_SPEED_MULT = 0.7        # 30% slower
RANGED_ENEMY_HEALTH_MULT = 0.8       # 20% less health
RANGED_ENEMY_DAMAGE_MULT = 1.2       # 20% more damage
RANGED_ENEMY_SIZE_MULT = 0.9         # Slightly smaller
RANGED_ENEMY_XP_MULT = 1.5           # 50% more XP
RANGED_ENEMY_ATTACK_RANGE = 300      # Shoot from distance
RANGED_ENEMY_ATTACK_COOLDOWN = 2.0   # Attack every 2 seconds
RANGED_ENEMY_KEEP_DISTANCE = 250     # Stay away from player

# === POWER-UPS ===
POWERUP_DROP_CHANCE = 0.15           # 15% chance to drop on enemy death
POWERUP_LIFETIME = 10.0              # Seconds before disappearing
POWERUP_HEALTH_VALUE = 25            # HP restored
POWERUP_DAMAGE_BOOST_VALUE = 5       # Damage increase
POWERUP_DAMAGE_BOOST_DURATION = 10.0 # Seconds
POWERUP_XP_VALUE = 50                # XP gained

# Power-up colors
POWERUP_HEALTH_COLOR = (50, 255, 100)      # Green
POWERUP_DAMAGE_COLOR = (255, 150, 50)      # Orange
POWERUP_XP_COLOR = (255, 215, 0)           # Gold

# === GAME BALANCE (Game Designer) ===
DIFFICULTY_SCALING = 1.1             # Enemy stats multiply per minute

# === DEBUG ===
DEBUG_MODE = True
SHOW_FPS = True
SHOW_HITBOXES = False
GOD_MODE = False
