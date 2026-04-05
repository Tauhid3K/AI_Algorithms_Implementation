from typing import Any, Dict, List, Tuple

from depth_limited_search import depth_limited_search


def iterative_deepening_search(
	graph: Dict[Any, List[Any]], start: Any, goal: Any, max_depth: int = 50
) -> Tuple[List[Any], int]:
	"""Return (path, depth_used). If no path, returns ([], -1)."""
	for depth in range(max_depth + 1):
		path, cutoff = depth_limited_search(graph, start, goal, depth)
		if path:
			return path, depth
		if not cutoff:
			break

	return [], -1
