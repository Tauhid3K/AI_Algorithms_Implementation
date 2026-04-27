import numpy as np

# Sigmoid function
def sigmoid(x):
    return 1 / (1 + np.exp(-x))

# Derivative of sigmoid
def sigmoid_deriv(x):
    return x * (1 - x)

# Input (XOR problem)
X = np.array([[0,0],
              [0,1],
              [1,0],
              [1,1]])

# Output
y = np.array([[0],
              [1],
              [1],
              [0]])

# Seed for reproducibility
np.random.seed(1)

# Weights
w1 = np.random.rand(2, 2)
w2 = np.random.rand(2, 1)

lr = 0.1

# Training
for i in range(10000):

    # Forward pass
    l1 = sigmoid(np.dot(X, w1))
    l2 = sigmoid(np.dot(l1, w2))

    # Error
    error = y - l2

    # Backpropagation
    d2 = error * sigmoid_deriv(l2)
    d1 = d2.dot(w2.T) * sigmoid_deriv(l1)

    # Update weights
    w2 += l1.T.dot(d2) * lr
    w1 += X.T.dot(d1) * lr

# Output after training
print("Output after training:")
print(l2)
