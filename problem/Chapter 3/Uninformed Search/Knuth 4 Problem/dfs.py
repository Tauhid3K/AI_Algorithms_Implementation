"""Knuth 4 Problem - DFS starter implementation."""


def dfs(graph, start):
    stack = [start]
    visited = set()
    order = []

    while stack:
        node = stack.pop()
        if node in visited:
            continue
        visited.add(node)
        order.append(node)
        for neighbor in reversed(graph.get(node, [])):
            if neighbor not in visited:
                stack.append(neighbor)

    return order


if __name__ == "__main__":
    graph = {"A": ["B", "C"], "B": ["D"], "C": [], "D": []}
    print("Traversal:", dfs(graph, "A"))
