"""Romania Route Finding - IDS starter implementation."""


def dfs_limited(graph, node, limit, visited):
    if node in visited:
        return
    visited.append(node)
    if limit == 0:
        return
    for neighbor in graph.get(node, []):
        dfs_limited(graph, neighbor, limit - 1, visited)


def iterative_deepening(graph, start, max_limit):
    iterations = []
    for depth in range(1, max_limit + 1):
        visited = []
        dfs_limited(graph, start, depth, visited)
        iterations.append((depth, visited))
    return iterations


if __name__ == "__main__":
    graph = {"A": ["B", "C"], "B": ["D"], "C": [], "D": []}
    for depth, order in iterative_deepening(graph, "A", 3):
        print(f"Depth {depth}:", order)
