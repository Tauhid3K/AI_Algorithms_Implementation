from collections import deque
from typing import Dict, List, Set


def bidirectional_search_uncertain(
	forward_transitions: Dict[str, Dict[str, float]],
	backward_transitions: Dict[str, Dict[str, float]],
	start_belief: Set[str],
	goal_belief: Set[str],
	probability_threshold: float = 0.4,
):
	"""Bidirectional search over belief states using probability-filtered edges."""

	def successors(belief: frozenset[str], transitions: Dict[str, Dict[str, float]]):
		next_states = set()
		for s in belief:
			for nxt, p in transitions.get(s, {}).items():
				if p >= probability_threshold:
					next_states.add(nxt)
		return frozenset(next_states)

	start = frozenset(start_belief)
	goal = frozenset(goal_belief)

	q_f = deque([start])
	q_b = deque([goal])
	vis_f = {start: None}
	vis_b = {goal: None}

	while q_f and q_b:
		bf = q_f.popleft()
		nf = successors(bf, forward_transitions)
		if nf and nf not in vis_f:
			vis_f[nf] = bf
			if nf in vis_b:
				return True
			q_f.append(nf)

		bb = q_b.popleft()
		nb = successors(bb, backward_transitions)
		if nb and nb not in vis_b:
			vis_b[nb] = bb
			if nb in vis_f:
				return True
			q_b.append(nb)

	return False


if __name__ == "__main__":
	fwd = {
		"S": {"A": 0.9, "B": 0.2},
		"A": {"G": 0.8},
		"B": {"G": 0.3},
	}
	bwd = {
		"G": {"A": 0.9, "B": 0.1},
		"A": {"S": 0.9},
		"B": {"S": 0.2},
	}
	print(bidirectional_search_uncertain(fwd, bwd, {"S"}, {"G"}))
