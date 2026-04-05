import heapq
from itertools import count
from typing import Callable, Dict, List, Tuple

from heuristics import manhattan_distance, misplaced_tiles
from search_node import Node


PuzzleState = Tuple[int, int, int, int, int, int, int, int, int]


class EightPuzzleProblem:
	"""8-puzzle state-space representation and A* solver."""

	def __init__(
		self,
		start: PuzzleState,
		goal: PuzzleState = (1, 2, 3, 4, 5, 6, 7, 8, 0),
	):
		if len(start) != 9 or len(goal) != 9:
			raise ValueError("start and goal must have 9 elements")
		self.start = start
		self.goal = goal

	def is_goal(self, state: PuzzleState) -> bool:
		return state == self.goal

	def neighbors(self, state: PuzzleState) -> List[Tuple[PuzzleState, int]]:
		"""Return reachable states with unit step-cost."""
		idx = state.index(0)
		r, c = divmod(idx, 3)
		moves = []

		for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
			nr, nc = r + dr, c + dc
			if 0 <= nr < 3 and 0 <= nc < 3:
				nidx = nr * 3 + nc
				new_state = list(state)
				new_state[idx], new_state[nidx] = new_state[nidx], new_state[idx]
				moves.append((tuple(new_state), 1))

		return moves

	def solve_a_star(self, heuristic: Callable[[PuzzleState, PuzzleState], int]):
		"""Return (path_of_states, cost)."""
		frontier = []
		counter = count()
		root = Node(state=self.start, path_cost=0.0)
		root.priority = heuristic(self.start, self.goal)
		heapq.heappush(frontier, (root.priority, next(counter), root))
		best_cost: Dict[PuzzleState, float] = {self.start: 0.0}

		while frontier:
			_, _, node = heapq.heappop(frontier)
			state = node.state

			if self.is_goal(state):
				return node.solution_path(), node.path_cost

			if node.path_cost > best_cost.get(state, float("inf")):
				continue

			for next_state, step_cost in self.neighbors(state):
				new_cost = node.path_cost + step_cost
				if new_cost < best_cost.get(next_state, float("inf")):
					best_cost[next_state] = new_cost
					child = node.child(next_state, step_cost)
					child.priority = new_cost + heuristic(next_state, self.goal)
					heapq.heappush(frontier, (child.priority, next(counter), child))

		return [], float("inf")


def solve_with_manhattan(start: PuzzleState):
	problem = EightPuzzleProblem(start)
	return problem.solve_a_star(manhattan_distance)


def solve_with_misplaced_tiles(start: PuzzleState):
	problem = EightPuzzleProblem(start)
	return problem.solve_a_star(misplaced_tiles)
