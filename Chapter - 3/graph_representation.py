from typing import Any, Dict, Iterable, List, Tuple


def make_unweighted_graph(edges: Iterable[Tuple[Any, Any]], directed: bool = False) -> Dict[Any, List[Any]]:
	"""Build an unweighted adjacency list from edge pairs."""
	graph: Dict[Any, List[Any]] = {}
	for u, v in edges:
		graph.setdefault(u, []).append(v)
		graph.setdefault(v, [])
		if not directed:
			graph[v].append(u)
	return graph


def make_weighted_graph(
	edges: Iterable[Tuple[Any, Any, float]], directed: bool = False
) -> Dict[Any, List[Tuple[Any, float]]]:
	"""Build a weighted adjacency list from (u, v, cost) triples."""
	graph: Dict[Any, List[Tuple[Any, float]]] = {}
	for u, v, cost in edges:
		graph.setdefault(u, []).append((v, cost))
		graph.setdefault(v, [])
		if not directed:
			graph[v].append((u, cost))
	return graph


if __name__ == "__main__":
	# Example edges for quick testing.
	unweighted_edges = [("A", "B"), ("A", "C"), ("B", "D")]
	weighted_edges = [("A", "B", 2), ("A", "C", 5), ("B", "D", 1)]

	print("Unweighted Graph :", make_unweighted_graph(unweighted_edges))
	print("Weighted Graph :", make_weighted_graph(weighted_edges))
