from code.GameMap import Map
import inspect
import code.Units as Units
from pathlib import Path
from collections import defaultdict


class GameState:
    """Global state of the game."""

    def __init__(self, filename: Path):
        self.map = Map.from_file(filename)
        self.units = defaultdict(list)
        self.scores = {'p1': 0, 'p2': 0}
        self.spark_points = defaultdict(list)       #{p1: [unit1, unit2, ...], p2: [unit1, unit2, ...}
        self.unit_created = defaultdict(lambda: defaultdict(int))     #{p1: {minor: 1, transporter: 3, ...} p2: ...}
        self.unit_registry = self.scan_all_classes()

    def scan_all_classes(self):
        """Scan all classes in this module and return a registry of unit types."""

        registry = {}
        for name, obj in inspect.getmembers(Units, inspect.isclass):
            unit_type = name.lower()
            registry[unit_type] = obj
        return registry


    @property

    def add_score(self, player_id: str, score: int):
        '''Add the given score to the score of the given player.'''

        self.scores[player_id] = self.scores.get(player_id, 0) + score


    def update_death(self):
        '''Remove dead units from the game state.'''

        for unit in self.units:
            if not unit.is_alive:
                self.units.pop(unit)

    def new_unit(self, player_id : str, unit_type : str):
        '''Create a new unit of the given type for the given player.'''

        self.unit_created[player_id][unit_type] = self.unit_created.get(player_id, {}).get(unit_type, 0) + 1
        unit_id = f'{player_id}_{unit_type}_{self.unit_created[player_id][unit_type]}'
        UnitClass = self.unit_registry[unit_type]
        self.units[player_id].append(UnitClass(self, player_id, unit_id))