"""
DARK SANCTUM - Background & Environment System
Matrix Team: Creative Director + UI/UX Designer

Sprint 25: Parallax backgrounds and environmental atmosphere
"""

import pygame
import random
import math
from src.core.ecs import System
from config.settings import WINDOW_WIDTH, WINDOW_HEIGHT
from config.ui_theme import *


class BackgroundLayer:
    """Single parallax background layer"""

    def __init__(self, color: tuple, scroll_speed: float, pattern: str = "stars"):
        self.color = color
        self.scroll_speed = scroll_speed  # 0.0 to 1.0 (1.0 = follows camera exactly)
        self.pattern = pattern  # "stars", "fog", "solid"
        self.offset_x = 0.0
        self.offset_y = 0.0

        # Generate pattern elements
        self.elements = []
        if pattern == "stars":
            # Generate random stars
            for _ in range(50):
                x = random.uniform(0, WINDOW_WIDTH)
                y = random.uniform(0, WINDOW_HEIGHT)
                size = random.randint(1, 3)
                brightness = random.randint(150, 255)
                self.elements.append({
                    'x': x, 'y': y, 'size': size,
                    'brightness': brightness,
                    'twinkle_speed': random.uniform(0.5, 2.0),
                    'twinkle_offset': random.uniform(0, math.pi * 2)
                })
        elif pattern == "fog":
            # Generate fog patches
            for _ in range(10):
                x = random.uniform(-100, WINDOW_WIDTH + 100)
                y = random.uniform(-100, WINDOW_HEIGHT + 100)
                radius = random.randint(80, 200)
                alpha = random.randint(10, 40)
                drift_speed = random.uniform(5, 15)
                drift_direction = random.uniform(0, math.pi * 2)
                self.elements.append({
                    'x': x, 'y': y, 'radius': radius,
                    'alpha': alpha,
                    'drift_speed': drift_speed,
                    'drift_dir': drift_direction
                })

    def update(self, dt: float, camera_offset: tuple):
        """Update layer position based on camera"""
        # Apply parallax scrolling
        self.offset_x = camera_offset[0] * self.scroll_speed
        self.offset_y = camera_offset[1] * self.scroll_speed

        # Update animated elements
        if self.pattern == "fog":
            for elem in self.elements:
                # Drift fog patches
                elem['x'] += math.cos(elem['drift_dir']) * elem['drift_speed'] * dt
                elem['y'] += math.sin(elem['drift_dir']) * elem['drift_speed'] * dt

                # Wrap around screen
                if elem['x'] < -elem['radius']:
                    elem['x'] = WINDOW_WIDTH + elem['radius']
                elif elem['x'] > WINDOW_WIDTH + elem['radius']:
                    elem['x'] = -elem['radius']
                if elem['y'] < -elem['radius']:
                    elem['y'] = WINDOW_HEIGHT + elem['radius']
                elif elem['y'] > WINDOW_HEIGHT + elem['radius']:
                    elem['y'] = -elem['radius']

    def render(self, surface: pygame.Surface, time: float):
        """Render background layer"""
        if self.pattern == "solid":
            # Simple solid color fill
            surface.fill(self.color)

        elif self.pattern == "stars":
            # Render twinkling stars
            for star in self.elements:
                # Calculate twinkle effect
                twinkle = math.sin(time * star['twinkle_speed'] + star['twinkle_offset'])
                brightness = int(star['brightness'] * (0.7 + 0.3 * twinkle))
                color = (brightness, brightness, brightness)

                # Apply parallax offset and wrap
                x = (star['x'] + self.offset_x) % WINDOW_WIDTH
                y = (star['y'] + self.offset_y) % WINDOW_HEIGHT

                pygame.draw.circle(surface, color, (int(x), int(y)), star['size'])

        elif self.pattern == "fog":
            # Render fog patches
            for fog in self.elements:
                # Create fog surface with alpha
                fog_surf = pygame.Surface((fog['radius'] * 2, fog['radius'] * 2), pygame.SRCALPHA)

                # Draw radial gradient fog
                for i in range(fog['radius'], 0, -5):
                    alpha = int(fog['alpha'] * (1.0 - i / fog['radius']))
                    pygame.draw.circle(
                        fog_surf,
                        (*self.color, alpha),
                        (fog['radius'], fog['radius']),
                        i
                    )

                # Apply parallax offset
                x = fog['x'] + self.offset_x
                y = fog['y'] + self.offset_y

                surface.blit(fog_surf, (int(x - fog['radius']), int(y - fog['radius'])))


