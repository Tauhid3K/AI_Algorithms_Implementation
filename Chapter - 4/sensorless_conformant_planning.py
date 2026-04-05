from collections import deque
from typing import Callable, Dict, FrozenSet, List, Set, Tuple


BeliefState = FrozenSet[str]


def conformant_planning_bfs(
	initial_belief: Set[str],
	actions: List[str],
	transition: Callable[[str, str], Set[str]],
	goal_test: Callable[[str], bool],
):
	"""Find a sequence of actions that reaches goal for every possible state."""
	start = frozenset(initial_belief)
	queue = deque([(start, [])])
	visited = {start}

	while queue:
		belief, plan = queue.popleft()
		if belief and all(goal_test(s) for s in belief):
			return plan, belief

		for action in actions:
			next_belief = set()
			for s in belief:
				next_belief.update(transition(s, action))
			next_belief = frozenset(next_belief)
			if next_belief not in visited:
				visited.add(next_belief)
				queue.append((next_belief, plan + [action]))

	return [], frozenset()


if __name__ == "__main__":
	transitions = {
		("S1", "a"): {"S2"},
		("S2", "a"): {"G"},
		("S1", "b"): {"S1"},
		("S2", "b"): {"S2"},
		("G", "a"): {"G"},
		("G", "b"): {"G"},
	}
	transition_fn = lambda s, a: transitions.get((s, a), {s})
	plan, final_belief = conformant_planning_bfs({"S1", "S2"}, ["a", "b"], transition_fn, lambda s: s == "G")
	print("Plan:", plan)
	print("Final belief:", final_belief)
