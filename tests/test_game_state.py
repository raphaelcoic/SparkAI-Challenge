import sys
from pathlib import Path
from code.GameState import GameState


ROOT = Path(__file__).parent.parent
sys.path.append(str(ROOT / "code"))

MAP_DIR = ROOT / "examples"



map_file = MAP_DIR / "small.txt"


game_state = GameState(map_file)
game_state.new_unit('p1', 'minor')
game_state.new_unit('p1', 'commandant')
print(game_state.unit_created)
for unit in game_state.units['p1']:
    print(vars(unit))