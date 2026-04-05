import math
from typing import Any, Callable, Dict, List, Tuple

from expand_function import expand
from search_node import Node


WeightedGraph = Dict[Any, List[Tuple[Any, float]]]


def recursive_best_first_search(
	graph: WeightedGraph,
	start: Any,
	goal: Any,
	heuristic: Callable[[Any, Any], float],
):
	"""Return (path, cost). If no solution, returns ([], inf)."""
	if start not in graph or goal not in graph:
		return [], float("inf")

	root = Node(state=start, path_cost=0.0)
	root.priority = heuristic(start, goal)

	def rbfs(node: Node, f_limit: float, path_states: set):
		if node.state == goal:
			return node, node.priority

		path_states.add(node.state)
		try:
			successors = [s for s in expand(node, graph) if s.state not in path_states]
			if not successors:
				return None, math.inf

			for succ in successors:
				g = succ.path_cost
				succ.priority = max(g + heuristic(succ.state, goal), node.priority)

			while True:
				successors.sort(key=lambda n: n.priority)
				best = successors[0]
				if best.priority > f_limit:
					return None, best.priority

				alternative = successors[1].priority if len(successors) > 1 else math.inf
				result, best.priority = rbfs(best, min(f_limit, alternative), path_states)
				if result is not None:
					return result, best.priority
		finally:
			path_states.discard(node.state)

	result, _ = rbfs(root, math.inf, set())
	if result is None:
		return [], float("inf")
	return result.solution_path(), result.path_cost
