import heapq
from itertools import count
from typing import Any, Dict, List, Tuple

from search_node import Node


WeightedGraph = Dict[Any, List[Tuple[Any, float]]]


def uniform_cost_search(graph: WeightedGraph, start: Any, goal: Any):
	"""Return (path, cost). If no solution, returns ([], inf)."""
	if start not in graph or goal not in graph:
		return [], float("inf")

	frontier = []
	counter = count()
	root = Node(state=start, path_cost=0.0, priority=0.0)
	heapq.heappush(frontier, (0.0, next(counter), root))
	best_cost = {start: 0.0}

	while frontier:
		cost, _, node = heapq.heappop(frontier)

		if node.state == goal:
			return node.solution_path(), node.path_cost

		if cost > best_cost.get(node.state, float("inf")):
			continue

		for neighbor, step_cost in graph.get(node.state, []):
			new_cost = node.path_cost + step_cost
			if new_cost < best_cost.get(neighbor, float("inf")):
				best_cost[neighbor] = new_cost
				child = node.child(neighbor, step_cost)
				heapq.heappush(frontier, (new_cost, next(counter), child))

	return [], float("inf")
