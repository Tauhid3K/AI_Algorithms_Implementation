"""Romania Route Finding - BFS starter implementation."""
from collections import deque


def bfs(graph, start):
    visited = {start}
    queue = deque([start])
    order = []

    while queue:
        node = queue.popleft()
        order.append(node)
        for neighbor in graph.get(node, []):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)

    return order


if __name__ == "__main__":
    graph = {"A": ["B", "C"], "B": ["D"], "C": [], "D": []}
    print("Traversal:", bfs(graph, "A"))
