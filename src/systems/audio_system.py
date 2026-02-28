"""
DARK SANCTUM - Audio System
Matrix Team: Audio Director + Developer

Simple but impactful sound effect system
"""

import pygame
from src.core.ecs import System
from src.components.components import *
from typing import Dict, Optional


class AudioSystem(System):
    """Manages game audio and sound effects"""

    def __init__(self, world):
        super().__init__(world)
        self.priority = 70  # After death/effects but before render

        # Initialize pygame mixer
        pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)

        # Volume settings (0.0 to 1.0)
        self.master_volume = 0.7
        self.sfx_volume = 0.8
        self.music_volume = 0.5
        self.enabled = True  # Master enable/disable

        # Sound channels
        self.music_channel = None
        self.sfx_channels = []

        # Sound effects cache
        self.sounds: Dict[str, pygame.mixer.Sound] = {}

        # Generate procedural sounds
        self._generate_sounds()

        print("🔊 Audio System initialized")

    def set_master_volume(self, volume: float):
        """Set master volume (0.0 to 1.0)"""
        self.master_volume = max(0.0, min(1.0, volume))

    def set_sfx_volume(self, volume: float):
        """Set SFX volume (0.0 to 1.0)"""
        self.sfx_volume = max(0.0, min(1.0, volume))

    def set_music_volume(self, volume: float):
        """Set music volume (0.0 to 1.0)"""
        self.music_volume = max(0.0, min(1.0, volume))

    def toggle_audio(self):
        """Toggle audio on/off"""
        self.enabled = not self.enabled

    def _generate_sounds(self):
        """Generate simple procedural sound effects"""
        # We'll use pygame's built-in sound generation for simplicity
        # In a full game, these would be loaded from audio files

        try:
            # Player hit (short beep)
            self.sounds['player_hit'] = self._generate_tone(440, 0.1, 0.3)

            # Enemy death (descending tone)
            self.sounds['enemy_death'] = self._generate_tone(330, 0.15, 0.4)

            # Ability cast (ascending chirp)
            self.sounds['ability_cast'] = self._generate_tone(523, 0.12, 0.5)

            # Boss spawn (deep rumble)
            self.sounds['boss_spawn'] = self._generate_tone(110, 0.3, 0.6)

            # Level up (triumphant)
            self.sounds['level_up'] = self._generate_tone(659, 0.2, 0.7)

            # Projectile fire (quick blip)
            self.sounds['projectile_fire'] = self._generate_tone(880, 0.05, 0.2)

            print(f"✅ Generated {len(self.sounds)} sound effects")

        except Exception as e:
            print(f"⚠️  Warning: Could not generate sounds: {e}")
            # Disable audio if it fails
            self.sounds = {}

    def _generate_tone(self, frequency: float, duration: float, volume: float) -> Optional[pygame.mixer.Sound]:
        """Generate a simple sine wave tone"""
        try:
            import numpy as np

            sample_rate = 22050
            num_samples = int(duration * sample_rate)

            # Generate sine wave
            t = np.linspace(0, duration, num_samples, False)
            wave = np.sin(frequency * 2 * np.pi * t)

            # Apply envelope (fade out)
            envelope = np.linspace(1.0, 0.0, num_samples)
            wave = wave * envelope * volume

            # Convert to 16-bit integers
            wave = (wave * 32767).astype(np.int16)

            # Create stereo sound
            stereo_wave = np.zeros((num_samples, 2), dtype=np.int16)
            stereo_wave[:, 0] = wave
            stereo_wave[:, 1] = wave

            # Create pygame Sound object
            sound = pygame.sndarray.make_sound(stereo_wave)
            return sound

        except Exception as e:
            print(f"⚠️  Could not generate tone at {frequency}Hz: {e}")
            return None

    def update(self, dt: float):
        """Process audio events"""
        from src.components.components import AudioEvent

        # Find and process all audio events
        audio_entities = self.get_entities(AudioEvent)

        for entity in audio_entities:
            event = entity.get_component(AudioEvent)

            if not event.processed:
                # Play the sound
                if event.event_type == 'player_hit':
                    self.play_player_hit()
                elif event.event_type == 'enemy_death':
                    self.play_enemy_death()
                elif event.event_type == 'ability_cast':
                    self.play_ability_cast()
                elif event.event_type == 'boss_spawn':
                    self.play_boss_spawn()
                elif event.event_type == 'level_up':
                    self.play_level_up()
                elif event.event_type == 'projectile_fire':
                    self.play_projectile_fire()

                event.processed = True

            # Destroy event entity after processing
            self.world.destroy_entity(entity)

    def play_sound(self, sound_name: str, volume: float = 1.0):
        """Play a sound effect with volume control"""
        if not self.enabled:
            return

        if sound_name not in self.sounds:
            return

        sound = self.sounds[sound_name]
        if sound:
            # Apply master and SFX volume
            final_volume = volume * self.sfx_volume * self.master_volume
            sound.set_volume(final_volume)
            sound.play()

    def play_player_hit(self):
        """Play player hit sound"""
        self.play_sound('player_hit', 0.4)

    def play_enemy_death(self):
        """Play enemy death sound"""
        self.play_sound('enemy_death', 0.3)

    def play_ability_cast(self):
        """Play ability cast sound"""
        self.play_sound('ability_cast', 0.5)

    def play_boss_spawn(self):
        """Play boss spawn sound"""
        self.play_sound('boss_spawn', 0.7)

    def play_level_up(self):
        """Play level up sound"""
        self.play_sound('level_up', 0.6)

    def play_projectile_fire(self):
        """Play projectile fire sound"""
        self.play_sound('projectile_fire', 0.2)


# === AUDIO DIRECTOR NOTE ===
# Simple procedural sound generation keeps the game lightweight
# No external audio files needed - all sounds generated at runtime
# Volume levels carefully balanced to not be annoying
# Future: Add music track, spatial audio, more complex sound effects
