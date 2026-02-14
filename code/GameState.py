from GameMap import Map

class Game_State:
    """Global state of the game."""

    def __init__(self):
        self.map = None
        self.units = {}  # {player_id: [units]}
        self.scores = {}

    def load_map(self, filename: str):
        self.map = Map.from_file(filename)
        print(f"Game loaded")
