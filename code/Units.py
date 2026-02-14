from GameMap import *

class Worker:
    """Class for a worker unit."""
    def __init__(self, player = None, position = None):
        self.player = player
        self.position = position
        self.health = 5
        self.speed = 1
        self.extraction_speed = 1
        self.load = 0
        self.capacity = 3
        self.map = None

    def set_map(self, gamemap):
        self.map = gamemap

    def move(self, v):
        """Moves the worker to v if it is adjacent to it."""
        if v in self.map.neighbors(self.position):
            self.position = v
        else:
            print("Impossible move")

    def extract(self):
        """Extracts resources from the map."""
        if self.load < self.capacity and self.map.resources(self.position) != 0:
            available_resources = self.map.resources[self.position]
            available_space = self.capacity - self.load
            extracted_resources = min(available_resources, available_space, self.extraction_speed)

            self.load += extracted_resources
            self.map.resources[self.position] -= extracted_resources

        else:
            print("Impossible extraction")

    def drop(self):
            self.map.resources[self.position] += self.load
            self.load = 0
