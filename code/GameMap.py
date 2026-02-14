class AbstractMap:
    """
    ABSTRACT map with original distances (for visualization).
    NOT expanded - shows real distances between vertices.
    """

    def __init__(self, edges: set[tuple[str, str, int]], resources: dict[str, int], base1: str, base2: str):
        self.edges = edges  # (u, v, distance)
        self.resources = resources
        self.base1 = base1
        self.base2 = base2
        self.grid_matrix = []
        self.is_expanded = False

    def visualize_grid(self, filename: str = "grid_map.png", dpi: int = 200):
        """
        Visualize AbstractMap using GRID MATRIX with ULTRA-HIGH RESOLUTION.
        """
        try:
            import networkx as nx
            import matplotlib.pyplot as plt
            import numpy as np

            G = nx.Graph()
            edge_labels = {}

            # Add edges with distances
            for u, v, dist in self.edges:
                G.add_edge(u, v, weight=dist)
                edge_labels[(u, v)] = str(dist)

            # Parse grid → positions fixes
            rows, cols = len(self.grid_matrix), len(self.grid_matrix[0])
            pos = {}
            resources_pos = {}

            for i in range(rows):
                for j in range(cols):
                    vertex = self.grid_matrix[i][j]
                    if vertex != '0':
                        x = j / (cols - 1)
                        y = 1 - i / (rows - 1)
                        pos[vertex] = (x, y)
                        resources_pos[vertex] = (x, y - 0.05)

            # FIGURES HAUTE Résolution
            fig = plt.figure(figsize=(20, 16), dpi=dpi)  # Gros + haute densité

            # 1. NŒUDS NORMAUX
            normal_nodes = [n for n in G.nodes() if n not in [self.base1, self.base2]]
            nx.draw_networkx_nodes(G, pos, nodelist=normal_nodes,
                                   node_color='lightblue', node_size=2000, alpha=0.9)

            # 2. BASE1 ROUGE ÉNORME
            if self.base1 in pos:
                nx.draw_networkx_nodes(G, pos, nodelist=[self.base1],
                                       node_color='red', node_size=3500, alpha=1.0)

            # 3. BASE2 BLEU ÉNORME
            if self.base2 in pos:
                nx.draw_networkx_nodes(G, pos, nodelist=[self.base2],
                                       node_color='darkblue', node_size=3500, alpha=1.0)

            # 4. ARÊTES ULTRA-ÉPAISSES
            nx.draw_networkx_edges(G, pos, edge_color='darkblue',
                                   width=6, alpha=0.9, arrows=False)

            # 5. LABELS SOMMETS GROS
            nx.draw_networkx_labels(G, pos, font_size=18, font_weight='bold')

            # 6. DISTANCES SUR ARÊTES
            nx.draw_networkx_edge_labels(G, pos, edge_labels,
                                         font_size=16, font_weight='bold')

            # 7. RESSOURCES VERTES
            resource_labels = {v: str(self.resources.get(v, 0))
                               for v in resources_pos}
            nx.draw_networkx_labels(G, resources_pos, labels=resource_labels,
                                    font_size=14, font_color='darkgreen',
                                    font_weight='bold')

            # Légende
            plt.text(0.02, 0.98, f"Base1: {self.base1} | Base2: {self.base2}",
                     transform=plt.gca().transAxes, fontsize=18,
                     bbox=dict(boxstyle="round,pad=0.4", facecolor="yellow", alpha=0.8))
            plt.text(0.02, 0.93, f"Total resources: {sum(self.resources.values())}",
                     transform=plt.gca().transAxes, fontsize=16, fontweight='bold')

            plt.title(f"Game Map Grid {rows}x{cols} - High Resolution", fontsize=24, fontweight='bold')
            plt.axis('off')
            plt.tight_layout()

            # SAUVEGARDE ULTRA-HD
            plt.savefig(filename, dpi=dpi, bbox_inches='tight',
                        pad_inches=0.2, facecolor='white')
            plt.show()
            print(f"ULTRA-HD map saved: {filename} ({dpi} DPI)")

        except ImportError:
            print("Install: pip install networkx matplotlib numpy")

    @classmethod
    def from_file(cls, filename: str):
        """Load ABSTRACT map (no expansion)."""
        temp_edges = set()
        temp_resources = {}
        grid_matrix = []

        with open(filename, "r", encoding="utf-8") as f:
            header = f.readline().strip().split()
            nb_roads, nb_vertices, base1, base2 = header

            for _ in range(int(nb_roads)):
                u, v, dist = f.readline().strip().split()
                dist = int(dist)

                norm_u, norm_v = min(u, v), max(u, v)
                edge_exists = False

                for existing_u, existing_v, existing_dist in temp_edges:
                    if min(existing_u, existing_v) == norm_u and max(existing_u, existing_v) == norm_v:
                        print(f"Warning: duplicate edge {norm_u}-{norm_v}")
                        edge_exists = True
                        break

                if not edge_exists:
                    temp_edges.add((norm_u, norm_v, dist))

            for line in f:
                if line.strip():
                    parts = line.strip().split()
                    if len(parts) <= 2:
                        vertex, quantity = parts
                        temp_resources[vertex] = int(quantity)
                    else:
                        grid_matrix.append(parts)
        instance = cls(temp_edges, temp_resources, base1, base2)
        instance.grid_matrix = grid_matrix
        return instance

class Map(AbstractMap):
    """
    EXPANDED map for unit movement (distance=1 everywhere).
    Inherits visualization from AbstractMap.
    """

    def __init__(self, edges: set[tuple[str, str]], resources: dict[str, int], base1: str, base2: str):
        super().__init__(set(), {}, base1, base2)
        self.edges = edges  # (u, v) distance=1
        self.resources = resources
        self.is_expanded = True
        self.abstract_map = None  # Cache pour visualisation


    def neighbors(self, vertex: str) -> list[str]:
        """Unit neighbors (distance=1)."""
        outgoing = [v for (u, v) in self.edges if u == vertex]
        incoming = [u for (u, v) in self.edges if v == vertex]
        return list(set(outgoing + incoming))
    
    def distance(self, u: str, v: str) -> int:
        """Distance between two vertices using BFS since all edges have weight 1."""
        import math
        from collections import deque

        visited = set()
        queue = deque([(u, 0)])  # (vertex, distance)
        visited.add(u)

        while queue:
            vertex, dist = queue.popleft()

            if vertex == v:
                return dist

            for neighbor in self.neighbors(vertex):
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, dist + 1))

        return math.inf  # No path found

    @classmethod
    def from_file(cls, filename: str):
        """Load → EXPAND → unit-ready map."""
        # Charge abstract D'ABORD
        abstract = AbstractMap.from_file(filename)

        # EXPAND
        final_edges = set()
        final_resources = abstract.resources.copy()

        for u, v, dist in abstract.edges:
            current = u
            for step in range(1, dist):
                inter_cell = f"{u}_{v}_{step}"
                final_resources[inter_cell] = 0
                final_edges.add((current, inter_cell))
                current = inter_cell
            final_edges.add((current, v))

        return cls(final_edges, final_resources, abstract.base1, abstract.base2)
