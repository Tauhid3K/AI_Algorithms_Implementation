"""Job Shop Scheduling - Simulated annealing starter implementation."""
import math
import random


def simulated_annealing(start, neighbors_fn, score_fn, temp=100.0, cooling=0.95, min_temp=1e-3):
    current = start
    while temp > min_temp:
        neighbors = neighbors_fn(current)
        if not neighbors:
            break
        nxt = random.choice(neighbors)
        delta = score_fn(nxt) - score_fn(current)
        if delta > 0 or random.random() < math.exp(delta / temp):
            current = nxt
        temp *= cooling
    return current


if __name__ == "__main__":
    print("Simulated annealing starter ready")
