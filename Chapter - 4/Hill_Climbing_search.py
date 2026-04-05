from steepest_ascent_hill_climbing import steepest_ascent_hill_climbing


if __name__ == "__main__":
	func = lambda x: -(x - 3.2) ** 2 + 10
	nb = lambda x: [x - 0.2, x + 0.2]
	state, score = steepest_ascent_hill_climbing(0.0, func, nb)
	print("Best state:", round(state, 4), "Score:", round(score, 4))

