"""Romania Route Finding - A* starter implementation."""
import heapq


def a_star(graph, start, goal, heuristic):
    open_heap = [(heuristic(start), 0, start, [start])]
    best_g = {start: 0}

    while open_heap:
        _, g, node, path = heapq.heappop(open_heap)
        if node == goal:
            return g, path
        if g > best_g.get(node, float("inf")):
            continue
        for neighbor, cost in graph.get(node, []):
            ng = g + cost
            if ng < best_g.get(neighbor, float("inf")):
                best_g[neighbor] = ng
                f = ng + heuristic(neighbor)
                heapq.heappush(open_heap, (f, ng, neighbor, path + [neighbor]))

    return float("inf"), []


if __name__ == "__main__":
    graph = {"A": [("B", 1), ("C", 4)], "B": [("D", 2)], "C": [("D", 1)], "D": []}
    h = {"A": 3, "B": 2, "C": 1, "D": 0}
    cost, path = a_star(graph, "A", "D", lambda n: h[n])
    print("Cost:", cost, "Path:", path)
