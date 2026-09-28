"""
Graph Dijkstra Shortest Path Algorithm (DSA Topic)
Used in DevCollab Pro for dependency resolution and service pathway optimization.
"""
import heapq
from typing import Dict, List, Tuple, Any

class GraphDijkstra:
    def __init__(self):
        self.graph: Dict[str, List[Tuple[str, int]]] = {}

    def add_edge(self, u: str, v: str, weight: int):
        if u not in self.graph:
            self.graph[u] = []
        if v not in self.graph:
            self.graph[v] = []
        self.graph[u].append((v, weight))
        self.graph[v].append((u, weight))

    def shortest_path(self, start: str, target: str) -> Dict[str, Any]:
        distances = {node: float('inf') for node in self.graph}
        distances[start] = 0
        predecessors: Dict[str, Optional[str]] = {node: None for node in self.graph}
        pq = [(0, start)]

        while pq:
            curr_dist, curr_node = heapq.heappop(pq)
            if curr_dist > distances[curr_node]:
                continue
            if curr_node == target:
                break

            for neighbor, weight in self.graph.get(curr_node, []):
                distance = curr_dist + weight
                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    predecessors[neighbor] = curr_node
                    heapq.heappush(pq, (distance, neighbor))

        # Reconstruct path
        path = []
        curr = target
        while curr is not None:
            path.append(curr)
            curr = predecessors.get(curr)
        path.reverse()

        return {
            "start": start,
            "target": target,
            "distance": distances.get(target, float('inf')),
            "path": path if path and path[0] == start else []
        }
