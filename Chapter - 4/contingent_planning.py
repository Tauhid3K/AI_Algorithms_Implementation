from typing import Any, Callable, Dict, List


def contingent_plan(
	start: Any,
	goal_test: Callable[[Any], bool],
	observations: Callable[[Any], List[Any]],
	action_model: Callable[[Any, Any], Any],
	actions: List[Any],
	depth_limit: int = 8,
):
	"""Build a conditional plan tree that branches on observations."""

	def plan(state: Any, depth: int, visited: set):
		if goal_test(state):
			return {"done": state}
		if depth == depth_limit or state in visited:
			return None

		for action in actions:
			next_state = action_model(state, action)
			branches = {}
			ok = True
			for obs in observations(next_state):
				subplan = plan(obs, depth + 1, visited | {state})
				if subplan is None:
					ok = False
					break
				branches[obs] = subplan
			if ok:
				return {"action": action, "branches": branches}

		return None

	return plan(start, 0, set())


if __name__ == "__main__":
	goal_test = lambda s: s == "G"
	obs = lambda s: [s]
	actions = ["move"]
	model = lambda s, a: "G" if s == "S" else s
	print(contingent_plan("S", goal_test, obs, model, actions))
