import numpy as np
from sklearn.datasets import make_classification
from tqdm import tqdm


def relu(x):
    return np.maximum(0, x)


def relu_grad(x):
    return (x > 0).astype(np.float32)


def softmax(x):
    x_shifted = x - np.max(x, axis=1, keepdims=True)
    exp_x = np.exp(x_shifted)
    return exp_x / np.sum(exp_x, axis=1, keepdims=True)


def one_hot(labels, num_classes):
    y = np.zeros((labels.shape[0], num_classes), dtype=np.float32)
    y[np.arange(labels.shape[0]), labels] = 1.0
    return y


class SimpleNNManual:
    def __init__(self, input_size, hidden_size, output_size):
        rng = np.random.default_rng(42)
        self.W1 = rng.normal(0, 0.1, (input_size, hidden_size)).astype(np.float32)
        self.b1 = np.zeros((1, hidden_size), dtype=np.float32)
        self.W2 = rng.normal(0, 0.1, (hidden_size, output_size)).astype(np.float32)
        self.b2 = np.zeros((1, output_size), dtype=np.float32)

    def forward(self, x):
        z1 = x @ self.W1 + self.b1
        a1 = relu(z1)
        z2 = a1 @ self.W2 + self.b2
        probs = softmax(z2)
        cache = (x, z1, a1, z2, probs)
        return probs, cache

    def backward(self, cache, y_onehot):
        x, z1, a1, _, probs = cache
        m = x.shape[0]

        # Cross-entropy gradient for softmax output
        dz2 = (probs - y_onehot) / m
        dW2 = a1.T @ dz2
        db2 = np.sum(dz2, axis=0, keepdims=True)

        da1 = dz2 @ self.W2.T
        dz1 = da1 * relu_grad(z1)
        dW1 = x.T @ dz1
        db1 = np.sum(dz1, axis=0, keepdims=True)

        return dW1, db1, dW2, db2

    def step(self, grads, lr):
        dW1, db1, dW2, db2 = grads
        self.W1 -= lr * dW1
        self.b1 -= lr * db1
        self.W2 -= lr * dW2
        self.b2 -= lr * db2


def get_batches(data, labels, batch_size):
    idx = np.random.permutation(len(data))
    data_shuffled = data[idx]
    labels_shuffled = labels[idx]
    for start in range(0, len(data), batch_size):
        end = min(start + batch_size, len(data))
        yield data_shuffled[start:end], labels_shuffled[start:end]


def train_manual_model(epochs=100, input_size=10, hidden_size=5, output_size=2, lr=0.01):
    # Same style dataset as automatic version
    data, labels = make_classification(
        n_samples=100,
        n_features=10,
        n_classes=2,
        n_informative=8,
        random_state=42,
    )
    data = data.astype(np.float32)
    labels = labels.astype(np.int64)
    labels_onehot = one_hot(labels, output_size)

    model = SimpleNNManual(input_size, hidden_size, output_size)
    batch_size = 16

    for epoch in tqdm(range(epochs), desc="Training (Manual Backprop)"):
        last_loss = 0.0
        for x_batch, y_batch in get_batches(data, labels, batch_size):
            y_batch_onehot = one_hot(y_batch, output_size)
            probs, cache = model.forward(x_batch)

            # Cross-entropy loss
            eps = 1e-9
            last_loss = -np.mean(np.sum(y_batch_onehot * np.log(probs + eps), axis=1))

            grads = model.backward(cache, y_batch_onehot)
            model.step(grads, lr)

        if (epoch + 1) % 10 == 0:
            print(f"Epoch [{epoch + 1}/{epochs}], Loss: {last_loss:.4f}")

    return model


if __name__ == "__main__":
    trained_model = train_manual_model()