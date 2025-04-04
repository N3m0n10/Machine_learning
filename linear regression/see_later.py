# NEMO RAMOS LOPES NETO
import numpy as np
import matplotlib.pyplot as plt
import mplcursors

def f_true ( x ) :
    return 2 + 0.8 * x

# conjunto de dados {( x , y ) }
xs = np . linspace ( -3 , 3 , 100)
ys = np . array ( [ f_true ( x ) + np . random . randn () *0.5 for x in xs ] )

tht = np.array([np.random.randint(20),np.random.randint(20)]) #or random
a = 0.01 # learning rate
epochs = 5000 # iterations 
m = len(ys) # len(data)
factor = a/m 

'''Hyphotesis'''
def h (x , theta ) :
    return theta[0] + x*theta[1]

'''Cost function'''
def J ( sum) :  # TODO: for plot
    return sum/(2*m) 

def gradient (i , theta , xs , ys ) :
    grad_0 = h(xs[i],theta) - ys[i]
    grad_1 = grad_0*xs[i]
    return np.array([grad_0,grad_1])

''' plota no mesmo grafico : - o modelo / hipotese ( reta )
    - a reta original ( true function )
    - e os dados com ruido ( xs , ys )'''

def print_modelo ( theta , xs , ys ,cost) :
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 5))
    ax1.plot(cost, 'b-')
    ax1.set_title("Loss funtion per iteration")
    ax1.set_xlabel("Iteratons")
    ax1.set_ylabel("Error")

    scatter = ax2.scatter(xs, ys, color='blue', label='Data points',s = 1.5)  # Plot data points
    y_pred = [h(x, theta) for x in xs]  # Generate predictions
    y_true = [f_true(x) for x in xs]    # Generate true function
    ax2.plot(xs, y_pred, 'r-', label='Model')  # Plot model line
    ax2.plot(xs, y_true, 'g--', label='True function')  # Plot true function
    ax2.legend()
    ax2.set_title("Linear Regression")
    
    cursor = mplcursors.cursor(scatter, hover=True)
    @cursor.connect("add")
    def on_hover(sel):
        # Get the x,y coordinates of the selected point
        x_val = sel.target[0]
        y_val = sel.target[1]
        # Find the closest point in our data
        idx = np.abs(xs - x_val).argmin()
        sel.annotation.set_text(f'x: {xs[idx]:.2f}\ny: {ys[idx]:.2f}')
    
    
    plt.show()


loss_list = []
for _ in range(epochs):
    grad_sum = np.zeros(2)
    loss = 0
    ## calculate new gradient and loss
    for j in range(m):
        grad = gradient(j,tht,xs,ys)
        grad_sum += grad
        loss += grad[0]**2

    loss = J(loss)
    ## calculate new theta
    tht = tht - factor*grad_sum
    ## check loss function
    loss_list.append(loss)
    ## append values for plot - > loss func for epoch 

print_modelo(tht,xs,ys,loss_list)                           