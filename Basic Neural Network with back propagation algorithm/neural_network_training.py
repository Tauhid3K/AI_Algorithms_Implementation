"""
Basic Neural Network with Backpropagation Algorithm - Topic 4
Implementation of a simple feedforward neural network trained with backpropagation
"""

import numpy as np
import matplotlib.pyplot as plt


class NeuralNetworkTrainer:
    """Simple neural network with backpropagation for training"""

    def __init__(self, layer_sizes, learning_rate=0.1):
        """
        Initialize network with given layer sizes
        layer_sizes: list of neurons per layer, e.g., [2, 4, 1]
        """
        self.layer_sizes = layer_sizes
        self.learning_rate = learning_rate
        self.weights = []
        self.biases = []
        self.losses = []
        
        self._initialize_weights()

    def _initialize_weights(self):
        """Initialize weights and biases with random values"""
        np.random.seed(42)
        for i in range(len(self.layer_sizes) - 1):
            w = np.random.randn(self.layer_sizes[i], self.layer_sizes[i + 1]) * 0.01
            b = np.zeros((1, self.layer_sizes[i + 1]))
            self.weights.append(w)
            self.biases.append(b)
        print(f"✓ Initialized network: {self.layer_sizes}")

    def sigmoid(self, z):
        """Sigmoid activation function"""
        return 1 / (1 + np.exp(-np.clip(z, -500, 500)))

    def sigmoid_derivative(self, a):
        """Derivative of sigmoid: σ'(z) = σ(z)(1 - σ(z))"""
        return a * (1 - a)

    def relu(self, z):
        """ReLU activation function"""
        return np.maximum(0, z)

    def relu_derivative(self, z):
        """Derivative of ReLU"""
        return (z > 0).astype(float)

    def forward_pass(self, X):
        """
        Forward pass through network
        X: input data of shape (samples, input_features)
        """
        self.activations = [X]
        self.z_values = []
        
        A = X
        for i in range(len(self.weights) - 1):
            Z = np.dot(A, self.weights[i]) + self.biases[i]
            A = self.relu(Z)
            self.z_values.append(Z)
            self.activations.append(A)
        
        # Output layer with sigmoid
        Z = np.dot(A, self.weights[-1]) + self.biases[-1]
        A = self.sigmoid(Z)
        self.z_values.append(Z)
        self.activations.append(A)
        
        return A

    def backward_pass(self, y):
        """
        Backward pass: compute gradients using chain rule
        y: target output
        """
        m = y.shape[0]
        deltas = []
        
        # Output layer error
        dZ = self.activations[-1] - y
        deltas.insert(0, dZ)
        
        # Hidden layer errors (backpropagate)
        for i in range(len(self.weights) - 2, -1, -1):
            dZ = np.dot(deltas[0], self.weights[i + 1].T) * self.relu_derivative(self.z_values[i])
            deltas.insert(0, dZ)
        
        # Update weights and biases
        for i in range(len(self.weights)):
            dW = np.dot(self.activations[i].T, deltas[i]) / m
            dB = np.sum(deltas[i], axis=0, keepdims=True) / m
            
            self.weights[i] -= self.learning_rate * dW
            self.biases[i] -= self.learning_rate * dB

    def compute_loss(self, y_pred, y_true):
        """Binary cross-entropy loss"""
        epsilon = 1e-7
        y_pred = np.clip(y_pred, epsilon, 1 - epsilon)
        return -np.mean(y_true * np.log(y_pred) + (1 - y_true) * np.log(1 - y_pred))

    def train(self, X_train, y_train, epochs=100, verbose=True):
        """
        Train the network
        X_train: training inputs (samples, features)
        y_train: training targets (samples, 1)
        """
        print(f"\n[Training] Epochs: {epochs}, Learning rate: {self.learning_rate}")
        
        for epoch in range(epochs):
            # Forward pass
            y_pred = self.forward_pass(X_train)
            
            # Compute loss
            loss = self.compute_loss(y_pred, y_train)
            self.losses.append(loss)
            
            # Backward pass
            self.backward_pass(y_train)
            
            if verbose and (epoch + 1) % (epochs // 10) == 0:
                print(f"  Epoch {epoch + 1}/{epochs} - Loss: {loss:.6f}")
        
        print(f"  Final Loss: {self.losses[-1]:.6f}")

    def predict(self, X):
        """Make predictions on new data"""
        return self.forward_pass(X)

    def plot_loss(self):
        """Plot training loss over epochs"""
        plt.figure(figsize=(10, 5))
        plt.plot(self.losses, linewidth=2)
        plt.xlabel('Epoch')
        plt.ylabel('Loss')
        plt.title('Training Loss Over Time')
        plt.grid(True, alpha=0.3)
        plt.show()


# Example Usage
if __name__ == "__main__":
    print("=" * 60)
    print("NEURAL NETWORK WITH BACKPROPAGATION - TOPIC 4")
    print("=" * 60)
    
    # XOR Problem (classic test case)
    print("\n>>> EXAMPLE: XOR Problem")
    print("[Problem] Learn XOR function: (0,0)→0, (0,1)→1, (1,0)→1, (1,1)→0")
    
    X_train = np.array([
        [0, 0],
        [0, 1],
        [1, 0],
        [1, 1]
    ], dtype=np.float32)
    
    y_train = np.array([
        [0],
        [1],
        [1],
        [0]
    ], dtype=np.float32)
    
    # Create and train network
    print("\n[Network] Architecture: 2 → 4 → 1")
    network = NeuralNetworkTrainer(layer_sizes=[2, 4, 1], learning_rate=0.5)
    
    print("\n[Training] XOR Network")
    network.train(X_train, y_train, epochs=1000, verbose=False)
    
    # Make predictions
    print("\n[Predictions]")
    predictions = network.predict(X_train)
    for i, (x, y, pred) in enumerate(zip(X_train, y_train, predictions)):
        print(f"  Input {x} → Target: {y[0]:.1f}, Predicted: {pred[0]:.4f}")
    
    # Accuracy
    print("\n[Evaluation]")
    pred_binary = (predictions > 0.5).astype(int)
    accuracy = np.mean(pred_binary == y_train) * 100
    print(f"  Accuracy: {accuracy:.1f}%")
    
    # Plot training curve
    print("\n[Visualization] Generating loss plot...")
    try:
        network.plot_loss()
    except:
        print("  (Plot requires matplotlib GUI)")
    
    print("\n" + "=" * 60)
