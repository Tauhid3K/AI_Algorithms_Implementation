import random
from typing import Callable, Tuple


State = float


def first_choice_hill_climbing(
	start: State,
	evaluate: Callable[[State], float],
	neighbor_sampler: Callable[[State], State],
	max_steps: int = 1000,
	samples_per_step: int = 40,
) -> Tuple[State, float]:
	"""Accept the first sampled neighbor that improves the objective."""
	current = start
	current_score = evaluate(current)

	for _ in range(max_steps):
		moved = False
		for _ in range(samples_per_step):
			candidate = neighbor_sampler(current)
			score = evaluate(candidate)
			if score > current_score:
				current, current_score = candidate, score
				moved = True
				break
		if not moved:
			break

	return current, current_score


if __name__ == "__main__":
	random.seed(3)
	func = lambda x: -(x - 1.8) ** 2 + 6
	sampler = lambda x: x + random.uniform(-0.5, 0.5)
	state, score = first_choice_hill_climbing(0.0, func, sampler)
	print("Best state:", round(state, 4), "Score:", round(score, 4))
