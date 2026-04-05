import random


def fun(state):
	# Count how many queen pairs attack each other.
	attacks = 0
	size = len(state)
	for i in range(size):
		for j in range(i + 1, size):
			if state[i] == state[j] or abs(state[i] - state[j]) == abs(i - j):
				attacks += 1
	return attacks


def fitness(state):
	# Higher fitness means fewer conflicts.
	size = len(state)
	max_pairs = (size * (size - 1)) // 2
	return max_pairs - fun(state)


def create_individual(size):
	# One queen in each column, row chosen randomly.
	return [random.randint(0, size - 1) for _ in range(size)]


def selection(population):
	# Tournament selection: pick the better of two random boards.
	a, b = random.sample(population, 2)
	return a if fitness(a) > fitness(b) else b


def crossover(parent1, parent2):
	# Combine the first part of one parent with the rest of the other.
	size = len(parent1)
	point = random.randint(1, size - 2)
	return parent1[:point] + parent2[point:]


def mutate(individual, mutation_rate):
	# Randomly move one queen to a different row.
	if random.random() < mutation_rate:
		col = random.randint(0, len(individual) - 1)
		individual[col] = random.randint(0, len(individual) - 1)
	return individual


def solve(size=8, population_size=100, mutation_rate=0.05, max_generations=10000):
	# Start with a random population.
	population = [create_individual(size) for _ in range(population_size)]
	max_fitness = (size * (size - 1)) // 2

	for generation in range(max_generations):
		# Stop if we already found a perfect board.
		for individual in population:
			if fitness(individual) == max_fitness:
				return individual, generation

		# Build the next generation.
		new_population = []
		for _ in range(population_size):
			parent1 = selection(population)
			parent2 = selection(population)
			child = crossover(parent1, parent2)
			child = mutate(child, mutation_rate)
			new_population.append(child)

		population = new_population

	return None, max_generations


def print_board(state):
	size = len(state)
	for r in range(size):
		row = ""
		for c in range(size):
			row += "Q " if state[c] == r else ". "
		print(row)
	print()


if __name__ == "__main__":
	random.seed(21)
	solution, generations = solve(size=8, population_size=4, mutation_rate=0.1)

	if solution:
		print(f"Solution found in {generations} generations:\n")
		print_board(solution)
	else:
		print("No solution found.")
