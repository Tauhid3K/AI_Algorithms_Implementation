"""Romania Route Finding - Bidirectional search starter implementation."""
from collections import deque


def bidirectional_search(graph, start, goal):
    if start == goal:
        return [start]

    q1, q2 = deque([start]), deque([goal])
    p1, p2 = {start: None}, {goal: None}

    while q1 and q2:
        m = _expand(graph, q1, p1, p2)
        if m is not None:
            return _build_path(m, p1, p2)
        m = _expand(graph, q2, p2, p1)
        if m is not None:
            return _build_path(m, p1, p2)

    return []


def _expand(graph, queue, parent, other_parent):
    node = queue.popleft()
    for n in graph.get(node, []):
        if n not in parent:
            parent[n] = node
            if n in other_parent:
                return n
            queue.append(n)
    return None


def _build_path(meet, p1, p2):
    left, cur = [], meet
    while cur is not None:
        left.append(cur)
        cur = p1[cur]
    left.reverse()

    right, cur = [], p2[meet]
    while cur is not None:
        right.append(cur)
        cur = p2[cur]

    return left + right


if __name__ == "__main__":
    graph = {"A": ["B", "C"], "B": ["A", "D"], "C": ["A", "D"], "D": ["B", "C"]}
    print("Path:", bidirectional_search(graph, "A", "D"))
