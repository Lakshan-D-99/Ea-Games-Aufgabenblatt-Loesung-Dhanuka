# In the N Queen Problem, we have to check if the Queens has placed in an Order, that they won't get Terminated from
# other Queens.

import random

# Firstly, define a Population Amount -> Population == Possible Solutions
POPULATION_SIZE = 100
# Genome length will define the length of a single solution ( This could be variable )
GENOME_LENGTH = 8  # we can change this board value as we like -> 8 : 8x8
# Mutation Value will decide the probability, that a Mutation can occur. Mutation = Random change of a single Solution
MUTATION_RATE = 0.05
# Crossover Rate will decide the probability, that two solutions producing a new solution
CROSSOVER_RATE = 0.7
# It's also important to test this Algorithm on many Generations
GENERATION_SIZE = 200


# I will use an Array to represent the place of a Queen. Array index is the Column Number and the value of each Index will
# represent the row place of the Queen, in that specific Column.

# generate_solution() function will generate a random solution, and we have to pass board_size value, because based on the
# board_size we can define the size of the rows and the columns
def generate_solution(board_size: int):
    if board_size > 0:
        possible_solution = []
        for i in range(board_size):
            possible_solution.append(random.randint(0, board_size - 1))
        return possible_solution
    return "Board Size can not be Zero"


# init_population() function will define the initial Population with possible Solutions, so that we can the EA on them.
# The board_size is to define the amount of rows and columns
def initial_population(population_size: int, board_size: int):
    if population_size > 0 and board_size > 0:
        population = []
        for i in range(population_size):
            population.append(generate_solution(board_size))
        return population
    return "The Population Size or the Board Size should be greater than 0"


# Now we need to define a fitness Function, based on the fitness function we can decide, which Solutions are better.
# Inside the fitness function, we have to count the amount of non-attacking pair of queens.
def fitness(solution):
    conflict_count = 0  # Conflict count will store the amount of Queen pairs attacking each other
    queen_count = len(solution)  # This will store the number of Queens
    for i in range(queen_count):
        for j in range(i + 1, queen_count):
            # First, we check if two Queens are in the same column or not
            if solution[i] == solution[j]:
                conflict_count += 1
            # Secondly, we check if two Queens attack each other diagonally
            if abs(solution[i] - solution[j]) == abs(i - j):
                conflict_count += 1

    max_pairs = queen_count * (queen_count - 1) // 2
    return max_pairs - conflict_count


# The following select_parent() will select a parent for crossover. We will use the Roulette Wheel Method to select a parent.
# In the Roulette wheel we will use a weight based approach and the weight will be the sum of total_fitness
def select_parent(population, fitness_values):
    total_fitness = sum(fitness_values)
    # Now we have to randomly pick a value from the total fitness
    pick = random.uniform(0, total_fitness)
    current = 0
    for i, fit_value in zip(population, fitness_values):
        current += fit_value
        if current >= pick:
            return i
    return population[0]


# The crossover() will combine two parents to create two children.In our case two solutions, where a less amount of Queens attacking
# each-other
def crossover(parent_one, parent_two):
    # We want a Crossover to happen with a specific probability
    if random.random() < CROSSOVER_RATE:
        # Define a specific Point to cross the both parents
        crossover_point = random.randint(1, len(parent_one) - 1)
        child_one = parent_one[:crossover_point] + parent_two[crossover_point:]
        child_two = parent_two[:crossover_point] + parent_one[crossover_point:]
        return child_one, child_two
    else:
        return parent_one[:], parent_two[:]


# The mutate() will mutate a solution, in our case change the position of a Queen in the column
def mutate(solution):
    for i in range(len(solution)):
        if random.random() < MUTATION_RATE:
            solution[i] = random.randint(0, len(solution) - 1)
    return solution


# Lastly, combine all the above implemented functions to create the genetic algorithm function
def genetic_algorithm():
    population = initial_population(POPULATION_SIZE, GENOME_LENGTH)
    # Based on the Size of our board, we can calculate the maximum amount of pairs, that a pair of Queens not attacking each-other
    max_fitness_value = GENOME_LENGTH * (GENOME_LENGTH - 1) // 2

    # We want to loop through all the Generations, so that we can identify a good solution
    for generation in range(GENERATION_SIZE):
        # Calculate all the fitness values in all the solutions in a Generation
        fitness_values = [fitness(solution) for solution in population]

        print(f"Generation {generation}: Best Fitness = {max(fitness_values)}")

        # If we find any Solution, that has the maximum fitness value, then we have our solution
        if max_fitness_value in fitness_values:
            best_index = fitness_values.index(max_fitness_value)
            best_solution = population[best_index]
            print(f"Solution found in the Generation:{generation} and Solution:{best_solution} with the fitness value:{max_fitness_value}")
            return best_solution

        # If we couldn't find a perfect Solution, then we have to evolve the Generation to find a perfect Solution
        new_population = []

        for _ in range(POPULATION_SIZE // 2):
            # Select two Parents from our population, in our case choose two columns
            parent_one = select_parent(population, fitness_values)
            parent_two = select_parent(population, fitness_values)

            # Perform a Cross-Over to produce two children, in our case split and combine two columns
            child_one, child_two = crossover(parent_one, parent_two)

            # Mutate the newly produced children, in our case changing the Queens places and add them to the new population
            new_population.extend([mutate(child_one), mutate(child_two)])

            population = new_population

    # If we can not find a perfect Solution, we can just return the best found solution
    fitness_values = [fitness(solution) for solution in population]
    best_index = fitness_values.index(max(fitness_values))
    best_solution = population[best_index]
    print(f"A Perfect Solution could not be found, the best found solution : {best_solution} and the fitness value:{best_index}")
    return best_solution


# Call the genetic algorithm function
for i in range(1,100):
    genetic_algorithm()
