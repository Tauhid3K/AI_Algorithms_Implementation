def depth_limited_search(graph, start, goal, limit):
	# Return DFS traversal order and whether goal was found under depth limit

	if start not in graph:
		return [], False  # Start node not in graph, nothing to traverse or find

	traversal_order = []  # Record nodes in order they are visited
	goal_found = False    # Flag to stop recursion once goal is found

	def dfs_limited(node, depth, path_visited):  # Recursive helper for depth-limited DFS
		nonlocal goal_found

		# Stop recursion early once goal is found
		if goal_found:
			return

		traversal_order.append(node)              # Record node in traversal order

		# Goal test
		if node == goal:
			goal_found = True
			return

		# Path reconstruction can be added here if needed
		# path = []
		# current = goal
		# while current is not None:
		# 	path.append(current)
		# 	current = parent[current]
		# path.reverse()

		# Stop expansion when limit is reached
		if depth == limit:
			return

		# DFS expansion of neighbors
		for neighbor in graph.get(node, []):    		# Get neighbors, return empty list if node has no neighbors
			if neighbor in path_visited:				# Cycle prevention
				continue
			path_visited.add(neighbor)					# Mark neighbor as visited to prevent cycles
			dfs_limited(neighbor, depth + 1, path_visited)  # Recursive call with increased depth
			path_visited.remove(neighbor)					# Backtrack: explore neighbor of other paths

	dfs_limited(start, 0, {start})  # Initial call with start node, depth 0, and visited set containing start
	return traversal_order, goal_found


if __name__ == "__main__":
	# Example graph
	graph = {
		'A': ['B', 'C'],
		'B': ['D', 'E'],
		'C': ['F', 'G'],
		'D': ['H'],
		'E': [],
		'F': [],
		'G': [],
		'H': []
	}

	start_node = 'A'
	goal_node = 'H'
	limit = 3

	traversal_order, goal_found = depth_limited_search(graph, start_node, goal_node, limit)
	print("Traversal Order:", traversal_order)
	print("Goal Found:", goal_found)