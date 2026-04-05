from heapq import heappop, heappush
# for min-heap priority queue

def ucs(graph, start, goal):
	frontier = [(0, start, [start])] # (cost, node, path)
	best_cost = {start: 0}			 # best cost to reach each node

	while frontier:
		cost, node, path = heappop(frontier)  # get lowest cost node

		if node == goal:
			return path, cost

		if cost > best_cost.get(node, float("inf")): # skip if we already have a better cost to this node
			continue

		for neighbor, step_cost in graph.get(node, []):
			new_cost = cost + step_cost
			if new_cost < best_cost.get(neighbor, float("inf")): 
				# only add to frontier if we found a cheaper path to neighbor
				best_cost[neighbor] = new_cost
				heappush(frontier, (new_cost, neighbor, path + [neighbor]))

	return [], float("inf")


uniform_cost_search = ucs


if __name__ == "__main__":
	ROMANIA_MAP = {
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

	path, cost = ucs(ROMANIA_MAP, "Arad", "Bucharest")

	print("Path :", " -> ".join(path) if path else "No path found")
	print("Cost :", cost)
