from heapq import heappop, heappush
 #f(n) = g(n) + h(n) (UCS + Greedy)

def a_star(graph, heuristic, start, goal): 

	frontier = []   #priority queue of (f_cost, path_cost, node, path)
	heappush(frontier, (heuristic[start], 0, start, [start]))
	# Best known f-cost for each node.
	best_graph = {start: heuristic[start]}

	while frontier:
		f_cost, path_cost, node, path_list = heappop(frontier)

		if node == goal:
			# Goal reached with the current best path.
			return path_cost, path_list

		# Ignore outdated heap entries.
		if f_cost > best_graph.get(node, float("inf")):
			continue

		for neighbor, neighbor_cost in graph.get(node, []):
			# f(n) = g(n) + h(n)
			updated_cost = path_cost + neighbor_cost + heuristic.get(neighbor, float("inf"))
			if updated_cost < best_graph.get(neighbor, float("inf")):
				best_graph[neighbor] = updated_cost
				heappush(
					frontier,
					(updated_cost, path_cost + neighbor_cost, neighbor, path_list + [neighbor]),
					# f(n) = g(n) + h(n), g(n) = path_cost + neighbor_cost, h(n) = heuristic[neighbor] 
				)

	return float("inf"), []


a_star_search = a_star


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
		# Straight-line distance heuristic to Bucharest.
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

	cost, path = a_star(G, H, "Arad", "Bucharest")
	print("Path :", " -> ".join(path) if path else "No path found")
	print("Cost :", cost)
