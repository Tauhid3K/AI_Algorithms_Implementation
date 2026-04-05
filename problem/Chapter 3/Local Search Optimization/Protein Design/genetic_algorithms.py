"""Protein Design - Genetic algorithm starter implementation."""
import random


def genetic_algorithm(population, fitness_fn, mutate_fn, crossover_fn, generations=50, elite_size=2):
    pop = list(population)
    for _ in range(generations):
        pop.sort(key=fitness_fn, reverse=True)
        next_pop = pop[:elite_size]
        while len(next_pop) < len(pop):
            p1, p2 = random.sample(pop[:max(2, len(pop)//2)], 2)
            child = crossover_fn(p1, p2)
            child = mutate_fn(child)
            next_pop.append(child)
        pop = next_pop
    return max(pop, key=fitness_fn)


if __name__ == "__main__":
    print("Genetic algorithm starter ready")
