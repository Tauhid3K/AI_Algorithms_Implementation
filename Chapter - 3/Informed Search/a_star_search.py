import heapq
from itertools import count
from typing import Any, Callable, Dict, List, Tuple

from search_node import Node


WeightedGraph = Dict[Any, List[Tuple[Any, float]]]


def a_star_search(
	graph: WeightedGraph, start: Any, goal: Any, heuristic: Callable[[Any, Any], float]
):
	"""Return (path, cost). If no solution, returns ([], inf)."""
	if start not in graph or goal not in graph:
		return [], float("inf")

	frontier = []
	counter = count()
	root = Node(state=start, path_cost=0.0)
	root.priority = heuristic(start, goal)
	heapq.heappush(frontier, (root.priority, next(counter), root))
	best_cost = {start: 0.0}

	while frontier:
		_, _, node = heapq.heappop(frontier)

		if node.state == goal:
			return node.solution_path(), node.path_cost

		if node.path_cost > best_cost.get(node.state, float("inf")):
			continue

		for neighbor, step_cost in graph.get(node.state, []):
			new_cost = node.path_cost + step_cost
			if new_cost < best_cost.get(neighbor, float("inf")):
				best_cost[neighbor] = new_cost
				child = node.child(neighbor, step_cost)
				child.priority = new_cost + heuristic(neighbor, goal)
				heapq.heappush(frontier, (child.priority, next(counter), child))

	return [], float("inf")
