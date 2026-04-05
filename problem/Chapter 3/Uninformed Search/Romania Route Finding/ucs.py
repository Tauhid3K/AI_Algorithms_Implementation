"""Romania Route Finding - UCS starter implementation."""
import heapq


def uniform_cost_search(graph, start, goal):
    pq = [(0, start, [start])]
    best_cost = {start: 0}

    while pq:
        cost, node, path = heapq.heappop(pq)
        if node == goal:
            return cost, path
        if cost > best_cost.get(node, float("inf")):
            continue
        for neighbor, step_cost in graph.get(node, []):
            new_cost = cost + step_cost
            if new_cost < best_cost.get(neighbor, float("inf")):
                best_cost[neighbor] = new_cost
                heapq.heappush(pq, (new_cost, neighbor, path + [neighbor]))

    return float("inf"), []


if __name__ == "__main__":
    graph = {"A": [("B", 1), ("C", 4)], "B": [("D", 2)], "C": [("D", 1)], "D": []}
    cost, path = uniform_cost_search(graph, "A", "D")
    print("Cost:", cost, "Path:", path)
