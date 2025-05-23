## save thetas and result to a txt file
from utils import J,j, gradient_descent, forward_prop, backward_prop, sigmoid,\
    gradient_validation, bin_logistic_error, gradient_for_op_minimize, gradient_descent_for_grad_check
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy import optimize
import os

## TODO: separate training and test data

## logistic regression
## cross entropy error
## 2 hidden (for now)
## hypostesis will change the layer number

# tesing and validation
# cross validation

init_epsilon = 1e-2
epochs = 5000
lbd = 0.00001

current_dir = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(current_dir, "classification2.txt")

try:
    with open(data_path, "r") as input_file:
        training_data = input_file.readlines()
except FileNotFoundError:
    print(f"Error: Could not find {data_path}")
    print(f"Current working directory: {os.getcwd()}")
training_data = [line.strip().split(",") for line in training_data]
#np.random.shuffle(training_data)
input_data = np.array([[float(data[0]), float(data[1])] for data in training_data])
input_data_1 = np.array([[float(data[0])] for data in training_data])
input_data_2 = np.array([[ float(data[1])] for data in training_data])
mm1 = [min(input_data_1), max(input_data_1)]
mm2 = [min(input_data_2), max(input_data_2)]
rang_1 , rang_2 = mm1[1] - mm1[0] , mm2[1] - mm2[0]
reg_data = [[a[0]/rang_1,a[1]/rang_2] for a in input_data]
X = input_data
#X = reg_data
Y = np.array([float(data[2]) for data in training_data], dtype=np.float32).reshape(-1, 1)

M = len(X)

#provisory  ##bias added  
def xavier_init(n_out, n_in):
    return np.random.randn(n_out, n_in) * np.sqrt(1.0 / n_in)

shapes = [(10, 3), (7, 11), (1, 8)]
theta0 = xavier_init(shapes[0][0],shapes[0][1])  
theta1 = xavier_init(shapes[1][0],shapes[1][1])
theta2 = xavier_init(shapes[2][0],shapes[2][1])  

W = [theta0, theta1, theta2]
n_layers = len(W) + 1

# gradient validation 
theta = np.concatenate([w.flatten() for w in W])
initial_theta = np.hstack(theta)  
#print("theta:", theta)
analytical_grad = gradient_for_op_minimize(theta, X, Y,shapes,lbd = 0)
#analytical_grad = gradient_descent_for_grad_check(X, Y, W, lbd=lbd)
numerical_grad = gradient_validation(theta, X, Y,shapes)
## do flaten and hstack for gradient
analytical_grad = np.concatenate([w.flatten() for w in analytical_grad])
print("numerical_grad:", numerical_grad)
print("analytical_grad:", analytical_grad)
print("diff:", np.linalg.norm(analytical_grad - numerical_grad))
for i, (a, n) in enumerate(zip(analytical_grad,numerical_grad)):
    print(f"Layer {i} diff:", np.abs(a - n).mean(), np.max(np.abs(a - n)))
if sum(np.abs(analytical_grad - numerical_grad))/len(theta) < 1e-2:
    print("Gradient check passed")
else:
    print("gradient_check_failed")
    raise ValueError("gradient is wrong!")
#raise ValueError("Gradient check done")


result = optimize.minimize(fun=J, jac=gradient_for_op_minimize,\
                x0=initial_theta, method='TNC', args=(X, Y,shapes,lbd), options={'maxiter': 50000, 'disp': True})
print(result)
if result.success:
    final_loss = result.fun
    print("Optimization successful!")
    print("Final loss:", final_loss)
else:
    print("Optimization failed:", result.message)

sizes = [np.prod(shape) for shape in shapes]
split_points = np.cumsum([0] + sizes)
reshaped_W = [
    result.x[split_points[i]:split_points[i+1]].reshape(shapes[i])
    for i in range(len(shapes))
]

acc = 0
for i in range(len(X)):
    if Y[i] == np.round(forward_prop(X[i], reshaped_W, n_layers)[0][-1]): acc+=1
acc = acc / len(X)
print("acc: ",acc)

    

for i in range(len(X)):
    print(f"X: {X[i]}, Y: {Y[i]}, prediction: {np.round(forward_prop(X[i], reshaped_W, n_layers)[0][-1])}")
## remove round for seeing true results
print("accuracy:", acc)

save = input("save data y/n: \t")
print(save.lower())
if save.lower() == "y":
    with open("Neural_networks/Project_1/saved_weights.txt", "a+") as f:
        f.seek(0)  # Go to start of file
        old = f.read()  # Read existing content
        f.seek(0)  # Go back to start
        f.truncate()  # Clear the file
        final_loss = result.fun
        weights = f"Final weights: {reshaped_W}\n"
        text = (
            "##############################"
            f"{shapes}"
            f"{acc}"
            f"{final_loss}"
        )
        f.write(old + weights)