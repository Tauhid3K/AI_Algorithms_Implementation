from typing import Tuple


PuzzleState = Tuple[int, int, int, int, int, int, int, int, int]


def manhattan_distance(state: PuzzleState, goal: PuzzleState) -> int:
	"""Sum of Manhattan distances of each tile from goal positions."""
	total = 0
	for tile in range(1, 9):
		i = state.index(tile)
		j = goal.index(tile)
		r1, c1 = divmod(i, 3)
		r2, c2 = divmod(j, 3)
		total += abs(r1 - r2) + abs(c1 - c2)
	return total


def misplaced_tiles(state: PuzzleState, goal: PuzzleState) -> int:
	"""Count tiles that are not in the goal position (excluding blank=0)."""
	return sum(1 for i, tile in enumerate(state) if tile != 0 and tile != goal[i])


if __name__ == "__main__":
	# Sample start/goal for heuristic comparison.
	start = (1, 2, 3, 4, 5, 6, 0, 7, 8)
	goal = (1, 2, 3, 4, 5, 6, 7, 8, 0)

	print("Manhattan Distance :", manhattan_distance(start, goal))
	print("Misplaced Tiles :", misplaced_tiles(start, goal))
