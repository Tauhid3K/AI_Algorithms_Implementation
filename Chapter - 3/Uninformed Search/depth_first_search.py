from typing import Any, Dict, List


def depth_first_search(graph: Dict[Any, List[Any]], start: Any, goal: Any = None):
	"""Return DFS traversal order or a path if goal is provided."""
	if start not in graph:
		return []

	stack = [(start, [start])]
	visited = set()
	order = []

	while stack:
		node, path = stack.pop()
		if node in visited:
			continue

		visited.add(node)
		order.append(node)

		if goal is not None and node == goal:
			return path

		for neighbor in reversed(graph.get(node, [])):
			if neighbor not in visited:
				stack.append((neighbor, path + [neighbor]))

	return order if goal is None else []
