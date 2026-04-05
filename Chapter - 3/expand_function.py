from typing import Any, Dict, List, Tuple

from search_node import Node


WeightedGraph = Dict[Any, List[Tuple[Any, float]]]


def expand(node: Node, graph: WeightedGraph) -> List[Node]:
	"""Generate successor nodes from a weighted adjacency-list graph."""
	children = []
	for neighbor, step_cost in graph.get(node.state, []):
		children.append(node.child(neighbor, step_cost))
	return children
