"""n-Queens - Hill climbing starter implementation."""


def hill_climbing(start, neighbors_fn, score_fn, max_steps=100):
    current = start
    for _ in range(max_steps):
        neighbors = neighbors_fn(current)
        if not neighbors:
            break
        best = max(neighbors, key=score_fn)
        if score_fn(best) <= score_fn(current):
            break
        current = best
    return current


if __name__ == "__main__":
    print("Hill climbing starter ready")
