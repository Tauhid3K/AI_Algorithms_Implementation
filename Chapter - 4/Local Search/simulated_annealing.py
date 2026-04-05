import math
import random


def fun(x):
	# Objective function to maximize.
	return -((x - 2) ** 2) + 4


def simulated_annealing(objective, start=-10, stop=10, step=1.0, temperature=100, cooling=0.95):
	# Start from a random point inside the search range.
	x = random.uniform(start, stop)
	# Keep track of the best point seen so far.
	best = x

	# Continue until temperature becomes very small.
	while temperature > 0.1:
		# Small random move (neighbor).
		x_new = x + random.uniform(-step, step)
		# Clamp neighbor to stay within [start, stop].
		if x_new < start:
			x_new = start
		if x_new > stop:
			x_new = stop

		# Improvement amount from current point to neighbor.
		delta = objective(x_new) - objective(x)

		# Accept if better or with probability exp(delta / T).
		if delta > 0 or random.random() < math.exp(delta / temperature):
			x = x_new
			# Update global best when a better point is found.
			if objective(x) > objective(best):
				best = x

		# Slowly reduce temperature to lower random jumps over time.
		temperature *= cooling

	# Return best point found during the search.
	return best


if __name__ == "__main__":
	# Demo run.
	best_x = simulated_annealing(fun, -10, 10, 1.0, 100, 0.9)
	print(f"Best x: {best_x:.2f}")
	print(f"Best f(x): {fun(best_x):.2f}")
