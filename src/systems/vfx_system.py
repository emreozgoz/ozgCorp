"""
DARK SANCTUM - Enhanced VFX System
Matrix Team: Creative Director + Technical Director + UI/UX Designer

Sprint 23: Advanced visual effects for weapons and abilities
"""

import pygame
import math
import random
from src.core.ecs import System
from src.components.components import *
from config.settings import *


class VFXSystem(System):
    """Enhanced visual effects system"""

    def __init__(self, world):
        super().__init__(world)
        self.priority = 67  # After particle system

    def update(self, dt: float):
        """Update all VFX components"""
        # Update trails
        trail_entities = self.get_entities(TrailEffect, Position)
        for entity in trail_entities:
            trail = entity.get_component(TrailEffect)
            pos = entity.get_component(Position)

            # Add current position to trail
            trail.add_position(pos.x, pos.y)
            trail.update(dt)

        # Update glows
        glow_entities = self.get_entities(GlowEffect)
        for entity in glow_entities:
            glow = entity.get_component(GlowEffect)
            glow.update(dt)

        # Update impact effects
        impact_entities = self.get_entities(ImpactEffect)
        for entity in impact_entities:
            impact = entity.get_component(ImpactEffect)
            if impact.update(dt):
                self.world.destroy_entity(entity)

        # Update screen distortions
        distortion_entities = self.get_entities(ScreenDistortion)
        for entity in distortion_entities:
            distortion = entity.get_component(ScreenDistortion)
            if distortion.update(dt):
                self.world.destroy_entity(entity)


class VFXRenderer(System):
    """Render visual effects"""

    def __init__(self, world, screen: pygame.Surface):
        super().__init__(world)
        self.priority = 98  # Just before main render
        self.screen = screen

    def update(self, dt: float):
        """Render all VFX"""
        # Render trails
        self._render_trails()

        # Render glows
        self._render_glows()

        # Render impact effects
        self._render_impacts()

    def _render_trails(self):
        """Render trail effects"""
        trail_entities = self.get_entities(TrailEffect, Position)

        for entity in trail_entities:
            trail = entity.get_component(TrailEffect)

            # Draw trail segments
            for i, (x, y, alpha) in enumerate(trail.positions):
                if alpha <= 0:
                    continue

                # Size decreases along trail
                size = max(1, int((i + 1) / len(trail.positions) * 4))

                # Create surface with alpha
                color_with_alpha = (*trail.color, int(alpha))

                # Draw circle for each trail segment
                pygame.draw.circle(
                    self.screen,
                    trail.color,
                    (int(x), int(y)),
                    size
                )

    def _render_glows(self):
        """Render glow effects"""
        glow_entities = self.get_entities(GlowEffect, Position, Size)

        for entity in glow_entities:
            glow = entity.get_component(GlowEffect)
            pos = entity.get_component(Position)
            size = entity.get_component(Size)

            intensity = glow.get_current_intensity()

            # Draw multiple circles for glow effect
            for i in range(3):
                radius = int(size.width / 2 + i * 5 * intensity)
                alpha = int(100 * intensity * (1.0 - i / 3.0))

                # Create glow surface
                glow_surface = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
                pygame.draw.circle(
                    glow_surface,
                    (*glow.color, alpha),
                    (radius, radius),
                    radius
                )

                # Blit to screen
                self.screen.blit(
                    glow_surface,
                    (int(pos.x - radius), int(pos.y - radius)),
                    special_flags=pygame.BLEND_ADD
                )

    def _render_impacts(self):
        """Render impact effects"""
        impact_entities = self.get_entities(ImpactEffect, Position)

        for entity in impact_entities:
            impact = entity.get_component(ImpactEffect)
            pos = entity.get_component(Position)

            # Different rendering based on effect type
            if impact.effect_type == "spark":
                self._render_spark_impact(pos, impact)
            elif impact.effect_type == "explosion":
                self._render_explosion_impact(pos, impact)
            elif impact.effect_type == "slash":
                self._render_slash_impact(pos, impact)

    def _render_spark_impact(self, pos: Position, impact: ImpactEffect):
        """Render spark-style impact"""
        alpha = int(255 * (1.0 - impact.elapsed / impact.duration))
        size = int(10 * impact.scale)

        # Draw star-burst
        for i in range(8):
            angle = i * (2 * math.pi / 8)
            end_x = pos.x + math.cos(angle) * size
            end_y = pos.y + math.sin(angle) * size

            pygame.draw.line(
                self.screen,
                (255, 255, 200),
                (int(pos.x), int(pos.y)),
                (int(end_x), int(end_y)),
                2
            )

    def _render_explosion_impact(self, pos: Position, impact: ImpactEffect):
        """Render explosion-style impact"""
        alpha = int(255 * (1.0 - impact.elapsed / impact.duration))
        radius = int(15 * impact.scale)

        # Draw expanding circle
        pygame.draw.circle(
            self.screen,
            (255, 100, 50),
            (int(pos.x), int(pos.y)),
            radius,
            3
        )

    def _render_slash_impact(self, pos: Position, impact: ImpactEffect):
        """Render slash-style impact"""
        alpha = int(255 * (1.0 - impact.elapsed / impact.duration))
        length = int(20 * impact.scale)

        # Draw slash line
        angle = random.uniform(0, 2 * math.pi)
        end_x = pos.x + math.cos(angle) * length
        end_y = pos.y + math.sin(angle) * length

        pygame.draw.line(
            self.screen,
            (200, 200, 255),
            (int(pos.x), int(pos.y)),
            (int(end_x), int(end_y)),
            4
        )


