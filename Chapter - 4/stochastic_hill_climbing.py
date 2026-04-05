import random
from typing import Callable, Tuple


State = float


def stochastic_hill_climbing(
	start: State,
	evaluate: Callable[[State], float],
	neighbors: Callable[[State], list[State]],
	max_steps: int = 1000,
) -> Tuple[State, float]:
	"""Choose randomly among improving neighbors."""
	current = start
	current_score = evaluate(current)

	for _ in range(max_steps):
		improving = [s for s in neighbors(current) if evaluate(s) > current_score]
		if not improving:
			break

		next_state = random.choice(improving)
		current, current_score = next_state, evaluate(next_state)

	return current, current_score


if __name__ == "__main__":
	random.seed(12)
	func = lambda x: -(x - 2.5) ** 2 + 8
	nb = lambda x: [x - 0.3, x + 0.3]
	state, score = stochastic_hill_climbing(0.0, func, nb)
	print("Best state:", round(state, 4), "Score:", round(score, 4))
