"""
DARK SANCTUM - Animation System
Matrix Team: UI/UX Designer + Technical Director

Sprint 21: Animation controller for sprite-based visuals
"""

from src.core.ecs import System
from src.components.components import AnimationComponent


class AnimationSystem(System):
    """Update sprite animations"""

    def __init__(self, world):
        super().__init__(world)
        self.priority = 15  # Before rendering

    def update(self, dt: float):
        """Update all animations"""
        animated_entities = self.get_entities(AnimationComponent)

        for entity in animated_entities:
            anim = entity.get_component(AnimationComponent)

            if not anim.playing:
                continue

            # Update frame timer
            anim.time_since_frame += dt

            if anim.time_since_frame >= anim.frame_duration:
                anim.time_since_frame = 0.0

                # Advance frame
                if anim.current_animation in anim.animations:
                    frames = anim.animations[anim.current_animation]
                    if frames:
                        anim.current_frame += 1

                        if anim.current_frame >= len(frames):
                            if anim.loop:
                                anim.current_frame = 0
                            else:
                                anim.current_frame = len(frames) - 1
                                anim.playing = False


# === TECHNICAL DIRECTOR NOTE ===
# Sprint 21: Simple frame-based animation system
# Ready for sprite sheet integration in Sprint 22
