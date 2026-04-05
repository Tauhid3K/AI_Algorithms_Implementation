def recursive_best_first_search(graph, heuristic, start, goal):
	def rbfs(node, g_cost, path, f_limit, visited):
		if node == goal:
			return g_cost, path, g_cost

		# Generate successors while avoiding cycles in current recursion path.
		successors = []
		for neighbor, step_cost in graph.get(node, []):
			if neighbor in visited:
				continue
			new_g = g_cost + step_cost
			f_cost = new_g + heuristic.get(neighbor, float("inf"))
			successors.append([f_cost, new_g, neighbor, path + [neighbor]])

		if not successors:
			return float("inf"), [], float("inf")

		while True:
			# Always explore the lowest-f successor first.
			successors.sort(key=lambda item: item[0])
			best = successors[0]

			if best[0] > f_limit:
				return float("inf"), [], best[0]

			alternative = successors[1][0] if len(successors) > 1 else float("inf")
			# Recurse with a tighter limit based on best alternative path.
			visited.add(best[2])
			result_cost, result_path, best_new_f = rbfs(
				best[2],
				best[1],
				best[3],
				min(f_limit, alternative),
				visited,
			)
			visited.discard(best[2])
			best[0] = best_new_f

			if result_path:
				return result_cost, result_path, best_new_f

	cost, path, _ = rbfs(start, 0, [start], float("inf"), {start})
	return cost, path


if __name__ == "__main__":
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

	cost, path = recursive_best_first_search(G, H, "Arad", "Bucharest")
	print("Path :", " -> ".join(path) if path else "No path found")
	print("Cost :", cost)
