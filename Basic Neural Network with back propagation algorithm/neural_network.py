"""
Basic Neural Network with Backpropagation Algorithm
Implements a simple feedforward neural network with backpropagation for training.
"""

import numpy as np
from typing import List, Tuple, Callable


class NeuralNetwork:
    """
    A simple feedforward neural network with backpropagation training.
    
    Attributes:
        layers: List of layer sizes (including input and output layers)
        weights: List of weight matrices for each layer
        biases: List of bias vectors for each layer
        learning_rate: Learning rate for gradient descent
        activation: Activation function to use (sigmoid, relu, tanh)
        activation_derivative: Derivative of activation function
    """
    
    def __init__(
        self,
        layer_sizes: List[int],
        learning_rate: float = 0.1,
        activation: str = 'sigmoid'
    ):
        """
        Initialize the neural network.
        
        Args:
            layer_sizes: List of layer sizes (e.g., [2, 4, 3, 1] for input, hidden1, hidden2, output)
            learning_rate: Learning rate for training
            activation: Activation function ('sigmoid', 'relu', 'tanh')
        """
        self.layer_sizes = layer_sizes
        self.learning_rate = learning_rate
        self.activation_name = activation
        
        # Initialize weights and biases
        self.weights = []
        self.biases = []
        
        # Xavier/Glorot initialization for weights
        for i in range(len(layer_sizes) - 1):
            w = np.random.randn(layer_sizes[i], layer_sizes[i + 1]) * np.sqrt(2.0 / layer_sizes[i])
            b = np.zeros((1, layer_sizes[i + 1]))
            self.weights.append(w)
            self.biases.append(b)
        
        # Set activation functions
        self._set_activation_function(activation)
    
    def _set_activation_function(self, activation: str):
        """Set activation function and its derivative."""
        if activation == 'sigmoid':
            self.activation = lambda x: 1 / (1 + np.exp(-np.clip(x, -500, 500)))
            self.activation_derivative = lambda x: x * (1 - x)
        elif activation == 'relu':
            self.activation = lambda x: np.maximum(0, x)
            self.activation_derivative = lambda x: (x > 0).astype(float)
        elif activation == 'tanh':
            self.activation = np.tanh
            self.activation_derivative = lambda x: 1 - x ** 2
        else:
            raise ValueError(f"Unknown activation function: {activation}")
    
    def forward(self, X: np.ndarray) -> Tuple[np.ndarray, List[np.ndarray], List[np.ndarray]]:
        """
        Forward pass through the network.
        
        Args:
            X: Input data (batch_size, input_size)
            
        Returns:
            Tuple of (output, z_values, a_values) where:
                - output: Network output (batch_size, output_size)
                - z_values: Pre-activation values for each layer
                - a_values: Post-activation values (activations) for each layer
        """
        z_values = []
        a_values = [X]
        
        current_input = X
        
        for i in range(len(self.weights)):
            z = np.dot(current_input, self.weights[i]) + self.biases[i]
            z_values.append(z)
            
            # Use linear activation for output layer in regression tasks
            if i == len(self.weights) - 1:
                a = z  # Linear output for regression
            else:
                a = self.activation(z)
            
            a_values.append(a)
            current_input = a
        
        return current_input, z_values, a_values
    
    def backward(
        self,
        X: np.ndarray,
        y: np.ndarray,
        z_values: List[np.ndarray],
        a_values: List[np.ndarray]
    ) -> Tuple[List[np.ndarray], List[np.ndarray]]:
        """
        Backpropagation to calculate gradients.
        
        Args:
            X: Input data
            y: Target values
            z_values: Pre-activation values
            a_values: Activation values
            
        Returns:
            Tuple of (weight_gradients, bias_gradients)
        """
        m = X.shape[0]  # Number of samples
        
        # Calculate output layer error
        y_pred = a_values[-1]
        delta = (y_pred - y)  # For MSE loss with linear output
        
        weight_gradients = []
        bias_gradients = []
        
        # Backpropagate through layers
        for i in range(len(self.weights) - 1, -1, -1):
            # Gradient for weights and biases
            dW = np.dot(a_values[i].T, delta) / m
            db = np.sum(delta, axis=0, keepdims=True) / m
            
            weight_gradients.insert(0, dW)
            bias_gradients.insert(0, db)
            
            # Propagate error to previous layer
            if i > 0:
                delta = np.dot(delta, self.weights[i].T) * self.activation_derivative(a_values[i])
        
        return weight_gradients, bias_gradients
    
    def update_weights(self, weight_gradients: List[np.ndarray], bias_gradients: List[np.ndarray]):
        """
        Update weights and biases using calculated gradients.
        
        Args:
            weight_gradients: Gradients for weights
            bias_gradients: Gradients for biases
        """
        for i in range(len(self.weights)):
            self.weights[i] -= self.learning_rate * weight_gradients[i]
            self.biases[i] -= self.learning_rate * bias_gradients[i]
    
    def train(
        self,
        X_train: np.ndarray,
        y_train: np.ndarray,
        epochs: int = 100,
        batch_size: int = 32,
        validation_data: Tuple[np.ndarray, np.ndarray] = None,
        verbose: bool = True
    ):
        """
        Train the neural network using backpropagation.
        
        Args:
            X_train: Training input data
            y_train: Training target data
            epochs: Number of training epochs
            batch_size: Batch size for training
            validation_data: Optional validation data
            verbose: Whether to print training progress
        """
        train_losses = []
        val_losses = []
        
        for epoch in range(epochs):
            # Shuffle training data
            indices = np.random.permutation(len(X_train))
            X_shuffled = X_train[indices]
            y_shuffled = y_train[indices]
            
            epoch_loss = 0
            num_batches = 0
            
            # Mini-batch training
            for batch_start in range(0, len(X_train), batch_size):
                batch_end = min(batch_start + batch_size, len(X_train))
                X_batch = X_shuffled[batch_start:batch_end]
                y_batch = y_shuffled[batch_start:batch_end]
                
                # Forward pass
                y_pred, z_values, a_values = self.forward(X_batch)
                
                # Calculate loss
                batch_loss = np.mean((y_pred - y_batch) ** 2)
                epoch_loss += batch_loss
                num_batches += 1
                
                # Backward pass
                weight_grads, bias_grads = self.backward(X_batch, y_batch, z_values, a_values)
                
                # Update weights
                self.update_weights(weight_grads, bias_grads)
            
            epoch_loss /= num_batches
            train_losses.append(epoch_loss)
            
            # Validation
            if validation_data is not None:
                X_val, y_val = validation_data
                y_val_pred, _, _ = self.forward(X_val)
                val_loss = np.mean((y_val_pred - y_val) ** 2)
                val_losses.append(val_loss)
                
                if verbose and (epoch + 1) % 10 == 0:
                    print(f"Epoch {epoch + 1}/{epochs} - Loss: {epoch_loss:.6f}, Val Loss: {val_loss:.6f}")
            else:
                if verbose and (epoch + 1) % 10 == 0:
                    print(f"Epoch {epoch + 1}/{epochs} - Loss: {epoch_loss:.6f}")
        
        return train_losses, val_losses
    
    def predict(self, X: np.ndarray) -> np.ndarray:
        """
        Make predictions on new data.
        
        Args:
            X: Input data
            
        Returns:
            Predicted values
        """
        output, _, _ = self.forward(X)
        return output
    
    def evaluate(self, X_test: np.ndarray, y_test: np.ndarray) -> float:
        """
        Evaluate the network on test data.
        
        Args:
            X_test: Test input data
            y_test: Test target data
            
        Returns:
            Mean squared error
        """
        y_pred = self.predict(X_test)
        mse = np.mean((y_pred - y_test) ** 2)
        return mse


