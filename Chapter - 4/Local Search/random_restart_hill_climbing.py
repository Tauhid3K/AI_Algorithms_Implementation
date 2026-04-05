import random
from typing import Callable, Tuple

from steepest_ascent_hill_climbing import steepest_ascent_hill_climbing


State = float


def random_restart_hill_climbing(
	restart_generator: Callable[[], State],
	evaluate: Callable[[State], float],
	neighbors: Callable[[State], list[State]],
	restarts: int = 20,
	max_steps_each: int = 200,
) -> Tuple[State, float]:
	"""Run steepest ascent multiple times from random initial states."""
	best_state = None
	best_score = float("-inf")

	for _ in range(restarts):
		start = restart_generator()
		state, score = steepest_ascent_hill_climbing(start, evaluate, neighbors, max_steps_each)
		if score > best_score:
			best_state, best_score = state, score

	return best_state, best_score


if __name__ == "__main__":
	random.seed(9)
	func = lambda x: -(x - 4.3) ** 2 + 12
	nb = lambda x: [x - 0.25, x + 0.25]
	start_gen = lambda: random.uniform(-10, 10)
	state, score = random_restart_hill_climbing(start_gen, func, nb)
	print("Best state:", round(state, 4), "Score:", round(score, 4))
