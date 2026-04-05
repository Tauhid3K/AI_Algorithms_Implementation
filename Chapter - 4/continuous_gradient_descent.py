from typing import Callable, List, Tuple


Vector = List[float]


def numerical_gradient(f: Callable[[Vector], float], x: Vector, eps: float = 1e-6) -> Vector:
	grad = []
	for i in range(len(x)):
		x1 = x[:]
		x2 = x[:]
		x1[i] += eps
		x2[i] -= eps
		grad.append((f(x1) - f(x2)) / (2 * eps))
	return grad


def gradient_descent(
	f: Callable[[Vector], float],
	start: Vector,
	learning_rate: float = 0.1,
	max_steps: int = 1000,
	tolerance: float = 1e-8,
) -> Tuple[Vector, float]:
	"""Minimize f in continuous space with gradient descent."""
	x = start[:]
	for _ in range(max_steps):
		g = numerical_gradient(f, x)
		norm = sum(v * v for v in g) ** 0.5
		if norm < tolerance:
			break
		x = [xi - learning_rate * gi for xi, gi in zip(x, g)]
	return x, f(x)


if __name__ == "__main__":
	f = lambda v: (v[0] - 1) ** 2 + (v[1] + 2) ** 2
	x, val = gradient_descent(f, [5.0, 5.0], learning_rate=0.2)
	print("Argmin:", [round(i, 4) for i in x], "f(x)=", round(val, 6))
