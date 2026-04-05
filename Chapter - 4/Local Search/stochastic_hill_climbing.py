import numpy as np
import random
import matplotlib.pyplot as plt

# Example function (same as before)
def fun(x):
    return -((x - 2) ** 2) + 4

# Stochastic Hill Climbing
def stochastic_hill_climb(fun, init, step=1.0, iteration=100):
    x = init
    
    for i in range(iteration):  # Iterate for a fixed number of steps
        # Generate neighbors
        neighbors = [x + step, x - step]
        # Evaluate neighbors
        better_neighbors = [n 
                            for n in neighbors 
                            if fun(n) > fun(x)] 
        # only keep neighbors that are better than current x
        
        print(f"Step {i+1}: Current x={x}, better neighbors={better_neighbors}") 
        #Print current state and better neighbors
        
        if not better_neighbors:
            # No improvement, stop
            break
        
        # Randomly pick one of the better neighbors
        x = random.choice(better_neighbors) # this is the stochastic part
        
    return x

if __name__ == "__main__":
    # Run stochastic hill climbing first (prints steps).
    start = random.randint(-10, 10)
    result = stochastic_hill_climb(fun, start, step=1, iteration=50)
    print(f"Maximum found at x = {result}, f(x) = {fun(result)}")

    # Show graph after the step-by-step output.
    li = np.arange(-10, 10, 0.1)
    plt.plot(li, fun(li))
    plt.grid()
    plt.show()
