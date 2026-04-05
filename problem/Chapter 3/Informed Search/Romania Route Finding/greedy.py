"""Romania Route Finding - Greedy best-first starter implementation."""
import heapq


def greedy_best_first(graph, start, goal, heuristic):
    heap = [(heuristic(start), start, [start])]
    visited = set()

    while heap:
        _, node, path = heapq.heappop(heap)
        if node in visited:
            continue
        visited.add(node)
        if node == goal:
            return path
        for neighbor, _ in graph.get(node, []):
            if neighbor not in visited:
                heapq.heappush(heap, (heuristic(neighbor), neighbor, path + [neighbor]))

    return []


if __name__ == "__main__":
    graph = {"A": [("B", 1), ("C", 4)], "B": [("D", 2)], "C": [("D", 1)], "D": []}
    h = {"A": 3, "B": 2, "C": 1, "D": 0}
    print("Path:", greedy_best_first(graph, "A", "D", lambda n: h[n]))
