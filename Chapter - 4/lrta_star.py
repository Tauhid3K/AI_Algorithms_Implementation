from typing import Any, Callable, Dict, List, Tuple


Graph = Dict[Any, List[Tuple[Any, float]]]


def lrta_star(
	graph: Graph,
	start: Any,
	goal: Any,
	heuristic: Callable[[Any], float],
	max_steps: int = 200,
):
	"""Learning Real-Time A* for unknown/partially known costs."""
	H = {s: heuristic(s) for s in graph}
	current = start
	path = [current]

	for _ in range(max_steps):
		if current == goal:
			return path, H

		actions = graph.get(current, [])
		if not actions:
			return path, H

		min_cost = float("inf")
		best_next = None
		for nxt, cost in actions:
			est = cost + H.get(nxt, heuristic(nxt))
			if est < min_cost:
				min_cost = est
				best_next = nxt

		H[current] = min_cost
		current = best_next
		path.append(current)

	return path, H


if __name__ == "__main__":
	g = {
		"A": [("B", 1), ("C", 4)],
		"B": [("D", 2)],
		"C": [("D", 1)],
		"D": [],
	}
	h = {"A": 3, "B": 2, "C": 1, "D": 0}
	path, learned = lrta_star(g, "A", "D", lambda s: h.get(s, 0))
	print("Path:", path)
	print("Learned H:", learned)
