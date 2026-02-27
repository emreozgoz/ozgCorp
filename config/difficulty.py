"""
DARK SANCTUM - Difficulty Settings
Matrix Team: Game Designer + Systems Architect

Three difficulty modes: Easy, Normal, Hard
"""

from enum import Enum


class Difficulty(Enum):
    """Difficulty levels"""
    EASY = "easy"
    NORMAL = "normal"
    HARD = "hard"


class DifficultySettings:
    """Difficulty-specific game parameters"""

    # Current difficulty
    current = Difficulty.NORMAL

    @classmethod
    def get_multipliers(cls):
        """Get current difficulty multipliers"""
        if cls.current == Difficulty.EASY:
            return {
                # Player buffs
                'player_health': 1.5,
                'player_damage': 1.3,
                'player_speed': 1.1,
                'xp_gain': 1.5,

                # Enemy nerfs
                'enemy_health': 0.7,
                'enemy_damage': 0.7,
                'enemy_speed': 0.85,
                'wave_scaling': 1.05,  # Slower difficulty ramp
                'spawn_interval': 12.0,  # Longer between waves

                # Rewards
                'powerup_drop_chance': 0.25,  # 25% drop rate
            }
        elif cls.current == Difficulty.NORMAL:
            return {
                # Balanced
                'player_health': 1.0,
                'player_damage': 1.0,
                'player_speed': 1.0,
                'xp_gain': 1.0,

                'enemy_health': 1.0,
                'enemy_damage': 1.0,
                'enemy_speed': 1.0,
                'wave_scaling': 1.15,
                'spawn_interval': 10.0,

                'powerup_drop_chance': 0.15,  # 15% drop rate
            }
        else:  # HARD
            return {
                # Player nerfs
                'player_health': 0.75,
                'player_damage': 0.85,
                'player_speed': 0.95,
                'xp_gain': 0.8,

                # Enemy buffs
                'enemy_health': 1.4,
                'enemy_damage': 1.3,
                'enemy_speed': 1.15,
                'wave_scaling': 1.25,  # Faster difficulty ramp
                'spawn_interval': 8.0,  # Faster waves

                # Rewards
                'powerup_drop_chance': 0.10,  # 10% drop rate
            }

    @classmethod
    def get_difficulty_name(cls):
        """Get current difficulty display name"""
        return cls.current.value.upper()

    @classmethod
    def set_difficulty(cls, difficulty: Difficulty):
        """Set difficulty level"""
        cls.current = difficulty
        print(f"🎮 Difficulty set to: {cls.get_difficulty_name()}")


# === GAME DESIGNER NOTE ===
# Difficulty settings balance challenge and accessibility:
# - EASY: Forgiving for new players, focus on learning mechanics
# - NORMAL: Balanced challenge, intended experience
# - HARD: Punishing for veterans, requires mastery
#
# All modes maintain core gameplay loop, just adjust numbers
