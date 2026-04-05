import random


def fun(x):
	return -((x - 2) ** 2) + 4


def first_choice_hill_climbing(func, init, step=2.0, max_iterations=1000):
	# Start from the given initial state.
	x = init
	for i in range(max_iterations):
		# Generate the two immediate neighbors.
		neighbors = [x + step, x - step]
		# Randomize order so the first improving neighbor is chosen.
		random.shuffle(neighbors)
		print(f"Step {i + 1}: current x = {x}, neighbor order = {neighbors}")

		for neighbor in neighbors:
			# Move as soon as one better neighbor is found.
			if func(neighbor) > func(x):
				x = neighbor
				break
		else:
			# No better neighbor found.
			break

	# Return the final local optimum.
	return x


if __name__ == "__main__":
	# Run a simple demo with a random starting point.
	best_x = first_choice_hill_climbing(fun, random.randint(-20, 20), 2.0)
	print("Best x:", best_x)
	print("Best f(x):", fun(best_x))
