import matplotlib.pyplot as plt
import numpy as np
import random


def fun(x):
	return -((x - 2) ** 2) + 4


def hill_climb(func, init, step=1.0, iteration=100):
	# Start from the initial state provided by the user.
	x = init
	for i in range(iteration):
		# Compare current point with two local neighbors.
		print(f"Step {i + 1}: f({x}) -> f({x + step}) OR f({x - step})")

		# Move right if right neighbor improves the objective value.
		if func(x) < func(x + step):
			x += step
		# Otherwise move left if left neighbor improves the objective value.
		elif func(x) < func(x - step):
			x -= step
		else:
			# No better neighbor found, so stop at local optimum.
			break

	# Return the best x found by local search.
	return x


if __name__ == "__main__":
	# Input start point for search.
	while True:
		start_text = input("Enter start x (blank = random -10 to 10): ").strip()
		if start_text == "":
			start = random.randint(-10, 10)
			break
		try:
			start = float(start_text)
			break
		except ValueError:
			print("Invalid input. Please enter a numeric value.")

	# Input step size (neighbor distance).
	while True:
		step_text = input("Enter step size (> 0, default 1.0): ").strip()
		if step_text == "":
			step = 1.0
			break
		try:
			step = float(step_text)
			if step <= 0:
				print("Step size must be greater than 0.")
				continue
			break
		except ValueError:
			print("Invalid input. Please enter a numeric value.")

	# Input maximum number of hill-climbing steps.
	while True:
		iteration_text = input("Enter max iterations (> 0, default 100): ").strip()
		if iteration_text == "":
			iteration = 100
			break
		try:
			iteration = int(iteration_text)
			if iteration <= 0:
				print("Iterations must be greater than 0.")
				continue
			break
		except ValueError:
			print("Invalid input. Please enter an integer value.")

	# Run hill climbing using selected input parameters.
	best_x = hill_climb(fun, start, step, iteration)
	# Report final state and objective value.
	print("Start :", start)
	print("Best x:", best_x)
	print("Best f(x):", fun(best_x))

	# Optional visualization of the objective function.
	while True:
		show_plot_text = input("Show graph now? (y/n, default y): ").strip().lower()
		if show_plot_text == "":
			show_plot = True
			break
		if show_plot_text in ("y", "yes"):
			show_plot = True
			break
		if show_plot_text in ("n", "no"):
			show_plot = False
			break
		print("Please enter y or n.")

	if show_plot:
		# Plot a fixed range so the function shape is easy to inspect.
		li = np.arange(-10, 10)
		plt.plot(li, fun(li))
		plt.title("Hill Climbing Function")
		plt.xlabel("x")
		plt.ylabel("f(x)")
		plt.grid()
		plt.show()

#Greedy → always chooses best local move.
#Step size matters → too large may skip max, too small → slower convergence.
#Local maxima → could stop at a peak that’s not global max.
#Random restart can improve chance of finding global maximum.