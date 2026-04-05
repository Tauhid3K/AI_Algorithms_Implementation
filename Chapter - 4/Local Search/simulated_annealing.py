import math
import random


def simulated_annealing(
	fun,
	start: float = -10.0,
	stop: float = 10.0,
	step: float = 1.0,
	temperature: float = 100.0,
	cooling: float = 0.95,
):
	"""Maximize a 1D function using simulated annealing."""
	x = random.uniform(start, stop)
	best = x
	t = temperature

	while t > 0.1:
		# Small random move (neighbor).
		x_new = x + random.uniform(-step, step)
		x_new = max(start, min(stop, x_new))

		delta = fun(x_new) - fun(x)

		# Accept if better or with probability exp(delta / T).
		if delta > 0 or random.random() < math.exp(delta / t):
			x = x_new
			if fun(x) > fun(best):
				best = x

		t *= cooling

	return best


class Board:
	def __init__(self, size: int = 8) -> None:
		self.size = size
		# Each index is a column, value is the row of the queen.
		self.state = [random.randint(0, size - 1) for _ in range(size)]

	def conflicts(self, state=None) -> int:
		"""Count how many pairs of queens attack each other."""
		if state is None:
			state = self.state
		attacks = 0
		for i in range(self.size):
			for j in range(i + 1, self.size):
				if state[i] == state[j] or abs(state[i] - state[j]) == abs(i - j):
					attacks += 1
		return attacks

	def random_neighbor(self, state=None):
		"""Return a neighbor by moving one queen in a random column."""
		if state is None:
			state = self.state
		new_state = state[:]
		col = random.randint(0, self.size - 1)
		new_row = random.randint(0, self.size - 1)
		while new_row == new_state[col]:
			new_row = random.randint(0, self.size - 1)
		new_state[col] = new_row
		return new_state


class SimulatedAnnealingSolver:
	def __init__(self, board: Board, temperature: float = 100.0, cooling_rate: float = 0.99) -> None:
		self.board = board
		self.temperature = temperature
		self.cooling_rate = cooling_rate

	def solve(self) -> bool:
		current = self.board.state[:]
		current_conflicts = self.board.conflicts(current)

		while self.temperature > 0.1 and current_conflicts > 0:
			neighbor = self.board.random_neighbor(current)
			neighbor_conflicts = self.board.conflicts(neighbor)

			# Difference in conflicts (negative means neighbor is better).
			delta = neighbor_conflicts - current_conflicts

			# Accept if better, or sometimes if worse.
			if delta < 0 or random.random() < math.exp(-delta / self.temperature):
				current = neighbor
				current_conflicts = neighbor_conflicts

			# Cool down.
			self.temperature *= self.cooling_rate

		self.board.state = current
		return current_conflicts == 0


def print_board(state) -> None:
	size = len(state)
	for r in range(size):
		row = ""
		for c in range(size):
			row += "Q " if state[c] == r else ". "
		print(row)
	print()


def simulated_annealing_test(board: Board, max_restarts: int = 100) -> bool:
	for _ in range(max_restarts):
		solver = SimulatedAnnealingSolver(board)
		if solver.solve():
			print("Solved")
			print_board(board.state)
			return True
		board.state = [random.randint(0, board.size - 1) for _ in range(board.size)]

	print("No solution found.")
	print("Best attempt conflicts:", board.conflicts())
	print_board(board.state)
	return False


if __name__ == "__main__":
	random.seed(5)
	board = Board(size=8)
	simulated_annealing_test(board)
