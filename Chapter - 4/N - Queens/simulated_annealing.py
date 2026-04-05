import math
import random
from typing import Callable, Tuple


State = float


def simulated_annealing(
	start: State,
	evaluate: Callable[[State], float],
	neighbor_sampler: Callable[[State], State],
	temperature: float = 5.0,
	cooling: float = 0.995,
	min_temperature: float = 1e-3,
	max_steps: int = 20000,
) -> Tuple[State, float]:
	"""Maximization with probabilistic downhill moves."""
	current = start
	current_score = evaluate(current)
	best_state, best_score = current, current_score

	t = temperature
	for _ in range(max_steps):
		if t < min_temperature:
			break

		candidate = neighbor_sampler(current)
		candidate_score = evaluate(candidate)
		delta = candidate_score - current_score

		if delta > 0 or random.random() < math.exp(delta / t):
			current, current_score = candidate, candidate_score
			if current_score > best_score:
				best_state, best_score = current, current_score

		t *= cooling

	return best_state, best_score


if __name__ == "__main__":
	random.seed(5)
	func = lambda x: -(x - 3.0) ** 2 + 9
	sampler = lambda x: x + random.uniform(-0.8, 0.8)
	state, score = simulated_annealing(10.0, func, sampler)
	print("Best state:", round(state, 4), "Score:", round(score, 4))
