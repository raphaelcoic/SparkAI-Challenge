import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.append(str(ROOT / "code"))

MAP_DIR = ROOT / "examples"

from Map import AbstractMap, Map

# Test ABSTRACT map (avec distances)
print("=== ABSTRACT MAP (visualisation distances) ===")
map_file = MAP_DIR / "small.txt"
abstract_map = AbstractMap.from_file(map_file)

print("Abstract edges:", abstract_map.edges)
print("Abstract resources:", abstract_map.resources)
print("Bases:", abstract_map.base1, "-", abstract_map.base2)
abstract_map.visualize_grid()

# Test EXPANDED map (jeu unités)
print("\n=== EXPANDED MAP (jeu unités) ===")
game_map = Map.from_file(map_file)

print("Expanded edges:", len(game_map.edges))
print("Total resources:", len(game_map.resources))
print("Unit moves from base1:", game_map.neighbors(game_map.base1))
print("Resources base1:", game_map.resources[game_map.base1])

