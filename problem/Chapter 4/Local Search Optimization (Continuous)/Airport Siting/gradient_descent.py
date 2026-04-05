"""Airport Siting - Gradient descent starter implementation."""


def gradient_descent(x0, grad_fn, lr=0.1, steps=100):
    x = x0
    for _ in range(steps):
        x = x - lr * grad_fn(x)
    return x


if __name__ == "__main__":
    print("Gradient descent starter ready")
