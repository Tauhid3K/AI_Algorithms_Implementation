"""Job Shop Scheduling - Local beam search starter implementation."""


def local_beam_search(initial_states, neighbors_fn, score_fn, beam_width=3, iterations=50):
    states = list(initial_states)
    for _ in range(iterations):
        all_neighbors = []
        for s in states:
            all_neighbors.extend(neighbors_fn(s))
        if not all_neighbors:
            break
        states = sorted(all_neighbors, key=score_fn, reverse=True)[:beam_width]
    return max(states, key=score_fn)


if __name__ == "__main__":
    print("Local beam search starter ready")
