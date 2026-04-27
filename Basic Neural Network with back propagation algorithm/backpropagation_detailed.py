"""
Backpropagation Algorithm - Step by Step Implementation
Shows the complete backpropagation process with detailed calculations.
"""

import numpy as np
from typing import Tuple, List


class BackpropagationAlgorithm:
    """Detailed implementation of backpropagation algorithm."""
    
    def __init__(self, layer_sizes: List[int], learning_rate: float = 0.1):
        """
        Initialize the network.
        
        Args:
            layer_sizes: List of layer sizes
            learning_rate: Learning rate
        """
        self.layer_sizes = layer_sizes
        self.learning_rate = learning_rate
        self.weights = []
        self.biases = []
        self.initialize_weights()
    
    def initialize_weights(self):
        """Initialize weights using small random values."""
        for i in range(len(self.layer_sizes) - 1):
            # Xavier initialization
            limit = np.sqrt(6.0 / (self.layer_sizes[i] + self.layer_sizes[i + 1]))
            w = np.random.uniform(-limit, limit, 
                                 (self.layer_sizes[i], self.layer_sizes[i + 1]))
            b = np.zeros((1, self.layer_sizes[i + 1]))
            
            self.weights.append(w)
            self.biases.append(b)
    
    @staticmethod
    def sigmoid(x: np.ndarray) -> np.ndarray:
        """Sigmoid activation function."""
        return 1 / (1 + np.exp(-np.clip(x, -500, 500)))
    
    @staticmethod
    def sigmoid_derivative(output: np.ndarray) -> np.ndarray:
        """Derivative of sigmoid."""
        return output * (1 - output)
    
    @staticmethod
    def relu(x: np.ndarray) -> np.ndarray:
        """ReLU activation function."""
        return np.maximum(0, x)
    
    @staticmethod
    def relu_derivative(x: np.ndarray) -> np.ndarray:
        """Derivative of ReLU."""
        return (x > 0).astype(float)
    
    def forward_propagation(self, X: np.ndarray) -> Tuple[np.ndarray, List, List]:
        """
        Forward propagation through all layers.
        
        Args:
            X: Input data
            
        Returns:
            Tuple of (output, z_values, activations)
        """
        self.z_values = []
        self.activations = [X]
        
        current_input = X
        
        for i in range(len(self.weights)):
            # Calculate pre-activation (z)
            z = np.dot(current_input, self.weights[i]) + self.biases[i]
            self.z_values.append(z)
            
            # Apply activation
            if i == len(self.weights) - 1:  # Output layer - linear
                a = z
            else:  # Hidden layers - sigmoid
                a = self.sigmoid(z)
            
            self.activations.append(a)
            current_input = a
        
        return current_input, self.z_values, self.activations
    
    def calculate_output_error(self, y_true: np.ndarray, y_pred: np.ndarray) -> np.ndarray:
        """
        Calculate error at output layer.
        
        Args:
            y_true: True labels
            y_pred: Predicted values
            
        Returns:
            Output error delta
        """
        # For MSE loss: dL/da = 2(a - y)
        # Then da/dz = 1 for linear output
        return (y_pred - y_true)
    
    def backpropagation(self, X: np.ndarray, y: np.ndarray, 
                       y_pred: np.ndarray) -> Tuple[List, List]:
        """
        Backpropagation algorithm.
        
        Args:
            X: Input data
            y: True labels
            y_pred: Predicted values
            
        Returns:
            Tuple of (weight gradients, bias gradients)
        """
        m = X.shape[0]  # Number of samples
        
        # Initialize gradients
        weight_gradients = [None] * len(self.weights)
        bias_gradients = [None] * len(self.biases)
        
        # Calculate output layer error
        delta = self.calculate_output_error(y, y_pred)
        
        # Backpropagate through layers
        for l in range(len(self.weights) - 1, -1, -1):
            # Calculate gradients for layer l
            weight_gradients[l] = np.dot(self.activations[l].T, delta) / m
            bias_gradients[l] = np.sum(delta, axis=0, keepdims=True) / m
            
            # Propagate error to previous layer
            if l > 0:
                # delta_l = (delta_{l+1} @ W_{l+1}^T) * sigmoid'(z_l)
                delta = np.dot(delta, self.weights[l].T) * self.sigmoid_derivative(self.activations[l])
        
        return weight_gradients, bias_gradients
    
    def update_weights(self, weight_gradients: List, bias_gradients: List):
        """
        Update weights and biases using gradient descent.
        
        Args:
            weight_gradients: Gradients for weights
            bias_gradients: Gradients for biases
        """
        for i in range(len(self.weights)):
            self.weights[i] -= self.learning_rate * weight_gradients[i]
            self.biases[i] -= self.learning_rate * bias_gradients[i]
    
    def train_step(self, X: np.ndarray, y: np.ndarray) -> float:
        """
        Single training step (forward + backward + update).
        
        Args:
            X: Input data
            y: Target data
            
        Returns:
            Loss value
        """
        # Forward pass
        y_pred, _, _ = self.forward_propagation(X)
        
        # Calculate loss (MSE)
        loss = np.mean((y_pred - y) ** 2)
        
        # Backward pass
        weight_grads, bias_grads = self.backpropagation(X, y, y_pred)
        
        # Update weights
        self.update_weights(weight_grads, bias_grads)
        
        return loss
    
    def train(self, X: np.ndarray, y: np.ndarray, epochs: int = 100, 
             verbose: bool = True) -> List:
        """
        Train the network.
        
        Args:
            X: Training input data
            y: Training target data
            epochs: Number of training epochs
            verbose: Whether to print progress
            
        Returns:
            List of loss values
        """
        loss_history = []
        
        for epoch in range(epochs):
            loss = self.train_step(X, y)
            loss_history.append(loss)
            
            if verbose and (epoch + 1) % max(1, epochs // 10) == 0:
                print(f"Epoch {epoch + 1}/{epochs} - Loss: {loss:.6f}")
        
        return loss_history
    
    def predict(self, X: np.ndarray) -> np.ndarray:
        """Make predictions."""
        output, _, _ = self.forward_propagation(X)
        return output


class DetailedBackpropagationAnalysis:
    """Analyzes backpropagation process in detail."""
    
    @staticmethod
    def print_gradient_analysis(network: BackpropagationAlgorithm, 
                               X: np.ndarray, y: np.ndarray):
        """Print detailed gradient information."""
        print("\n" + "="*60)
        print("DETAILED BACKPROPAGATION ANALYSIS")
        print("="*60)
        
        # Forward pass
        y_pred, z_values, activations = network.forward_propagation(X)
        
        print("\n1. FORWARD PROPAGATION:")
        print("-" * 60)
        for i, (z, a) in enumerate(zip(z_values, activations[1:])):
            print(f"\nLayer {i+1}:")
            print(f"  Pre-activation (z) shape: {z.shape}")
            print(f"  Pre-activation mean: {np.mean(z):.6f}")
            print(f"  Pre-activation std: {np.std(z):.6f}")
            print(f"  Activation shape: {a.shape}")
            print(f"  Activation mean: {np.mean(a):.6f}")
            print(f"  Activation range: [{np.min(a):.6f}, {np.max(a):.6f}]")
        
        print("\n2. BACKPROPAGATION:")
        print("-" * 60)
        weight_grads, bias_grads = network.backpropagation(X, y, y_pred)
        
        for i, (wg, bg) in enumerate(zip(weight_grads, bias_grads)):
            print(f"\nLayer {i+1}:")
            print(f"  Weight gradient shape: {wg.shape}")
            print(f"  Weight gradient mean: {np.mean(wg):.6f}")
            print(f"  Weight gradient std: {np.std(wg):.6f}")
            print(f"  Bias gradient shape: {bg.shape}")
            print(f"  Bias gradient mean: {np.mean(bg):.6f}")
        
        print("\n3. WEIGHT UPDATES:")
        print("-" * 60)
        learning_rate = network.learning_rate
        for i, (wg, w) in enumerate(zip(weight_grads, network.weights)):
            update_magnitude = learning_rate * np.mean(np.abs(wg))
            weight_magnitude = np.mean(np.abs(w))
            ratio = update_magnitude / (weight_magnitude + 1e-8)
            print(f"\nLayer {i+1}:")
            print(f"  Weight magnitude: {weight_magnitude:.6f}")
            print(f"  Update magnitude: {update_magnitude:.6f}")
            print(f"  Update ratio: {ratio:.6f}")


# Example usage
if __name__ == "__main__":
    print("="*60)
    print("BACKPROPAGATION ALGORITHM DEMONSTRATION")
    print("="*60)
    
    # XOR problem
    X = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
    y = np.array([[0], [1], [1], [0]])
    
    # Create and train network
    network = BackpropagationAlgorithm([2, 4, 4, 1], learning_rate=0.5)
    
    print("\nTraining on XOR problem...")
    losses = network.train(X, y, epochs=5000, verbose=True)
    
    # Detailed analysis
    DetailedBackpropagationAnalysis.print_gradient_analysis(network, X, y)
    
    # Predictions
    print("\n" + "="*60)
    print("PREDICTIONS")
    print("="*60)
    predictions = network.predict(X)
    for inp, pred, true in zip(X, predictions, y):
        print(f"Input: {inp} -> Predicted: {pred[0]:.4f}, True: {true[0]}")
