"""
DARK SANCTUM - Statistics & Persistence System
Matrix Team: Data Analyst + Developer

Track player statistics and high scores across sessions
"""

import json
import os
from datetime import datetime
from src.core.ecs import System, Component
from src.components.components import *
from config.settings import *


class GameStats(Component):
    """Session statistics tracking"""
    def __init__(self):
        # Current session stats
        self.kills = 0
        self.damage_dealt = 0
        self.damage_taken = 0
        self.power_ups_collected = 0
        self.abilities_cast = 0
        self.bosses_killed = 0
        self.highest_wave = 0
        self.session_start_time = datetime.now()
        self.survival_time = 0.0
        # Sprint 19: New stat tracking
        self.weapons_evolved = 0
        self.no_damage_streak = 0.0  # Time without taking damage
        self.last_damage_time = 0.0

    def get_survival_time_str(self) -> str:
        """Format survival time as MM:SS"""
        minutes = int(self.survival_time // 60)
        seconds = int(self.survival_time % 60)
        return f"{minutes:02d}:{seconds:02d}"


class PersistentStats:
    """Persistent statistics saved to disk"""
    STATS_FILE = "dark_sanctum_stats.json"

    def __init__(self):
        self.data = {
            "total_games_played": 0,
            "total_kills": 0,
            "total_damage_dealt": 0,
            "total_damage_taken": 0,
            "total_power_ups": 0,
            "total_abilities_cast": 0,
            "total_bosses_killed": 0,
            "total_playtime_seconds": 0,
            "highest_level": 1,
            "highest_wave": 0,
            "longest_survival_time": 0.0,
            "high_scores": [],  # List of {name, score, date, wave, level}
            "achievements_unlocked": [],
            "first_played": None,
            "last_played": None
        }
        self.load()

    def load(self):
        """Load stats from disk"""
        if os.path.exists(self.STATS_FILE):
            try:
                with open(self.STATS_FILE, 'r') as f:
                    loaded_data = json.load(f)
                    self.data.update(loaded_data)
            except Exception as e:
                print(f"⚠️ Could not load stats: {e}")

    def save(self):
        """Save stats to disk"""
        try:
            with open(self.STATS_FILE, 'w') as f:
                json.dump(self.data, f, indent=2)
        except Exception as e:
            print(f"⚠️ Could not save stats: {e}")

    def update_session_end(self, game_stats: GameStats, player_level: int):
        """Update persistent stats at end of game session"""
        now = datetime.now().isoformat()

        if self.data["first_played"] is None:
            self.data["first_played"] = now
        self.data["last_played"] = now

        self.data["total_games_played"] += 1
        self.data["total_kills"] += game_stats.kills
        self.data["total_damage_dealt"] += game_stats.damage_dealt
        self.data["total_damage_taken"] += game_stats.damage_taken
        self.data["total_power_ups"] += game_stats.power_ups_collected
        self.data["total_abilities_cast"] += game_stats.abilities_cast
        self.data["total_bosses_killed"] += game_stats.bosses_killed
        self.data["total_playtime_seconds"] += game_stats.survival_time

        self.data["highest_level"] = max(self.data["highest_level"], player_level)
        self.data["highest_wave"] = max(self.data["highest_wave"], game_stats.highest_wave)
        self.data["longest_survival_time"] = max(
            self.data["longest_survival_time"],
            game_stats.survival_time
        )

        self.save()

    def add_high_score(self, character_name: str, score: int, wave: int, level: int):
        """Add a high score entry"""
        entry = {
            "character": character_name,
            "score": score,
            "wave": wave,
            "level": level,
            "date": datetime.now().isoformat()
        }

        self.data["high_scores"].append(entry)
        # Sort by score descending
        self.data["high_scores"].sort(key=lambda x: x["score"], reverse=True)
        # Keep top 10
        self.data["high_scores"] = self.data["high_scores"][:10]

        self.save()

    def is_high_score(self, score: int) -> bool:
        """Check if score qualifies for top 10"""
        if len(self.data["high_scores"]) < 10:
            return True
        return score > self.data["high_scores"][-1]["score"]

    def unlock_achievement(self, achievement_id: str):
        """Unlock an achievement"""
        if achievement_id not in self.data["achievements_unlocked"]:
            self.data["achievements_unlocked"].append(achievement_id)
            self.save()
            return True
        return False


class StatsTrackingSystem(System):
    """Track statistics during gameplay"""

    def __init__(self, world):
        super().__init__(world)
        self.priority = 65
        self.persistent_stats = PersistentStats()

    def update(self, dt: float):
        """Update session stats"""
        # Find player with stats
        player_entities = self.get_entities(Player, GameStats)
        if not player_entities:
            return

        player = player_entities[0]
        stats = player.get_component(GameStats)

        # Update survival time
        stats.survival_time += dt

        # Update no-damage streak (Sprint 19)
        if stats.survival_time - stats.last_damage_time > stats.no_damage_streak:
            stats.no_damage_streak = stats.survival_time - stats.last_damage_time


class AchievementSystem(System):
    """Check for and unlock achievements"""

    ACHIEVEMENTS = {
        "first_blood": {
            "name": "First Blood",
            "description": "Kill your first enemy",
            "check": lambda stats: stats.kills >= 1
        },
        "slayer": {
            "name": "Slayer",
            "description": "Kill 100 enemies in one session",
            "check": lambda stats: stats.kills >= 100
        },
        "massacre": {
            "name": "Massacre",
            "description": "Kill 500 enemies in one session",
            "check": lambda stats: stats.kills >= 500
        },
        "survivor": {
            "name": "Survivor",
            "description": "Survive for 5 minutes",
            "check": lambda stats: stats.survival_time >= 300
        },
        "endurance": {
            "name": "Endurance",
            "description": "Survive for 15 minutes",
            "check": lambda stats: stats.survival_time >= 900
        },
        "boss_slayer": {
            "name": "Boss Slayer",
            "description": "Defeat your first boss",
            "check": lambda stats: stats.bosses_killed >= 1
        },
        "titan_killer": {
            "name": "Titan Killer",
            "description": "Defeat 10 bosses in one session",
            "check": lambda stats: stats.bosses_killed >= 10
        },
        "ability_master": {
            "name": "Ability Master",
            "description": "Cast 200 abilities",
            "check": lambda stats: stats.abilities_cast >= 200
        },
        "power_collector": {
            "name": "Power Collector",
            "description": "Collect 50 power-ups",
            "check": lambda stats: stats.power_ups_collected >= 50
        },
        "wave_warrior": {
            "name": "Wave Warrior",
            "description": "Reach wave 20",
            "check": lambda stats: stats.highest_wave >= 20
        },
        # Sprint 19: New Achievements
        "legend": {
            "name": "Legend",
            "description": "Reach wave 30",
            "check": lambda stats: stats.highest_wave >= 30
        },
        "god_slayer": {
            "name": "God Slayer",
            "description": "Defeat 25 bosses",
            "check": lambda stats: stats.bosses_killed >= 25
        },
        "unstoppable": {
            "name": "Unstoppable",
            "description": "Survive 30 minutes",
            "check": lambda stats: stats.survival_time >= 1800
        },
        "arsenal_master": {
            "name": "Arsenal Master",
            "description": "Evolve a weapon",
            "check": lambda stats: hasattr(stats, 'weapons_evolved') and stats.weapons_evolved >= 1
        },
        "damage_dealer": {
            "name": "Damage Dealer",
            "description": "Deal 50,000 damage",
            "check": lambda stats: stats.damage_dealt >= 50000
        },
        "tank": {
            "name": "Tank",
            "description": "Take 10,000 damage and survive",
            "check": lambda stats: stats.damage_taken >= 10000
        },
        "perfectionist": {
            "name": "Perfectionist",
            "description": "Complete a run without taking damage for 5 minutes",
            "check": lambda stats: hasattr(stats, 'no_damage_streak') and stats.no_damage_streak >= 300
        }
    }

    def __init__(self, world, persistent_stats: PersistentStats):
        super().__init__(world)
        self.priority = 66
        self.persistent_stats = persistent_stats
        self.checked_achievements = set()

    def update(self, dt: float):
        """Check for achievement unlocks"""
        player_entities = self.get_entities(Player, GameStats)
        if not player_entities:
            return

        stats = player_entities[0].get_component(GameStats)

        for achievement_id, achievement in self.ACHIEVEMENTS.items():
            # Skip already checked
            if achievement_id in self.checked_achievements:
                continue

            # Check condition
            if achievement["check"](stats):
                # Unlock achievement
                if self.persistent_stats.unlock_achievement(achievement_id):
                    print(f"🏆 ACHIEVEMENT UNLOCKED: {achievement['name']}")
                    print(f"   {achievement['description']}")

                    # Achievement unlock sound
                    audio_event = self.world.create_entity()
                    audio_event.add_component(AudioEvent('level_up'))  # Reuse level up sound

                self.checked_achievements.add(achievement_id)


# Helper function to calculate score
def calculate_score(stats: GameStats, player_level: int) -> int:
    """Calculate final score based on performance"""
    score = 0
    score += stats.kills * 10
    score += stats.bosses_killed * 100
    score += player_level * 50
    score += stats.highest_wave * 20
    score += int(stats.survival_time) * 2
    score += stats.power_ups_collected * 5
    score += stats.abilities_cast * 1
    return score


# === DATA ANALYST NOTE ===
# Statistics system provides:
# - Session tracking for immediate feedback
# - Persistent stats for long-term progression
# - High score leaderboard (top 10)
# - Achievement system for goals
# - Score calculation rewards all playstyles
