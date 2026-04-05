from typing import Any, Dict, List, Optional


AndOrGraph = Dict[Any, List[List[Any]]]


def and_or_graph_search(graph: AndOrGraph, start: Any, goals: set[Any]):
	"""Return a conditional plan as nested dicts/lists, or None if failure."""

	def or_search(state: Any, path: list[Any]):
		if state in goals:
			return []
		if state in path:
			return None

		for and_set in graph.get(state, []):
			subplan = and_search(and_set, path + [state])
			if subplan is not None:
				return {"if": state, "then": subplan}

		return None

	def and_search(states: list[Any], path: list[Any]):
		plan = {}
		for s in states:
			p = or_search(s, path)
			if p is None:
				return None
			plan[s] = p
		return plan

	return or_search(start, [])


if __name__ == "__main__":
	graph = {
		"S": [["A", "B"], ["C"]],
		"A": [["G1"]],
		"B": [["G2"]],
		"C": [["G3"]],
	}
	goals = {"G1", "G2", "G3"}
	plan = and_or_graph_search(graph, "S", goals)
	print("Plan:", plan)
