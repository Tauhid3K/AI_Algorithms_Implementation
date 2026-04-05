from typing import Any, Dict, List, Tuple

from search_node import Node


WeightedGraph = Dict[Any, List[Tuple[Any, float]]]


def expand(node: Node, graph: WeightedGraph) -> List[Node]:
	"""Generate successor nodes from a weighted adjacency-list graph."""
	children = []
	for neighbor, step_cost in graph.get(node.state, []):
		children.append(node.child(neighbor, step_cost))
	return children


if __name__ == "__main__":
	# Tiny weighted graph for expansion demo.
	graph = {
		"A": [("B", 2), ("C", 3)],
		"B": [("D", 4)],
		"C": [],
		"D": [],
	}

	start = Node(state="A", path_cost=0)
	children = expand(start, graph)
	# Prints each child state with its accumulated path cost.
	print("Expanded from A :", [(child.state, child.path_cost) for child in children])
