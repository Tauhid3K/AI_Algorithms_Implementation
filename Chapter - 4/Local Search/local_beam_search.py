import random
from typing import Callable, Tuple


State = float


def local_beam_search(
	initial_states: list[State],
	evaluate: Callable[[State], float],
	neighbors: Callable[[State], list[State]],
	k: int = 3,
	max_steps: int = 200,
) -> Tuple[State, float]:
	"""Keep the best k states among all successors each iteration."""
	beam = list(initial_states[:k])
	if not beam:
		raise ValueError("initial_states must not be empty")

	best_state = max(beam, key=evaluate)
	best_score = evaluate(best_state)

	for _ in range(max_steps):
		all_successors = []
		for state in beam:
			all_successors.extend(neighbors(state))

		if not all_successors:
			break

		all_successors.sort(key=evaluate, reverse=True)
		beam = all_successors[:k]

		candidate = beam[0]
		candidate_score = evaluate(candidate)
		if candidate_score > best_score:
			best_state, best_score = candidate, candidate_score

	return best_state, best_score


if __name__ == "__main__":
	random.seed(11)
	func = lambda x: -(x - 2.7) ** 2 + 9
	nb = lambda x: [x + random.uniform(-0.5, 0.5) for _ in range(4)]
	starts = [random.uniform(-10, 10) for _ in range(5)]
	state, score = local_beam_search(starts, func, nb)
	print("Best state:", round(state, 4), "Score:", round(score, 4))
