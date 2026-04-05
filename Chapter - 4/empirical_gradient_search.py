import random
from typing import Callable, List, Tuple


Vector = List[float]


def empirical_gradient_search(
	f: Callable[[Vector], float],
	start: Vector,
	step_size: float = 0.1,
	probe: float = 0.05,
	max_steps: int = 500,
):
	"""Estimate gradient from random directional probes and perform descent."""
	x = start[:]
	best_x = x[:]
	best_val = f(x)

	for _ in range(max_steps):
		direction = [random.uniform(-1, 1) for _ in x]
		norm = (sum(d * d for d in direction) ** 0.5) or 1.0
		direction = [d / norm for d in direction]

		x_plus = [xi + probe * di for xi, di in zip(x, direction)]
		x_minus = [xi - probe * di for xi, di in zip(x, direction)]
		grad_mag = (f(x_plus) - f(x_minus)) / (2 * probe)

		est_grad = [grad_mag * di for di in direction]
		x = [xi - step_size * gi for xi, gi in zip(x, est_grad)]

		val = f(x)
		if val < best_val:
			best_x, best_val = x[:], val

	return best_x, best_val


if __name__ == "__main__":
	random.seed(42)
	f = lambda v: (v[0] - 2) ** 2 + (v[1] + 1) ** 2 + 0.2 * (v[0] * v[1])
	x, val = empirical_gradient_search(f, [6.0, -6.0])
	print("Best point:", [round(i, 4) for i in x], "f(x)=", round(val, 6))