class BackgroundSystem(System):
    """Manage parallax background layers"""

    def __init__(self, world, screen: pygame.Surface):
        super().__init__(world)
        self.priority = 1  # Render first (before everything)
        self.screen = screen
        self.time = 0.0

        # Create background layers (back to front)
        self.layers = [
            # Far background - solid dark
            BackgroundLayer(GOTHIC_BLACK, 0.0, "solid"),

            # Deep space stars
            BackgroundLayer((100, 95, 110), 0.1, "stars"),

            # Distant fog layer
            BackgroundLayer((75, 45, 95), 0.3, "fog"),

            # Close fog layer
            BackgroundLayer((50, 30, 60), 0.6, "fog"),
        ]

    def update(self, dt: float):
        """Update and render background layers"""
        self.time += dt

        # Get camera offset (assuming camera follows player)
        camera_offset = (0, 0)  # TODO: Get from camera system if implemented

        # Update all layers
        for layer in self.layers:
            layer.update(dt, camera_offset)

        # Render layers back to front (Sprint 25: Background renders in update)
        for layer in self.layers:
            layer.render(self.screen, self.time)


class EnvironmentalParticles(System):
    """Ambient environmental particle effects"""

    def __init__(self, world, screen: pygame.Surface):
        super().__init__(world)
        self.priority = 2  # After background, before game entities
        self.screen = screen
        self.particles = []
        self.spawn_timer = 0.0

    def update(self, dt: float):
        """Update and render environmental particles"""
        # Spawn new particles periodically
        self.spawn_timer += dt
        if self.spawn_timer >= 0.1:  # Spawn every 100ms
            self.spawn_timer = 0.0
            self._spawn_particle()

        # Update existing particles
        for particle in self.particles[:]:
            particle['lifetime'] -= dt
            particle['y'] += particle['vy'] * dt
            particle['x'] += particle['vx'] * dt
            particle['alpha'] = int(255 * (particle['lifetime'] / particle['max_lifetime']))

            # Remove dead particles
            if particle['lifetime'] <= 0:
                self.particles.remove(particle)

        # Render particles (Sprint 25: Render in update for proper layering)
        self._render_particles()

    def _spawn_particle(self):
        """Spawn a floating particle (ash, embers, mist)"""
        particle_type = random.choice(["ash", "ember", "mist"])

        if particle_type == "ash":
            # Gray ash floating down
            self.particles.append({
                'x': random.uniform(0, WINDOW_WIDTH),
                'y': -10,
                'vx': random.uniform(-10, 10),
                'vy': random.uniform(20, 40),
                'size': random.randint(2, 4),
                'color': GOTHIC_MIST,
                'lifetime': random.uniform(8, 15),
                'max_lifetime': random.uniform(8, 15),
                'alpha': 255,
                'type': 'ash'
            })
        elif particle_type == "ember":
            # Glowing embers floating up
            self.particles.append({
                'x': random.uniform(0, WINDOW_WIDTH),
                'y': WINDOW_HEIGHT + 10,
                'vx': random.uniform(-5, 5),
                'vy': random.uniform(-50, -30),
                'size': random.randint(2, 3),
                'color': GLOW_CRIMSON,
                'lifetime': random.uniform(3, 6),
                'max_lifetime': random.uniform(3, 6),
                'alpha': 255,
                'type': 'ember'
            })
        else:  # mist
            # Drifting purple mist
            self.particles.append({
                'x': random.uniform(0, WINDOW_WIDTH),
                'y': random.uniform(0, WINDOW_HEIGHT),
                'vx': random.uniform(-20, 20),
                'vy': random.uniform(-10, 10),
                'size': random.randint(8, 16),
                'color': GOTHIC_PURPLE,
                'lifetime': random.uniform(5, 10),
                'max_lifetime': random.uniform(5, 10),
                'alpha': 50,
                'type': 'mist'
            })

    def _render_particles(self):
        """Render environmental particles"""
        for particle in self.particles:
            if particle['type'] == 'mist':
                # Draw mist as soft circle
                mist_surf = pygame.Surface((particle['size'] * 2, particle['size'] * 2), pygame.SRCALPHA)
                pygame.draw.circle(
                    mist_surf,
                    (*particle['color'], particle['alpha'] // 3),
                    (particle['size'], particle['size']),
                    particle['size']
                )
                self.screen.blit(mist_surf, (int(particle['x']), int(particle['y'])))
            else:
                # Draw ash/embers as small circles
                color_with_alpha = (*particle['color'], particle['alpha'])
                pygame.draw.circle(
                    self.screen,
                    particle['color'],
                    (int(particle['x']), int(particle['y'])),
                    particle['size']
                )


# === CREATIVE DIRECTOR NOTE ===
# Sprint 25: Environment & Final Polish
# - Parallax scrolling background for depth
# - Multiple atmospheric layers (stars, fog)
# - Environmental particles (ash, embers, mist)
# - Gothic atmosphere maintained throughout
# - Performance-optimized particle system
# - Final visual polish for v3.0 release
