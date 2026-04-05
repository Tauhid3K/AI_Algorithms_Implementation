"""Sensorless Vacuum World - Belief state search starter implementation."""


def belief_state_search(initial_belief, actions, transition_fn):
    belief = set(initial_belief)
    for action in actions:
        belief = transition_fn(belief, action)
    return belief


if __name__ == "__main__":
    print("Belief-state starter ready")
