from GameMap import Map

class GameState:
    """Global state of the game."""

    def __init__(self):
        self.map = None
        self.units = {}     #{id_player: unit}
        self.scores = {}

    def load_map(self, filename: str):
        self.map = Map.from_file(filename)
        print(f"Game loaded")


