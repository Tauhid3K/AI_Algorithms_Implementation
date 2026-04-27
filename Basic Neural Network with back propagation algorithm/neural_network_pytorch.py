"""
Neural Network with PyTorch - Backpropagation Algorithm
Implements a simple feedforward neural network using PyTorch for automatic differentiation.
"""

import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
from typing import Tuple


class SimpleNeuralNetwork(nn.Module):
    """Simple Neural Network for XOR problem."""
    
    def __init__(self, input_size: int = 2, hidden_size: int = 2, output_size: int = 1):
        """
        Initialize the neural network.
        
        Args:
            input_size: Size of input layer
            hidden_size: Size of hidden layer(s)
            output_size: Size of output layer
        """
        super(SimpleNeuralNetwork, self).__init__()
        
        self.fc1 = nn.Linear(input_size, hidden_size)
        self.sigmoid1 = nn.Sigmoid()
        self.fc2 = nn.Linear(hidden_size, output_size)
        self.sigmoid2 = nn.Sigmoid()
    
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """
        Forward pass through the network.
        
        Args:
            x: Input tensor
            
        Returns:
            Output tensor
        """
        x = self.fc1(x)
        x = self.sigmoid1(x)
        x = self.fc2(x)
        x = self.sigmoid2(x)
        return x


class DeepNeuralNetwork(nn.Module):
    """Deep Neural Network with multiple hidden layers."""
    
    def __init__(self, layer_sizes: list):
        """
        Initialize deep neural network.
        
        Args:
            layer_sizes: List of layer sizes [input, hidden1, hidden2, ..., output]
        """
        super(DeepNeuralNetwork, self).__init__()
        
        self.layers = nn.ModuleList()
        self.activations = nn.ModuleList()
        
        for i in range(len(layer_sizes) - 1):
            self.layers.append(nn.Linear(layer_sizes[i], layer_sizes[i + 1]))
            # Use Sigmoid for all except last layer can be linear
            if i < len(layer_sizes) - 2:
                self.activations.append(nn.Sigmoid())
            else:
                self.activations.append(nn.Sigmoid())  # Output layer activation
    
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """Forward pass through all layers."""
        for layer, activation in zip(self.layers, self.activations):
            x = layer(x)
            x = activation(x)
        return x


class NeuralNetworkTrainer:
    """Trainer for neural networks with backpropagation."""
    
    def __init__(self, model: nn.Module, learning_rate: float = 0.1, criterion=None):
        """
        Initialize trainer.
        
        Args:
            model: Neural network model
            learning_rate: Learning rate for optimizer
            criterion: Loss function (default: MSELoss)
        """
        self.model = model
        self.learning_rate = learning_rate
        self.criterion = criterion or nn.MSELoss()
        self.optimizer = optim.SGD(model.parameters(), lr=learning_rate)
        self.loss_history = []
    
    def train(self, X: torch.Tensor, y: torch.Tensor, epochs: int = 1000, 
              verbose: bool = False) -> list:
        """
        Train the neural network.
        
        Args:
            X: Input data tensor
            y: Target data tensor
            epochs: Number of training epochs
            verbose: Whether to print loss information
            
        Returns:
            List of loss values for each epoch
        """
        self.loss_history = []
        
        for epoch in range(epochs):
            # Forward pass
            output = self.model(X)
            
            # Calculate loss
            loss = self.criterion(output, y)
            self.loss_history.append(loss.item())
            
            # Backward pass (automatic differentiation)
            self.optimizer.zero_grad()  # Clear gradients
            loss.backward()  # Backpropagation
            self.optimizer.step()  # Update weights
            
            if verbose and (epoch + 1) % (epochs // 10) == 0:
                print(f"Epoch {epoch + 1}/{epochs} - Loss: {loss.item():.6f}")
        
        return self.loss_history
    
    def predict(self, X: torch.Tensor) -> torch.Tensor:
        """
        Make predictions on new data.
        
        Args:
            X: Input data tensor
            
        Returns:
            Predicted values
        """
        with torch.no_grad():  # No gradient computation for inference
            return self.model(X)
    
    def evaluate(self, X: torch.Tensor, y: torch.Tensor) -> float:
        """
        Evaluate model on test data.
        
        Args:
            X: Test input data
            y: Test target data
            
        Returns:
            Loss value
        """
        with torch.no_grad():
            output = self.model(X)
            loss = self.criterion(output, y)
        return loss.item()


def train_xor_network(epochs: int = 10000, verbose: bool = True) -> Tuple[nn.Module, list]:
    """
    Train a neural network on XOR problem.
    
    Args:
        epochs: Number of training epochs
        verbose: Whether to print progress
        
    Returns:
        Tuple of (trained model, loss history)
    """
    # XOR training data
    X = torch.tensor([[0., 0.],
                      [0., 1.],
                      [1., 0.],
                      [1., 1.]])
    
    y = torch.tensor([[0.],
                      [1.],
                      [1.],
                      [0.]])
    
    # Create and train model
    model = SimpleNeuralNetwork(input_size=2, hidden_size=2, output_size=1)
    trainer = NeuralNetworkTrainer(model, learning_rate=0.5)
    
    print("Training Neural Network on XOR problem...")
    loss_history = trainer.train(X, y, epochs=epochs, verbose=verbose)
    
    print("\nPredictions:")
    print("-" * 50)
    predictions = trainer.predict(X)
    for inp, pred, true in zip(X, predictions, y):
        print(f"Input: {inp.numpy()} -> Predicted: {pred.item():.4f}, True: {true.item()}")
    
    final_loss = trainer.evaluate(X, y)
    print(f"\nFinal Loss (MSE): {final_loss:.6f}")
    
    return model, loss_history


def train_deep_network(epochs: int = 1000, verbose: bool = True) -> Tuple[nn.Module, list]:
    """
    Train a deep neural network on XOR problem.
    
    Args:
        epochs: Number of training epochs
        verbose: Whether to print progress
        
    Returns:
        Tuple of (trained model, loss history)
    """
    # XOR training data
    X = torch.tensor([[0., 0.],
                      [0., 1.],
                      [1., 0.],
                      [1., 1.]])
    
    y = torch.tensor([[0.],
                      [1.],
                      [1.],
                      [0.]])
    
    # Create and train deep model
    model = DeepNeuralNetwork([2, 8, 8, 1])
    trainer = NeuralNetworkTrainer(model, learning_rate=0.5)
    
    print("Training Deep Neural Network on XOR problem...")
    print("Architecture: 2 -> 8 -> 8 -> 1")
    loss_history = trainer.train(X, y, epochs=epochs, verbose=verbose)
    
    print("\nPredictions:")
    print("-" * 50)
    predictions = trainer.predict(X)
    for inp, pred, true in zip(X, predictions, y):
        print(f"Input: {inp.numpy()} -> Predicted: {pred.item():.4f}, True: {true.item()}")
    
    final_loss = trainer.evaluate(X, y)
    print(f"\nFinal Loss (MSE): {final_loss:.6f}")
    
    return model, loss_history


# Example usage
if __name__ == "__main__":
    print("="*60)
    print("PYTORCH NEURAL NETWORK WITH BACKPROPAGATION")
    print("="*60)
    
    print("\n1. Simple Neural Network (2-2-1):")
    print("-" * 60)
    simple_model, simple_losses = train_xor_network(epochs=10000, verbose=False)
    
    print("\n\n2. Deep Neural Network (2-8-8-1):")
    print("-" * 60)
    deep_model, deep_losses = train_deep_network(epochs=5000, verbose=False)
    
    print("\n\n" + "="*60)
    print("TRAINING COMPLETED")
    print("="*60)
