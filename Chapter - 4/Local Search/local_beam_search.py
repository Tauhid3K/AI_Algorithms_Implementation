import random


def fun(x):
	# Objective function to maximize.
	return -((x - 2) ** 2) + 4


def local_beam_search(fun, k=4, start=-10, stop=10, step=1, iteration=10):
	# Start with k random states.
	states = [random.uniform(start, stop) for _ in range(k)]
	# Show the initial beam.
	print("Initial states:", [f"{state:.2f}" for state in states])

	for i in range(iteration):
		# Create neighbours for every state in the beam.
		neighbors = []
		for s in states:
			# Generate left and right neighbours for one state.
			left = s - step
			right = s + step
			# Keep neighbours inside the allowed range.
			if left < start:
				left = start
			if right > stop:
				right = stop
			neighbors.append(left)
			neighbors.append(right)

		# Keep current states and new neighbours together.
		all_states = states + neighbors
		# Remove duplicate states so the beam keeps more variety.
		unique_states = list(dict.fromkeys(all_states))

		# Pick the best k states for the next beam.
		states = sorted(unique_states, key=fun, reverse=True)[:k]

		# Show the current best state in this step.
		print(
			f"[Beam] Step {i + 1}: states={[f'{state:.2f}' for state in states]}, "
			f"best={states[0]:.2f}, f(best)={fun(states[0]):.2f}"
		)

	# Return the best state found in the beam.
	return max(states, key=fun)


if __name__ == "__main__":
	# Demo run.
	best_x = local_beam_search(fun, 4, -10, 10, 1, 10)
	print(f"Best x: {best_x:.2f}")
	print(f"Best f(x): {fun(best_x):.2f}")
