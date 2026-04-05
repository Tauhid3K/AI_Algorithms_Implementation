from collections import deque


def bfs(graph, start):
	"""Return BFS traversal order from the start node.

	Args:
		graph (dict): Adjacency list representation of a graph.
		start: Starting node.

	Returns:
		list: Nodes visited in BFS order.
	"""
	if start not in graph:
		return []

	visited = set([start])
	queue = deque([start])
	order = []

	while queue:
		node = queue.popleft()
		order.append(node)

		for neighbor in graph.get(node, []):
			if neighbor not in visited:
				visited.add(neighbor)
				queue.append(neighbor)

	return order


def bfs_shortest_path(graph, start, goal):
	"""Return the shortest path between start and goal using BFS.

	Returns:
		list: Shortest path as a list of nodes, or [] if unreachable.
	"""
	if start not in graph or goal not in graph:
		return []

	queue = deque([start])
	parent = {start: None}

	while queue:
		node = queue.popleft()
		if node == goal:
			break

		for neighbor in graph.get(node, []):
			if neighbor not in parent:
				parent[neighbor] = node
				queue.append(neighbor)

	if goal not in parent:
		return []

	path = []
	current = goal
	while current is not None:
		path.append(current)
		current = parent[current]

	path.reverse()
	return path


def read_graph_from_input():
	"""Read an adjacency-list graph from user input."""
	graph = {}
	n = int(input("Enter number of nodes: "))

	print("Enter each node and its neighbors in this format: node neighbor1 neighbor2 ...")
	print("Example: A B C")

	for _ in range(n):
		parts = input().strip().split()
		if not parts:
			continue

		node = parts[0]
		neighbors = parts[1:]
		graph[node] = neighbors

	# Ensure all neighbor-only nodes also exist as keys.
	for node in list(graph.keys()):
		for neighbor in graph[node]:
			if neighbor not in graph:
				graph[neighbor] = []

	return graph


if __name__ == "__main__":
	graph = read_graph_from_input()
	start_node = input("Enter start node: ").strip()
	goal_node = input("Enter goal node: ").strip()

	traversal = bfs(graph, start_node)
	if traversal:
		print("BFS Traversal:", traversal)
	else:
		print("Start node not found in graph.")

	path = bfs_shortest_path(graph, start_node, goal_node)
	if path:
		print("Shortest Path:", path)
	else:
		print("No path found (or start/goal node is missing).")
