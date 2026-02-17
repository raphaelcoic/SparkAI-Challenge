from GameMap import Map

class GameState:
    """Global state of the game."""

    def __init__(self):
        self.map = None
        self.units = {}
        self.scores = {}


    def load_map(self, filename: str):
        self.map = Map.from_file(filename)
        print(f"Game loaded")


    def add_score(self, player_id: str, score: int):
        self.scores[player_id] = self.scores.get(player_id, 0) + score


    def update_death(self):
        for unit in self.units:
            if unit.health <= 0:
                self.units.pop(unit.id)