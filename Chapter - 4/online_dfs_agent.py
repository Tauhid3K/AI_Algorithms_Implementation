from typing import Any, Dict, List, Optional


class OnlineDFSAgent:
	"""Online DFS agent that explores unknown graph from percepts."""

	def __init__(self, start_state: Any):
		self.untried: Dict[Any, List[Any]] = {}
		self.unbacktracked: Dict[Any, List[Any]] = {}
		self.result: Dict[tuple[Any, Any], Any] = {}
		self.previous_state: Optional[Any] = None
		self.previous_action: Optional[Any] = None
		self.current_state = start_state

	def next_action(self, state: Any, actions: List[Any], is_goal: bool = False):
		if is_goal:
			return None

		if state not in self.untried:
			self.untried[state] = actions[:]

		if self.previous_state is not None and self.previous_action is not None:
			self.result[(self.previous_state, self.previous_action)] = state
			self.unbacktracked.setdefault(state, [])
			if self.previous_state not in self.unbacktracked[state]:
				self.unbacktracked[state].append(self.previous_state)

		if self.untried[state]:
			action = self.untried[state].pop(0)
		elif self.unbacktracked.get(state):
			back_to = self.unbacktracked[state].pop()
			action = f"BACKTRACK->{back_to}"
		else:
			action = None

		self.previous_state = state
		self.previous_action = action
		self.current_state = state
		return action


if __name__ == "__main__":
	agent = OnlineDFSAgent("A")
	print(agent.next_action("A", ["toB", "toC"]))
	print(agent.next_action("B", ["toD"]))
	print(agent.next_action("D", []))
