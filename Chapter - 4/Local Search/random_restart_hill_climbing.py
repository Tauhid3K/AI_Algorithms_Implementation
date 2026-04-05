import random


def fun(x):
	# Objective function to maximize.
	return -((x - 2) ** 2) + 4


def hill_climb_random(func, start, stop, step=1.5, iteration=100):
	# Start from a random point in the given range.
	x = random.randint(start, stop)
	# Store local optima found during the search.
	di = {} # Dictionary to store local optima and their function values.
	#store x value and f(x) value in the dictionary when local optima is found.

	for i in range(iteration):
		# Compare current point with its two neighbors.
		print(f"Restart {i + 1}: f({x}) - right neighbour f({x + step}) - left neighbour f({x - step})")

		# Move to a better neighbor if one exists.
		if func(x) < func(x + step):
			x += step # Move right if right neighbor is better.
		elif func(x) < func(x - step):
			x -= step # Move left if left neighbor is better.
		else:
			# If stuck, save this local optimum and restart.
			di[x] = func(x)
			x = random.randint(start, stop)

	# Show all local optima found.
	print("Local optima found:", di)
	if not di:
		# If no local optimum was stored, return current position.
		return x

	# Return the best local optimum among all restarts.
	return [i for i, j in di.items() if j == max(di.values())][0]


random_restart_hill_climbing = hill_climb_random


if __name__ == "__main__":
	# Demo run with a random-restart search.
	best_x = hill_climb_random(fun, -10, 10, 1.5, 10)
	print("Best x:", best_x)
	print("Best f(x):", fun(best_x))
