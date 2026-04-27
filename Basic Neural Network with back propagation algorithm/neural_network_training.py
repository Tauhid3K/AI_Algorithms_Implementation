import numpy as np
import matplotlib.pyplot as plt


class NN:
    def __init__(self, sizes, lr=0.5):
        self.lr = lr
        np.random.seed(42)
        self.W = [np.random.randn(sizes[i], sizes[i+1]) * 0.01 for i in range(len(sizes)-1)]
        self.B = [np.zeros((1, sizes[i+1])) for i in range(len(sizes)-1)]
        self.loss = []

    def sig(self, x): return 1/(1+np.exp(-np.clip(x,-500,500)))
    def dsig(self, x): return x*(1-x)
    def relu(self, x): return np.maximum(0,x)
    def drelu(self, x): return (x>0).astype(float)

    def forward(self, X):
        self.A = [X]
        self.Z = []
        A = X

        for i in range(len(self.W)-1):
            Z = A @ self.W[i] + self.B[i]
            A = self.relu(Z)
            self.Z.append(Z)
            self.A.append(A)

        Z = A @ self.W[-1] + self.B[-1]
        A = self.sig(Z)
        self.Z.append(Z)
        self.A.append(A)
        return A

    def backward(self, y):
        m = y.shape[0]
        dZ = self.A[-1] - y
        deltas = [dZ]

        for i in range(len(self.W)-2, -1, -1):
            dZ = (deltas[0] @ self.W[i+1].T) * self.drelu(self.Z[i])
            deltas.insert(0, dZ)

        for i in range(len(self.W)):
            dW = self.A[i].T @ deltas[i] / m
            dB = np.sum(deltas[i],0,keepdims=True)/m
            self.W[i] -= self.lr * dW
            self.B[i] -= self.lr * dB

    def loss_fn(self,y,yh):
        e=1e-7
        yh=np.clip(yh,e,1-e)
        return -np.mean(y*np.log(yh)+(1-y)*np.log(1-yh))

    def train(self,X,y,epochs=1000):
        print("\n[Training] XOR Network")
        for i in range(epochs):
            yhat=self.forward(X)
            self.loss.append(self.loss_fn(y,yhat))
            self.backward(y)

        print(f"  Final Loss: {self.loss[-1]:.6f}")

    def predict(self,X):
        return self.forward(X)

    def plot(self):
        plt.plot(self.loss)
        plt.title("Training Loss")
        plt.show()


# ===== MAIN =====
if __name__ == "__main__":
    print("NEURAL NETWORK WITH BACKPROPAGATION - TOPIC 4")

    X = np.array([[0,0],[0,1],[1,0],[1,1]],dtype=float)
    y = np.array([[0],[1],[1],[0]],dtype=float)

    print("\n>>> EXAMPLE: XOR Problem")
    print("[Problem] Learn XOR function: (0,0)→0, (0,1)→1, (1,0)→1, (1,1)→0")

    print("\n[Network] Architecture: 2 → 4 → 1")
    nn = NN([2,4,1],lr=0.5)

    nn.train(X,y)

    print("\n[Predictions]")
    pred = nn.predict(X)
    for i in range(len(X)):
        print(f"  Input {X[i]} → Target: {y[i][0]:.1f}, Predicted: {pred[i][0]:.4f}")

    acc = np.mean((pred>0.5)==y)*100
    print("\n[Evaluation]")
    print(f"  Accuracy: {acc:.1f}%")

    print("\n[Visualization]")
    try: nn.plot()
    except: print("Plot not supported")
