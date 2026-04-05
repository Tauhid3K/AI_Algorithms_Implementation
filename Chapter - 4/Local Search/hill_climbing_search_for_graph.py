def hill_climbing_search(graph, heuristic, start, goal):
    """Greedy hill climbing on a graph using heuristic values only."""
    # Initialize search at the given start node.
    current = start
    path = [current]
    total_cost = 0
    visited = {current}

    while current != goal:
        # Get outgoing neighbors from the current node.
        neighbors = graph.get(current, [])
        if not neighbors:
            # Dead end: goal cannot be reached from here.
            return path, total_cost, False

        # Support neighbors as either `node` or `(node, cost)`.
        parsed_neighbors = []
        for item in neighbors:
            if isinstance(item, tuple):
                neighbor, step_cost = item[0], item[1]
            else:
                neighbor, step_cost = item, 1
            if neighbor not in visited:
                parsed_neighbors.append((neighbor, step_cost))

        if not parsed_neighbors:
            # All candidates are already visited, so stop.
            return path, total_cost, False

        # Choose neighbor with lowest heuristic value.
        next_node, step_cost = min(
            parsed_neighbors,
            key=lambda n: heuristic.get(n[0], float("inf")),
        )

        # Stop if no heuristic improvement.
        if heuristic.get(next_node, float("inf")) >= heuristic.get(current, float("inf")):
            # Local optimum reached.
            return path, total_cost, False

        # Move to best local neighbor.
        current = next_node
        total_cost += step_cost
        path.append(current)
        visited.add(current)

    # Goal reached successfully.
    return path, total_cost, True


hill_climbing = hill_climbing_search


if __name__ == "__main__":
    # Romania road graph with edge costs.
    G = {
        "Arad": [("Zerind", 75), ("Sibiu", 140), ("Timisoara", 118)],
        "Zerind": [("Arad", 75), ("Oradea", 71)],
        "Oradea": [("Zerind", 71), ("Sibiu", 151)],
        "Sibiu": [("Arad", 140), ("Oradea", 151), ("Fagaras", 99), ("Rimnicu Vilcea", 80)],
        "Timisoara": [("Arad", 118), ("Lugoj", 111)],
        "Lugoj": [("Timisoara", 111), ("Mehadia", 70)],
        "Mehadia": [("Lugoj", 70), ("Drobeta", 75)],
        "Drobeta": [("Mehadia", 75), ("Craiova", 120)],
        "Craiova": [("Drobeta", 120), ("Rimnicu Vilcea", 146), ("Pitesti", 138)],
        "Rimnicu Vilcea": [("Sibiu", 80), ("Craiova", 146), ("Pitesti", 97)],
        "Fagaras": [("Sibiu", 99), ("Bucharest", 211)],
        "Pitesti": [("Rimnicu Vilcea", 97), ("Craiova", 138), ("Bucharest", 101)],
        "Bucharest": [("Fagaras", 211), ("Pitesti", 101), ("Giurgiu", 90), ("Urziceni", 85)],
        "Giurgiu": [("Bucharest", 90)],
        "Urziceni": [("Bucharest", 85), ("Hirsova", 98), ("Vaslui", 142)],
        "Hirsova": [("Urziceni", 98), ("Eforie", 86)],
        "Eforie": [("Hirsova", 86)],
        "Vaslui": [("Urziceni", 142), ("Iasi", 92)],
        "Iasi": [("Vaslui", 92), ("Neamt", 87)],
        "Neamt": [("Iasi", 87)],
    }

    # Straight-line-distance heuristic to Bucharest.
    H = {
        "Arad": 366,
        "Bucharest": 0,
        "Craiova": 160,
        "Drobeta": 242,
        "Eforie": 161,
        "Fagaras": 176,
        "Giurgiu": 77,
        "Hirsova": 151,
        "Iasi": 226,
        "Lugoj": 244,
        "Mehadia": 241,
        "Neamt": 234,
        "Oradea": 380,
        "Pitesti": 100,
        "Rimnicu Vilcea": 193,
        "Sibiu": 253,
        "Timisoara": 329,
        "Urziceni": 80,
        "Vaslui": 199,
        "Zerind": 374,
    }

    path, cost, found = hill_climbing_search(G, H, "Arad", "Bucharest")
    # Print final search result.
    print("Path :", " -> ".join(path))
    print("Cost :", cost)
    print("Goal Found :", found)
