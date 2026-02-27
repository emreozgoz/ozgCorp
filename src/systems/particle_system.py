"""
DARK SANCTUM - Particle System
Matrix Team: Creative Director + Developer

Simple particle effects for game juice
"""

import random
import math
from src.core.ecs import System
from src.components.components import *
from config.settings import *


class ParticleComponent(Component):
    """Particle with lifetime and fade"""

    def __init__(self, lifetime: float, velocity_x: float = 0, velocity_y: float = 0):
        self.lifetime = lifetime
        self.max_lifetime = lifetime
        self.vx = velocity_x
        self.vy = velocity_y

    def update(self, dt: float) -> bool:
        """Return True if expired"""
        self.lifetime -= dt
        return self.lifetime <= 0

    @property
    def alpha(self) -> float:
        """Fade out over lifetime"""
        return self.lifetime / self.max_lifetime


class ParticleSystem(System):
    """Update and clean up particles"""

    def __init__(self, world):
        super().__init__(world)
        self.priority = 66  # After lifetime system

    def update(self, dt: float):
        """Update all particles"""
        particles = self.get_entities(ParticleComponent, Position, Velocity)

        for particle in particles:
            particle_comp = particle.get_component(ParticleComponent)

            # Update lifetime
            if particle_comp.update(dt):
                self.world.destroy_entity(particle)
                continue

            # Apply gravity/velocity damping
            vel = particle.get_component(Velocity)
            vel.vx *= 0.98  # Damping
            vel.vy *= 0.98


def create_hit_particles(world, x: float, y: float, color: tuple, count: int = 8):
    """Create particle burst on hit"""
    for i in range(count):
        angle = random.uniform(0, 2 * math.pi)
        speed = random.uniform(50, 150)

        particle = world.create_entity()
        particle.add_component(Position(x, y))
        particle.add_component(Velocity(
            math.cos(angle) * speed,
            math.sin(angle) * speed
        ))
        particle.add_component(Size(4, 4))
        particle.add_component(Sprite(color, radius=2))
        particle.add_component(ParticleComponent(
            lifetime=random.uniform(0.3, 0.6)
        ))
        particle.add_component(Tag("particle"))


def create_death_particles(world, x: float, y: float, color: tuple, count: int = 20):
    """Create particle explosion on death"""
    for i in range(count):
        angle = random.uniform(0, 2 * math.pi)
        speed = random.uniform(100, 250)

        particle = world.create_entity()
        particle.add_component(Position(x, y))
        particle.add_component(Velocity(
            math.cos(angle) * speed,
            math.sin(angle) * speed
        ))
        particle.add_component(Size(6, 6))
        particle.add_component(Sprite(color, radius=3))
        particle.add_component(ParticleComponent(
            lifetime=random.uniform(0.5, 1.0)
        ))
        particle.add_component(Tag("particle"))


def create_level_up_particles(world, x: float, y: float, count: int = 30):
    """Create golden particle burst on level up"""
    for i in range(count):
        angle = random.uniform(0, 2 * math.pi)
        speed = random.uniform(150, 300)

        particle = world.create_entity()
        particle.add_component(Position(x, y))
        particle.add_component(Velocity(
            math.cos(angle) * speed,
            math.sin(angle) * speed
        ))
        particle.add_component(Size(8, 8))
        particle.add_component(Sprite(COLOR_GOLD, radius=4))
        particle.add_component(ParticleComponent(
            lifetime=random.uniform(0.8, 1.5)
        ))
        particle.add_component(Tag("particle"))


def create_ability_particles(world, x: float, y: float, color: tuple, count: int = 20, spread: float = 50):
    """Create particle burst for ability effects"""
    for i in range(count):
        angle = random.uniform(0, 2 * math.pi)
        speed = random.uniform(50, spread * 3)

        particle = world.create_entity()
        particle.add_component(Position(x, y))
        particle.add_component(Velocity(
            math.cos(angle) * speed,
            math.sin(angle) * speed
        ))
        particle.add_component(Size(5, 5))
        particle.add_component(Sprite(color, radius=2.5))
        particle.add_component(ParticleComponent(
            lifetime=random.uniform(0.4, 0.8)
        ))
        particle.add_component(Tag("particle"))


# === CREATIVE DIRECTOR NOTE ===
# Particle effects add "game juice":
# - Visual feedback for hits
# - Death explosions feel satisfying
# - Level up celebrations
# - All using simple circles and velocity
