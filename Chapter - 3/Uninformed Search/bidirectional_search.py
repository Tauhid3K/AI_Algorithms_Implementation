from collections import deque
from typing import Any, Dict, Iterable, List


def _neighbors(graph: Dict[Any, Iterable], node: Any):
	for item in graph.get(node, []):
		if isinstance(item, tuple):
			yield item[0]
		else:
			yield item


def _build_path(meet, parent_fwd, parent_bwd):
	left = []
	node = meet
	while node is not None:
		left.append(node)
		node = parent_fwd[node]
	left.reverse()

	right = []
	node = parent_bwd[meet]
	while node is not None:
		right.append(node)
		node = parent_bwd[node]

	return left + right


def bidirectional_search(graph: Dict[Any, Iterable], start: Any, goal: Any) -> List[Any]:
	"""Return a path from start to goal for unweighted/undirected graphs."""
	if start not in graph or goal not in graph:
		return []
	if start == goal:
		return [start]

	q_fwd = deque([start])
	q_bwd = deque([goal])
	parent_fwd = {start: None}
	parent_bwd = {goal: None}

	while q_fwd and q_bwd:
		node_f = q_fwd.popleft()
		for nbr in _neighbors(graph, node_f):
			if nbr not in parent_fwd:
				parent_fwd[nbr] = node_f
				if nbr in parent_bwd:
					return _build_path(nbr, parent_fwd, parent_bwd)
				q_fwd.append(nbr)

		node_b = q_bwd.popleft()
		for nbr in _neighbors(graph, node_b):
			if nbr not in parent_bwd:
				parent_bwd[nbr] = node_b
				if nbr in parent_fwd:
					return _build_path(nbr, parent_fwd, parent_bwd)
				q_bwd.append(nbr)

	return []
