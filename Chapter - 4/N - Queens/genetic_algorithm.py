import random
from typing import Callable, List, Tuple


Genome = List[float]


def genetic_algorithm(
	fitness: Callable[[Genome], float],
	population_size: int = 30,
	genome_length: int = 5,
	generations: int = 80,
	mutation_rate: float = 0.05,
) -> Tuple[Genome, float]:
	"""Simple real-valued GA with tournament selection and single-point crossover."""
	if population_size < 2:
		raise ValueError("population_size must be >= 2")

	population = [
		[random.uniform(-5, 5) for _ in range(genome_length)] for _ in range(population_size)
	]

	def tournament_select(k: int = 3) -> Genome:
		candidates = random.sample(population, k=min(k, len(population)))
		return max(candidates, key=fitness)

	def crossover(a: Genome, b: Genome) -> Genome:
		point = random.randint(1, genome_length - 1)
		return a[:point] + b[point:]

	def mutate(g: Genome) -> Genome:
		out = g[:]
		for i in range(len(out)):
			if random.random() < mutation_rate:
				out[i] += random.uniform(-0.5, 0.5)
		return out

	for _ in range(generations):
		new_population = []
		elite = max(population, key=fitness)
		new_population.append(elite[:])

		while len(new_population) < population_size:
			p1 = tournament_select()
			p2 = tournament_select()
			child = crossover(p1, p2)
			child = mutate(child)
			new_population.append(child)

		population = new_population

	best = max(population, key=fitness)
	return best, fitness(best)


if __name__ == "__main__":
	random.seed(21)
	target = [1.0, -2.0, 0.5, 3.0, -1.5]

	def fit(g):
		return -sum((x - t) ** 2 for x, t in zip(g, target))

	best_genome, best_fitness = genetic_algorithm(fit)
	print("Best genome:", [round(x, 3) for x in best_genome])
	print("Best fitness:", round(best_fitness, 4))
