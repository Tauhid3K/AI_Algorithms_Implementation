import math
import random


def fun(state):
	# Count how many pairs of queens attack each other.
	attacks = 0
	size = len(state)
	for i in range(size):
		for j in range(i + 1, size):
			# Queens attack if they share a row or diagonal.
			if state[i] == state[j] or abs(state[i] - state[j]) == abs(i - j):
				attacks += 1
	return attacks


def neighbor(state):
	# Move one queen to a random row in the same column.
	new_state = state[:]
	col = random.randint(0, len(state) - 1)
	new_state[col] = random.randint(0, len(state) - 1)
	return new_state


def simulated_annealing(size=8, temperature=100, cooling_rate=0.99):
	# Start with a random board.
	state = [random.randint(0, size - 1) for _ in range(size)]
	current_conflicts = fun(state)

	# Keep searching while temperature is still high.
	while temperature > 0.1 and current_conflicts > 0:
		new_state = neighbor(state)
		new_conflicts = fun(new_state)

		# Lower conflicts is better.
		delta = new_conflicts - current_conflicts

		# Accept better boards, and sometimes worse ones.
		if delta < 0 or random.random() < math.exp(-delta / temperature):
			state = new_state
			current_conflicts = new_conflicts

		# Gradually reduce temperature.
		temperature *= cooling_rate

	return state, current_conflicts


def print_board(state):
	size = len(state)
	for r in range(size):
		row = ""
		for c in range(size):
			row += "Q " if state[c] == r else ". "
		print(row)
	print()


if __name__ == "__main__":
	# Try a few times because simulated annealing is random.
	for _ in range(100):
		board, score = simulated_annealing()
		if score == 0:
			print_board(board)
			break
	else:
		print("No solution found.")
