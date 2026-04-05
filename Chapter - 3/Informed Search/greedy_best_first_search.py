from heapq import heappop, heappush

# h(n) = heuristic estimate 

def greedy_best_first_search(graph, start, goal, heuristic):
	# (heuristic_value, path_cost, node, path)
	frontier = [(heuristic(start, goal), 0, start, [start])]
	# Closed set to avoid expanding the same node again.
	visited = set()

	while frontier:
		# Always expand the node with the smallest heuristic value.
		_, cost, node, path = heappop(frontier)
		#_ is the heuristic value, which we don't need after popping.
		if node in visited:
			continue

		visited.add(node)
		if node == goal:
			# Stop as soon as goal is selected for expansion.
			return path, cost

		for neighbor, step_cost in graph.get(node, []):
			if neighbor not in visited:
				new_cost = cost + step_cost
				# Greedy priority depends only on h(n), not path cost.
				heappush(frontier, (heuristic(neighbor, goal), new_cost, neighbor, path + [neighbor]))

	# No route to goal was found.
	return [], float("inf")


if __name__ == "__main__":
	# Small Romania map demo.
	romania_map = {
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
	# heuristic values for straight-line distance to Bucharest
	straight_line_to_bucharest = {
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

	def h(city, target):
		# Straight-line-distance heuristic toward Bucharest.
		if target != "Bucharest":
			return 0
		return straight_line_to_bucharest.get(city, 0)

	path, cost = greedy_best_first_search(romania_map, "Arad", "Bucharest", h)
	print("Path :", " -> ".join(path) if path else "No path found")
	print("Cost :", cost)