"""Maze Exploration - Online DFS starter implementation."""


def online_dfs_agent(start, successors_fn, goal_test):
    stack = [start]
    visited = set()
    while stack:
        state = stack.pop()
        if state in visited:
            continue
        visited.add(state)
        if goal_test(state):
            return state
        stack.extend(reversed(successors_fn(state)))
    return None


if __name__ == "__main__":
    print("Online DFS starter ready")
