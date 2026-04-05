from dataclasses import dataclass, field
from typing import Any, List, Optional


@dataclass(order=True)
class Node:
	"""Generic search-tree node used by informed and uninformed search."""

	priority: float = field(default=0.0)
	state: Any = field(default=None, compare=False)
	parent: Optional["Node"] = field(default=None, compare=False)
	action: Any = field(default=None, compare=False)
	path_cost: float = field(default=0.0, compare=False)
	depth: int = field(default=0, compare=False)

	def child(self, state: Any, cost: float, action: Any = None) -> "Node":
		"""Create a child node with updated path cost and depth."""
		return Node(
			priority=0.0,
			state=state,
			parent=self,
			action=action,
			path_cost=self.path_cost + cost,
			depth=self.depth + 1,
		)

	def solution_path(self) -> List[Any]:
		"""Return states from root to this node."""
		path = []
		current = self
		while current is not None:
			path.append(current.state)
			current = current.parent
		path.reverse()
		return path
