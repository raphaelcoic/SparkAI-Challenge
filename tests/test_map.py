import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.append(str(ROOT / "code"))

MAP_DIR = ROOT / "examples"

from Map import AbstractMap, Map  # Les deux classes !

# Test ABSTRACT map (avec distances)
print("=== ABSTRACT MAP (visualisation distances) ===")
map_file = MAP_DIR / "small.txt"
abstract_map = AbstractMap.from_file(map_file)
dic = [['0', '0', 'v5', 'v11', 'v12', '0', '0'],
       ['0', 'v2', 'v6', 'v9', 'v13', 'v16', '0'],
       ['v1', 'v3', 'v7', 'v10', 'v14', 'v15', 'v19'],
       ['0', 'v4', 'v8', 'v20', 'v18', 'v17', '0']]



print("Abstract edges:", abstract_map.edges)
print("Abstract resources:", abstract_map.resources)
print("Bases:", abstract_map.base1, "-", abstract_map.base2)
abstract_map.visualize_grid(dic, "abstract_small.png")  # DISTANCES visibles !

# Test EXPANDED map (jeu unités)
print("\n=== EXPANDED MAP (jeu unités) ===")
game_map = Map.from_file(map_file)

print("Expanded edges:", len(game_map.edges))
print("Total cells:", len(game_map.resources))
print("Unit moves from base1:", game_map.neighbors(game_map.base1))
print("Resources base1:", game_map.resources[game_map.base1])

game_map.visualize("expanded_small.png")  # Grille étendue

# Test neighbors bidirectionnels
print("\n=== NEIGHBORS TEST ===")
test_pos = game_map.base1
print(f"From {test_pos}: {game_map.neighbors(test_pos)}")
