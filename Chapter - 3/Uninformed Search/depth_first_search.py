def depth_first_search(graph, start, goal):
	# Initialize DFS data structures
	stack = [start]              # LIFO stack for depth-first exploration
	visited = set()              # Prevent revisiting nodes
	traversal_order = []         # Track nodes in visited order
	parent = {start: None}       # Store parent for path reconstruction

	while stack:
		node = stack.pop()         # Remove last node (LIFO)
		if node not in visited:	   # Check if node has not been visited
			visited.add(node)
			traversal_order.append(node)

			# Push neighbors in reverse to keep left-to-right visit order (stack is LIFO)
			for neighbor in reversed(graph.get(node, [])): # return empty list if node has no neighbors
				if neighbor not in visited and neighbor not in parent:
					parent[neighbor] = node
					stack.append(neighbor)  # Add neighbor to stack for later processing

	# Reconstruct path from start to goal (not necessarily the shortest path)
	path = []
	if goal in parent: 		# Check if goal was found
		current = goal
		while current is not None:  # Backtract to start (start has no parent, None)
			path.append(current)
			current = parent[current]
		path.reverse()
		print("Goal Found!")
	else:
		print("Goal Not Found")

	return traversal_order, path


if __name__ == "__main__":
	# Example graph
	graph = {
		'A': ['B', 'C', 'D'],
		'B': [],
		'C': ['E', 'F'],
		'D': [],
		'E': [],
		'F': ['G', 'H'],
		'G': [],
		'H': []
	}

	start_node = 'A'
	goal_node = 'H'

	traversal_order, path = depth_first_search(graph, start_node, goal_node)
	print("Traversal Order:", traversal_order)
	print("Path:", path)
