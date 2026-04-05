import random
from typing import Callable, Tuple


State = float


def steepest_ascent_hill_climbing(
	start: State,
	evaluate: Callable[[State], float],
	neighbors: Callable[[State], list[State]],
	max_steps: int = 1000,
) -> Tuple[State, float]:
	"""Maximization hill climbing that always picks the best neighbor."""
	current = start
	current_score = evaluate(current)

	for _ in range(max_steps):
		candidates = neighbors(current)
		if not candidates:
			break

		best = max(candidates, key=evaluate)
		best_score = evaluate(best)
		if best_score <= current_score:
			break

		current, current_score = best, best_score

	return current, current_score


if __name__ == "__main__":
	random.seed(7)
	func = lambda x: -(x - 3.2) ** 2 + 10
	nb = lambda x: [x - 0.2, x + 0.2]
	state, score = steepest_ascent_hill_climbing(0.0, func, nb)
	print("Best state:", round(state, 4), "Score:", round(score, 4))
