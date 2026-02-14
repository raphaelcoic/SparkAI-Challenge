import sys
from pathlib import Path
ROOT = Path(__file__).parent.parent
sys.path.append(str(ROOT / "code"))

NET_DIR = ROOT / "examples"

from Map import map

map_file = "../examples/small.txt"
M = map.from_file(map_file)
print(M.roads)
print(M.resources)
map.visualize_map(M)