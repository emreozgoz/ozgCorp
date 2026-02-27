"""
DARK SANCTUM - Entity Component System
Matrix Team: System Architect + Technical Director

Clean ECS implementation for high performance and maintainability
"""

from typing import Dict, List, Set, Type, Any
import uuid


class Component:
    """Base class for all components"""
    pass


class Entity:
    """
    Entity in ECS architecture
    Just an ID with components attached
    """

    def __init__(self):
        self.id = str(uuid.uuid4())
        self.components: Dict[Type[Component], Component] = {}
        self.active = True

    def add_component(self, component: Component):
        """Add a component to this entity"""
        self.components[type(component)] = component
        return self

    def get_component(self, component_type: Type[Component]):
        """Get a component from this entity"""
        return self.components.get(component_type)

    def has_component(self, component_type: Type[Component]) -> bool:
        """Check if entity has a component"""
        return component_type in self.components

    def remove_component(self, component_type: Type[Component]):
        """Remove a component from this entity"""
        if component_type in self.components:
            del self.components[component_type]


class System:
    """
    Base class for all systems
    Systems process entities with specific components
    """

    def __init__(self, world: 'World'):
        self.world = world
        self.priority = 0  # Lower = runs first

    def update(self, dt: float):
        """
        Update system logic
        dt: Delta time in seconds
        """
        pass

    def get_entities(self, *component_types: Type[Component]) -> List[Entity]:
        """Get all entities that have ALL specified components"""
        return self.world.get_entities_with_components(*component_types)


class World:
    """
    World manages all entities and systems
    Main ECS coordinator
    """

    def __init__(self):
        self.entities: Dict[str, Entity] = {}
        self.systems: List[System] = []

    def create_entity(self) -> Entity:
        """Create a new entity"""
        entity = Entity()
        self.entities[entity.id] = entity
        return entity

    def destroy_entity(self, entity: Entity):
        """Remove an entity from the world"""
        if entity.id in self.entities:
            entity.active = False
            del self.entities[entity.id]

    def add_system(self, system: System):
        """Add a system to the world"""
        self.systems.append(system)
        # Sort by priority
        self.systems.sort(key=lambda s: s.priority)

    def update(self, dt: float):
        """Update all systems"""
        # Remove inactive entities
        to_remove = [eid for eid, e in self.entities.items() if not e.active]
        for eid in to_remove:
            del self.entities[eid]

        # Update all systems
        for system in self.systems:
            system.update(dt)

    def get_entities_with_components(self, *component_types: Type[Component]) -> List[Entity]:
        """Get all entities that have ALL specified components"""
        result = []
        for entity in self.entities.values():
            if entity.active and all(entity.has_component(ct) for ct in component_types):
                result.append(entity)
        return result

    def clear(self):
        """Clear all entities"""
        self.entities.clear()


# === TECHNICAL DIRECTOR NOTE ===
# This ECS implementation is:
# - Clean and simple
# - Type-safe with Python typing
# - O(n) entity queries (fast enough for our scale)
# - Easy to extend with new components/systems
# - No external dependencies
