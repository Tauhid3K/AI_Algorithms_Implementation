import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.optim import Adam
from torch.utils.data import DataLoader, TensorDataset
from sklearn.datasets import make_classification
from tqdm import tqdm


# Create synthetic dataset using sklearn's make_classification
data, labels = make_classification(
    n_samples=100,
    n_features=10,
    n_classes=2,
    n_informative=8,
    random_state=42,
)

# PyTorch uses tensors
data = torch.tensor(data, dtype=torch.float32)
labels = torch.tensor(labels, dtype=torch.long)

# DataLoader loads the data in batches and shuffles during training
dataset = TensorDataset(data, labels)
dataloader = DataLoader(dataset, batch_size=16, shuffle=True)


class SimpleNN(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super(SimpleNN, self).__init__()
        self.fc1 = nn.Linear(input_size, hidden_size)  # hidden layer
        self.fc2 = nn.Linear(hidden_size, output_size)  # output layer
        self.relu = nn.ReLU()

    def forward(self, x):
        x = self.relu(self.fc1(x))
        x = self.fc2(x)
        return x


def train_model(epochs=100, input_size=10, hidden_size=5, output_size=2):
    model = SimpleNN(input_size, hidden_size, output_size)
    model.train()

    optimizer = Adam(model.parameters(), lr=0.001)
    criterion = nn.CrossEntropyLoss()

    for epoch in tqdm(range(epochs), desc="Training (Auto Backprop)"):
        for inputs, target in dataloader:
            outputs = model(inputs)
            loss = criterion(outputs, target)

            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

        if (epoch + 1) % 10 == 0:
            print(f"Epoch [{epoch + 1}/{epochs}], Loss: {loss.item():.4f}")

    return model


if __name__ == "__main__":
    trained_model = train_model()