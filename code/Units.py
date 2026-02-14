from GameMap import *

class Unit:
    """Abstract class for a unit."""

    def __init__(self, player_id=None, position=None):
        self.player_id = player_id
        self.position = position
        self.speed = 1
        self.id = None
        self.game_state = None

    def link_game_state(self, game_state):
        self.game_state = game_state

    def move(self, v):
        """Moves the unit to v if it is adjacent to it."""
        assert self.game_state.map.distance(self.position, v) <= self.speed, "Impossible move"
        self.position = v


class Worker(Unit):
    """Class for a worker unit."""

    def __init__(self, position=None, player_id=None):
        super().__init__(position, player_id)
        self.health = 5
        self.speed = 1
        self.extraction_speed = 1
        self.load = 0
        self.capacity = 3

    def extract(self):
        """Extracts resources from the map."""
        assert self.load < self.capacity and self.game_state.map.resources(self.position) != 0, "Impossible extraction"
        available_resources = self.game_state.map.resources[self.position]
        available_space = self.capacity - self.load
        extracted_resources = min(available_resources, available_space, self.extraction_speed)

        self.load += extracted_resources
        self.map.resources[self.position] -= extracted_resources

    def drop(self):
        self.map.resources[self.position] += self.load
        self.load = 0


class Fighter(Unit):
    """Class for a fighter unit."""

    def __init__(self, player_id=None, position=None):
        super().__init__(player_id, position)
        self.health = 10
        self.speed = 1
        self.damage = 1

    def attack(self, target: str):
        """Attacks the target unit."""
        assert target in self.game_state.units[self.player_id], "Target not found"
        assert self.position == self.game_state.units[self.player_id][target].position, "Target out of range"
        self.game_state.units[self.player_id][target].health -= self.damage
