from heapq import heappop, heappush

from heuristics import manhattan_distance, misplaced_tiles


GOAL_STATE = (1, 2, 3, 4, 5, 6, 7, 8, 0)


def get_neighbors(state):
	# 0 is the blank tile that can move up/down/left/right.
	idx = state.index(0)
	r, c = divmod(idx, 3)
	neighbors = []

	for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
		nr, nc = r + dr, c + dc
		if 0 <= nr < 3 and 0 <= nc < 3:
			nidx = nr * 3 + nc
			new_state = list(state)
			new_state[idx], new_state[nidx] = new_state[nidx], new_state[idx]
			neighbors.append(tuple(new_state))

	return neighbors


def solve_eight_puzzle(start, heuristic_name="manhattan"):
	# Choose which heuristic to use for A* priority.
	if heuristic_name == "misplaced":
		heuristic_fn = misplaced_tiles
	else:
		heuristic_fn = manhattan_distance

	# frontier keeps the next states to explore, sorted by f = g + h.
	# (f_cost = g+h, g_cost, state, path)
	frontier = []
	heappush(frontier, (heuristic_fn(start, GOAL_STATE), 0, start, [start]))
	# best_cost stores the cheapest known path to each state.
	best_cost = {start: 0}

	while frontier:
		_, path_cost, state, path = heappop(frontier)

		if state == GOAL_STATE:
			# Goal reached: return total moves and state path.
			return path_cost, path

		if path_cost > best_cost.get(state, float("inf")):
			continue

		for next_state in get_neighbors(state):
			# Every move in 8-puzzle costs 1.
			new_cost = path_cost + 1
			if new_cost < best_cost.get(next_state, float("inf")):
				best_cost[next_state] = new_cost
				priority = new_cost + heuristic_fn(next_state, GOAL_STATE)
				heappush(frontier, (priority, new_cost, next_state, path + [next_state]))

	return float("inf"), []


if __name__ == "__main__":
	start_state = (1, 2, 3, 4, 5, 6, 0, 7, 8)

	cost, path = solve_eight_puzzle(start_state, heuristic_name="manhattan")
	print("Heuristic : Manhattan")
	print("Cost :", cost)
	print("States visited in path :", len(path))

	cost2, path2 = solve_eight_puzzle(start_state, heuristic_name="misplaced")
	print("Heuristic : Misplaced Tiles")
	print("Cost :", cost2)
	print("States visited in path :", len(path2))
