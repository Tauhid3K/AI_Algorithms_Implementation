import heapq
from itertools import count
from typing import Any, Callable, Dict, List, Tuple

from search_node import Node


WeightedGraph = Dict[Any, List[Tuple[Any, float]]]


def greedy_best_first_search(
	graph: WeightedGraph, start: Any, goal: Any, heuristic: Callable[[Any, Any], float]
):
	"""Return (path, cost). Greedy uses h(n) as priority only."""
	if start not in graph or goal not in graph:
		return [], float("inf")

	frontier = []
	counter = count()
	root = Node(state=start, path_cost=0.0)
	root.priority = heuristic(start, goal)
	heapq.heappush(frontier, (root.priority, next(counter), root))
	visited = set()

	while frontier:
		_, _, node = heapq.heappop(frontier)
		if node.state in visited:
			continue

		visited.add(node.state)
		if node.state == goal:
			return node.solution_path(), node.path_cost

		for neighbor, step_cost in graph.get(node.state, []):
			if neighbor in visited:
				continue
			child = node.child(neighbor, step_cost)
			child.priority = heuristic(neighbor, goal)
			heapq.heappush(frontier, (child.priority, next(counter), child))

	return [], float("inf")