# === VFX HELPER FUNCTIONS ===

def create_weapon_trail(world, x: float, y: float, color: tuple, length: int = 10):
    """Create a trail effect entity"""
    trail_entity = world.create_entity()
    trail_entity.add_component(Position(x, y))
    trail_entity.add_component(TrailEffect(color, length, fade_speed=0.5))
    trail_entity.add_component(Tag("vfx_trail"))
    return trail_entity


def create_glow_effect(world, x: float, y: float, size: float, color: tuple, intensity: float = 1.0):
    """Create a glow effect entity"""
    glow_entity = world.create_entity()
    glow_entity.add_component(Position(x, y))
    glow_entity.add_component(Size(size, size))
    glow_entity.add_component(GlowEffect(color, intensity, pulse_speed=3.0))
    glow_entity.add_component(Tag("vfx_glow"))
    return glow_entity


def create_impact_effect(world, x: float, y: float, effect_type: str = "spark"):
    """Create an impact effect"""
    impact_entity = world.create_entity()
    impact_entity.add_component(Position(x, y))
    impact_entity.add_component(ImpactEffect(effect_type, duration=0.3))
    impact_entity.add_component(Tag("vfx_impact"))
    return impact_entity


def create_enhanced_particles(world, x: float, y: float, color: tuple, count: int = 15,
                              particle_type: str = "burst", speed_mult: float = 1.0):
    """Create enhanced particle effects"""
    for i in range(count):
        if particle_type == "burst":
            # Radial burst
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(100, 300) * speed_mult
        elif particle_type == "fountain":
            # Upward fountain
            angle = random.uniform(-math.pi * 0.3, -math.pi * 0.7)
            speed = random.uniform(150, 350) * speed_mult
        elif particle_type == "trail":
            # Directional trail
            angle = random.uniform(-0.2, 0.2)
            speed = random.uniform(50, 150) * speed_mult
        else:
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(100, 200) * speed_mult

        particle = world.create_entity()
        particle.add_component(Position(x, y))
        particle.add_component(Velocity(
            math.cos(angle) * speed,
            math.sin(angle) * speed
        ))
        particle.add_component(Size(random.randint(3, 7), random.randint(3, 7)))
        particle.add_component(Sprite(color, radius=random.uniform(2, 4)))

        # Enhanced particle component
        from src.systems.particle_system import ParticleComponent
        particle.add_component(ParticleComponent(
            lifetime=random.uniform(0.4, 1.2)
        ))
        particle.add_component(Tag("particle"))


# === CREATIVE DIRECTOR NOTE ===
# Sprint 23: Enhanced VFX System
# - Trail effects for projectiles and weapons
# - Pulsing glow effects for power-ups and abilities
# - Impact effects for satisfying hit feedback
# - Enhanced particle system with different emission types
# - All effects designed to improve game juice without tanking performance


