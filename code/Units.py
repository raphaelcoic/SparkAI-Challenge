from __future__ import annotations
from GameMap import *
from code.GameState import GameState


class Unit:
    """Abstract class for a unit."""

    def __init__(self, game_state : GameState, player_id: str, unit_id : str):
        self.game_state = game_state
        self.map = game_state.map
        self.player_id = player_id
        self.id = unit_id
        self.type = None
        self.position = self.map.base1 if player_id == 'p1' else self.map.base2
        self.speed = None
        self.health = None
        
        
    def move(self, v):
        """Moves the unit to v if it is adjacent to it."""

        assert self.map.distance(self.position, v) <= self.speed, "Impossible move"
        self.position = v


class Worker(Unit):
    """Class for a worker unit."""

    def __init__(self, game_state : GameState, player_id : str, unit_id : str):
        super().__init__(game_state, player_id, unit_id)
        self.health = 5
        self.speed = 1
        self.extraction_speed = 1
        self.load = 0
        self.capacity = 3
        self.type = "worker"


    @property
    def available_space(self):

        """Returns the number of resources available to extract."""
        return self.capacity - self.load


    def extract(self):
        """Extracts resources from the map."""

        assert self.load < self.capacity and self.map.resources(self.position) != 0, "Impossible extraction"
        available_resources = self.map.resources[self.position]
        extracted_resources = min(available_resources, self.available_space, self.extraction_speed)

        self.load += extracted_resources
        self.map.resources[self.position] -= extracted_resources


    def drop(self):
        """Drops resources on the base."""

        assert (self.position == self.map.base1 and self.player_id == 'p1') or (
                    self.position == self.map.base2 and self.player_id == 'p2'), "Drop location not allowed"
        self.map.resources[self.position] += self.load
        self.load = 0


    def give_to(self, target: Worker):
        """Gives resources to another worker."""

        assert target.type == "worker", "Target not a worker"
        assert target.position == self.position, "Target out of range"
        assert self.load > 0, "No resources to give"
        assert target.available_space > 0, "Target full"

        transferred_resources = min(self.load, target.available_space)
        self.load -= transferred_resources
        target.load += transferred_resources


class Fighter(Unit):
    """Class for a fighter unit."""

    def __init__(self, game_state, player_id, unit_id):
        super().__init__(game_state, player_id, unit_id)
        self.type = "fighter"
        self.health = 10
        self.speed = 1
        self.damage = 1
        self.range = 1


    def attack(self, target: Unit):
        """Attacks the target unit."""
        assert self.map.distance(self.position, target.position) <= self.range, "Target out of range"
        target.health -= self.damage
        if target.health <= 0:
            self.game_state.remove_unit(target.id)