class ConvolutionalLayer:
    """Convolutional layer for CNN."""
    
    def __init__(self, num_filters: int, filter_size: int = 3, stride: int = 1, padding: int = 0):
        self.num_filters = num_filters
        self.filter_size = filter_size
        self.stride = stride
        self.padding = padding
        self.filters = None
        self.biases = None
    
    def forward(self, X: np.ndarray) -> np.ndarray:
        """Forward pass through convolutional layer."""
        # Simplified implementation - pad input
        padded_X = np.pad(X, self.padding, mode='constant')
        
        # Extract patches and apply filters
        output_size = (X.shape[0] - self.filter_size + 2 * self.padding) // self.stride + 1
        output = np.zeros((X.shape[0], output_size, output_size, self.num_filters))
        
        # Apply convolution (simplified)
        for i in range(0, output_size):
            for j in range(0, output_size):
                for f in range(self.num_filters):
                    output[:, i, j, f] = np.sum(X[:, i:i+self.filter_size, j:j+self.filter_size] * 
                                               self.filters[f])
        
        return output


# Example usage
if __name__ == "__main__":
    # Create sample data (XOR problem)
    X_train = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
    y_train = np.array([[0], [1], [1], [0]])
    
    # Create and train network
    nn = NeuralNetwork(layer_sizes=[2, 4, 4, 1], learning_rate=0.5, activation='sigmoid')
    
    print("Training Neural Network on XOR problem...")
    train_losses, _ = nn.train(X_train, y_train, epochs=1000, verbose=True)
    
    # Make predictions
    predictions = nn.predict(X_train)
    print("\nPredictions:")
    for i, (pred, true) in enumerate(zip(predictions, y_train)):
        print(f"Input: {X_train[i]} -> Predicted: {pred[0]:.4f}, True: {true[0]}")
    
    # Evaluate
    mse = nn.evaluate(X_train, y_train)
    print(f"\nFinal MSE: {mse:.6f}")
