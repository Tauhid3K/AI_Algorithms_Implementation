"""Robot Localization - LRTA* starter implementation."""


def lrta_star(start, goal_test, actions_fn, cost_fn, heuristic):
    state = start
    h = {start: heuristic(start)}
    while not goal_test(state):
        actions = actions_fn(state)
        if not actions:
            break
        scored = []
        for a, next_state in actions:
            h.setdefault(next_state, heuristic(next_state))
            scored.append((cost_fn(state, a, next_state) + h[next_state], a, next_state))
        scored.sort(key=lambda x: x[0])
        state = scored[0][2]
    return state


if __name__ == "__main__":
    print("LRTA* starter ready")
