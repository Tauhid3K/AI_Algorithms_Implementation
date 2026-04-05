def depth_limited_search(graph, start, limit):
	# Store visited nodes and traversal order
	visited = set()
	traversal_order = []

	def dfs_limited(node, depth):
		# Stop if depth limit is reached
		if depth > limit:
			return

		if node not in visited:
			visited.add(node)
			traversal_order.append(node)

		# Stop expanding when the limit is reached
		if depth == limit:
			return

		# Visit neighbors using DFS style
		for neighbor in graph.get(node, []):
			dfs_limited(neighbor, depth + 1)

	dfs_limited(start, 0)
	return traversal_order


if __name__ == "__main__":
	# Example tree/graph
	tree = {
		'A': ['B', 'C'],
		'B': ['D', 'E'],
		'C': ['F', 'G'],
		'D': ['H'],
		'E': [],
		'F': [],
		'G': [],
		'H': []
	}

	# Start node and depth limit
	start_node = 'A'
	limit = 3

	# Run depth-limited DFS
	traversal_order = depth_limited_search(tree, start_node, limit)
	print("Traversal Order:", traversal_order)
