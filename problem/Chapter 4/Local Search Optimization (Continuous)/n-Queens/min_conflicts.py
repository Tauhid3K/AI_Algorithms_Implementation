"""n-Queens - Min-conflicts starter implementation."""
import random


def min_conflicts(state, conflicts_fn, repair_fn, max_steps=1000):
    current = state
    for _ in range(max_steps):
        if conflicts_fn(current) == 0:
            return current
        current = repair_fn(current, random)
    return current


if __name__ == "__main__":
    print("Min-conflicts starter ready")
