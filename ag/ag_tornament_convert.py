##NEMO RAMOS LOPES NETO
import numpy as np
import matplotlib.pyplot as plt
import os
from datetime import datetime

start_tme = os.times()
population_size = 150
mutation_rate = 0.01
pc = 0.9 ##crossover rate
L = 32
iters = 700
version = "0.42 - TOURNAMENT - CONVERTED"
stats = f"population: {population_size}, mutation rate: {mutation_rate}, crossover rate: {pc}"

##create population
def create_population(size):
    return np.random.uniform(0, np.pi, size).tolist()

def get_bits(x):
    """Convert a number between 0 and π to binary string"""

    # Normalize x to be between 0 and 1
    normalized = x / np.pi
    # Convert to integer between 0 and 2^L-1
    int_value = int(normalized * ((2**L) - 1))
    # Convert to binary and remove '0b' prefix
    binary = bin(int_value)[2:]
    # Pad with zeros to reach length L
    return binary.zfill(L)

def get_float(bits):
    """Convert binary string back to number between 0 and π"""
    # Convert binary string to integer
    int_value = int(bits, 2)
    # Convert to value between 0 and 1
    normalized = int_value / ((2**L) - 1)
    # Scale to range [0, π]
    return normalized * np.pi

## x must be >= 0 and < pi
def fitness_function(_chromosome):  #must be a float (pre conditionated)
    if 0 <= _chromosome < np.pi:
        return _chromosome + abs(np.sin(32 * _chromosome)) ##fitness function
    else:
        return 0

# get the fitness of the population
def get_fitness(population):  
    fitness_list = []
    for i in range(len(population)):
        fitness_list.append(fitness_function(population[i]))
    return fitness_list

# do the selection and crossover
def selection(_population):   ##tournament
    fitness_values = get_fitness(_population)
    total_fitness = sum(fitness_values)
    global population_size
    global average_fitness
    average_fitness = total_fitness/len(_population)
    couple = []
    for i in range(2):
        indexes = [np.random.choice(population_size - 1),np.random.choice(population_size -1)]
        if fitness_values[indexes[0]] > \
           fitness_values[indexes[1]]:
            selected = 0 
        else:
            selected = 1
        couple.append(_population[indexes[selected]])
    return couple[0], couple[1]

def crossover(crom1, crom2): 
    global pc
    global mutation_rate
    if np.random.rand() < pc:
        locus = np.random.randint(0, L)
        child1 = crom1[:locus] + crom2[locus:]
        child2 = crom2[:locus] + crom1[locus:]
    else:
        child1, child2 = crom1, crom2

    child1 = mutation(child1)
    child2 = mutation(child2)

    return child1, child2

def mutation(crom1):   
    for i in range(L):
        if np.random.rand() < mutation_rate:
            crom1 = crom1[:i] + str(1 - int(crom1[i])) + crom1[i+1:]
    return crom1


average_fitness = 0
population = create_population(population_size)
plot_points = [] 
plot_points.append(population.copy())
appt_list = []
best_fitness = []  
for q in range(iters):
    try:
        population = new_population.copy()
    except:
        pass
    all_fitness = get_fitness(population)
    appt_list.append(average_fitness)
    new_population = []
    for i in range(population_size//2):
        crom1, crom2 = selection(population)
        crom1_bits, crom2_bits = get_bits(crom1), get_bits(crom2)
        child1, child2 = crossover(crom1_bits, crom2_bits)
        float_child_1 , float_child_2 = get_float(child1), get_float(child2)
        new_population.append(float_child_1)
        new_population.append(float_child_2)
    if q == iters//2 - 1:
        plot_points.append(new_population.copy())  ##plt
    ####STRICT CONVERGION
    current_best = max(get_fitness(population))
    best_fitness.append(current_best)
    try:
        converged_at
    except:
        if len(best_fitness) > 50 and len(set(best_fitness[-50:])) == 1:  ##set exlude equals
            converged_at = f"Converged at generation {q}"

finish_time = os.times()[4]-start_tme[4]
print("time in seconds:{:.2f}".format(finish_time))  ##time for finish ag f"{os.times()[4]-start_tme[4]):.2f}
plot_points.append(new_population.copy())
fitness_of_points = []

# LOG
try:
    converged_at
except:
    converged_at = "Nan"
with open("ag/log.txt",'a+') as log:
    log.seek(0)  # Go to start of file
    old = log.read()  # Read existing content
    log.seek(0)  # Go back to start
    log.truncate()  # Clear the file
    timestamp = datetime.now().strftime("%d/%m/%Y %H:%M")
    
    # Format the new entry with proper indentation
    new_entry = (
        "====================================\n"
        f"TIMESTAMP: {timestamp}\n"
        f"VERSION: {version}\n"
        f"Converged at generation: {converged_at}\n"
        f"Finish time: {finish_time:.2f} s\n"
        f"Stats: {stats}\n"
        "====================================\n"
    )
    
    # Write new entry followed by old content
    log.write(new_entry + old)


# Plotting section
x = np.linspace(0, np.pi, 500)
y = [fitness_function(xi) for xi in x]

# Create figure with 2x2 subplots
fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(12, 10))

# First subplot (top-left) - Average Fitness Evolution
ax1.plot(appt_list,label = f"final Average fitness: {average_fitness:.3f}")
ax1.set_title(f'Average Fitness Evolution  - {version}')
ax1.set_xlabel('Generation')
ax1.set_ylabel('Fitness')
ax1.legend()
ax1.grid(True)

labels = ["Initial Population", "Middle Population", "Final Population"]
colors = ["bo", "yo", "ro"]  # blue, yellow, red

# Other subplots - Population Distribution at different stages
for idx, (ax, label, color) in enumerate(zip([ax2, ax3, ax4], labels, colors)):
    # Plot fitness function
    ax.plot(x, y, 'g-', label="Fitness Function")
    # Plot population points
    ax.plot(plot_points[idx], 
            [fitness_function(xi) for xi in plot_points[idx]],
            color, 
            label=label)
    
    ax.set_title(f'Population Distribution - {label}')
    ax.set_xlabel('Input value')
    ax.set_ylabel('Fitness')
    ax.set_xlim(0, np.pi)
    ax.legend()
    ax.grid(True)

plt.tight_layout()
plt.show()