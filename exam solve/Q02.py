import random
import math

def sigmoid(x):
    return 1 / (1 + math.exp(-x))

def sigmoid_derivative(output):
    return output * (1 - output)

training_data = [
    ([0, 0], [0]),
    ([0, 1], [1]),
    ([1, 0], [1]),
    ([1, 1], [0])
]

random.seed(1)

w1 = random.random()
w2 = random.random()
w3 = random.random()
w4 = random.random()

w5 = random.random()
w6 = random.random()

b1 = random.random()
b2 = random.random()
b3 = random.random()

lr = 0.5
epochs = 10000

for epoch in range(epochs):

    total_error = 0

    for inputs, target in training_data:

        x1 = inputs[0]
        x2 = inputs[1]
        y = target[0]

        h1_input = x1*w1 + x2  *w2 + b1
        h1_output = sigmoid(h1_input)

        h2_input = x1*w3 + x2*w4 + b2
        h2_output = sigmoid(h2_input)

        o1_input = h1_output*w5 + h2_output*w6 + b3
        o1_output = sigmoid(o1_input)

        error = y - o1_output
        total_error += error**2

        delta_output = error * sigmoid_derivative(o1_output)

        delta_h1 = delta_output * w5 * sigmoid_derivative(h1_output)
        delta_h2 = delta_output * w6 * sigmoid_derivative(h2_output)

        w5 += lr * delta_output * h1_output
        w6 += lr * delta_output * h2_output

        w1 += lr * delta_h1 * x1
        w2 += lr * delta_h1 * x2

        w3 += lr * delta_h2 * x1
        w4 += lr * delta_h2 * x2

        b3 += lr * delta_output
        b1 += lr * delta_h1
        b2 += lr * delta_h2

    if epoch % 1000 == 0:
        print("Epoch:", epoch, "Error:", total_error)

print("\nFinal Predictions:")

for inputs, target in training_data:

    x1 = inputs[0]
    x2 = inputs[1]
    
    #forword
    h1 = sigmoid(x1*w1 + x2*w2 + b1)
    h2 = sigmoid(x1*w3 + x2*w4 + b2)

    output = sigmoid(h1*w5 + h2*w6 + b3)

    print(inputs, "=>", round(output, 3))