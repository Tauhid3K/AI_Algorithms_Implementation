from typing import Any, Dict, List, Tuple


def depth_limited_search(
	graph: Dict[Any, List[Any]], start: Any, goal: Any, limit: int
) -> Tuple[List[Any], bool]:
	"""Return (path, cutoff_happened)."""
	if start not in graph or goal not in graph:
		return [], False

	def recursive_dls(node: Any, depth: int, path: List[Any], on_path: set):
		if node == goal:
			return list(path), False
		if depth == limit:
			return [], True

		cutoff = False
		for neighbor in graph.get(node, []):
			if neighbor in on_path:
				continue
			on_path.add(neighbor)
			path.append(neighbor)
			result, child_cutoff = recursive_dls(neighbor, depth + 1, path, on_path)
			if result:
				return result, False
			if child_cutoff:
				cutoff = True
			path.pop()
			on_path.remove(neighbor)

		return [], cutoff

	return recursive_dls(start, 0, [start], {start})
