import numpy as np


class map:
    """
    Class for a map that represents the environment.
    """

    def __init__(self, roads={}, resources={}, base1=None, base2=None):
        """
        Initializes the network from a dictionary roads.

        Parameters:
        -----------
        roads: dict
            A dictionary of the roads as an adjacency list
            roads[u] = list of v
            Ex: roads = {v0: [v1, v2],
                        v1: [v0, v2],
                        ...}
        ressources: dict
            A dictionary of resources available at each vertex
            ressources[v] = quantity of resources at vertex v
            Ex: ressources = {'v1': 5, 'v2': 3, ...}
        base1: str
            The vertex identifier for player 1's base
        base2: str
            The vertex identifier for player 2's base
        """

        self.roads = roads
        self.resources = resources
        self.base1 = base1
        self.base2 = base2

    @classmethod
    def from_file(cls, filename: str):
        """
        Creates a Map from a text file.

        File format:
        Line 1: nb_road nb_edges base1 base2
        Lines 2+: road (start end distance) 
        Then: ressources (vertex quantity) one per line
        """
        roads = {}
        resources = {}

        with open(filename, "r", encoding="utf-8") as f:
            # Header line
            nb_routes, nb_vertices, base1, base2 = f.readline().strip().split()

            # Read roads
            for _ in range(int(nb_routes)):
                start, end, dist = f.readline().strip().split()
                dist = int(dist)
                if dist==1:
                    roads.setdefault(start, []).append(end)
                else:
                    for i in range(1, dist+1):
                        if i==1:
                            roads.setdefault(start, []).append(start + '-' + end + ',' + str(i))
                        elif i==dist:
                            roads.setdefault(start + '-' + end + ',' + str(i-1), []).append(end)
                        else:
                            roads.setdefault(start + '-' + end + ',' + str(i-1), []).append(start + '-' + end + ',' + str(i))

            # Read resources (rest of file)
            for vertex in roads:
                resources[vertex] = 0
            for line in f:
                if line.strip():  # Skip empty lines
                    vertex, quantity = line.strip().split()
                    resources[vertex] = int(quantity)


        return cls(roads=roads, resources=resources, base1=base1, base2=base2)

    def visualize_map(self, filename="map.png"):
        """Visualise ta Map avec NetworkX"""
        import networkx as nx
        import matplotlib.pyplot as plt

        # Créer un graphe dirigé
        G = nx.DiGraph()

        # Ajouter les arêtes et les noeuds
        for start, neighbors in self.roads.items():
            res_start = self.resources.get(start, 0)
            for end in neighbors:
                res_end = self.resources.get(end, 0)
                G.add_edge(start, end)
            G.add_node(start, size=max(500, res_start * 1000))

        # Calculer les distances depuis les bases
        dist_from_base1 = nx.shortest_path_length(G, self.base1)
        dist_from_base2 = nx.shortest_path_length(G, self.base2)

        # Créer les positions manuellement
        pos = {}
        max_depth = max(max(dist_from_base1.values()), max(dist_from_base2.values()))

        # Positionner les bases
        pos[self.base1] = np.array([-2.0, 0])
        pos[self.base2] = np.array([2.0, 0])

        # Organiser les autres nœuds en couches
        for node in G.nodes():
            if node not in [self.base1, self.base2]:
                # Calculer la position x basée sur la distance moyenne aux bases
                d1 = dist_from_base1.get(node, max_depth)
                d2 = dist_from_base2.get(node, max_depth)

                # Position x relative aux bases
                rel_pos = (d1 - d2) / (d1 + d2)
                x = rel_pos * 2.0

                # Position y avec un léger décalage aléatoire pour éviter les superpositions
                y = np.random.uniform(-0.5, 0.5) * (1 - abs(rel_pos))

                pos[node] = np.array([x, y])

        # Créer la figure
        plt.figure(figsize=(15, 10))

        # Dessiner les nœuds
        node_sizes = [G.nodes[n]['size'] for n in G.nodes]
        colors = ['red' if n == self.base1 else 'blue' if n == self.base2 else 'lightgreen' for n in G.nodes]
        nx.draw_networkx_nodes(G, pos,
                               node_color=colors,
                               node_size=node_sizes)

        # Dessiner les arêtes avec des flèches
        nx.draw_networkx_edges(G, pos, edge_color='gray',
                               arrows=True, arrowsize=20,
                               connectionstyle='arc3,rad=0.2')

        # Ajouter les labels des nœuds avec les ressources
        labels = {node: f"{node}\n(r:{self.resources[node]})" for node in G.nodes()}
        nx.draw_networkx_labels(G, pos, labels, font_size=8)
    
        # Ajouter un titre
        plt.title(f"Map: {len(self.roads)} vertices, {sum(self.resources.values())} resources")
    
        # Sauvegarder et afficher
        plt.savefig(filename, bbox_inches='tight', dpi=300)
        plt.show()
