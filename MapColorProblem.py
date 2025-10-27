# In this Problem we have a Map with 6 different states and 3 Colors red,green and blue.
# We want color our map using these 5 Colors and the important thing is, neighbouring States should have a different
# Color and we have to use minimum colors.

# To solve this Problem, I will represent an Array, that includes 6 Elements. Index corresponds to a specific State
# and the value is the Color of that state.

# ["A" , "B" , "C" , "D" , "E" , "F"] -> ["red" ,"green "blue"]

import random

# Population Size will be the amount of possible solution.
POPULATION_SIZE = 100
# Genome length will be 6, because we have 6 States.
GENOME_LENGTH = 6
# Mutation Rate checks the probability to mutate colors.
MUTATION_RATE = 0.10
# Crossover rate to produce a child from two parents.
CROSSOVER_RATE = 0.7
# Generations to see how this algorithm evolves with the time.
GENERATION_SIZE = 200


# generate_genome(genome_length) will generate a genome with a length based on the passed in length value.
def generate_genome(genome_length: int):
    if genome_length > 0:
        possible_solution = []
        for i in range(genome_length):
            # So in my solution,I want to have different colors. I will use a random number to generate a Color based
            # on the generated random value.
            color_value = random.randint(1, 15)
            if 1 <= color_value < 5:
                possible_solution.append("red")
            elif 5 <= color_value < 10:
                possible_solution.append("blue")
            else:
                possible_solution.append("green")
        return possible_solution
    return "Genome Length should be greater than 0"


# init_population(population_size, genome_length) will generate a population of solution according to the passed in
# population size and every solution will have genome with a length of the passed in genome length size.
def init_population(population_size: int, genome_length: int):
    if population_size > 0 and genome_length > 0:
        population = []
        for i in range(population_size):
            population.append(generate_genome(genome_length))
        return population
    return "Population Size and Genome Length should be greater than 0"


# fitness() will check about the value of each solution
def fitness(genome):
    violations = 0
    genome_length = len(genome)
    if genome[0] == genome[1] or genome[0] == genome[2]:
        violations += 1
    if genome[1] == genome[0] or genome[1] == genome[2] or genome[1] == genome[3]:
        violations += 1
    if genome[2] == genome[0] or genome[2] == genome[1] or genome[2] == genome[3]:
        violations += 1
    if genome[3] == genome[1] or genome[3] == genome[2] or genome[3] == genome[4]:
        violations += 1
    if genome[4] == genome[3]:
        violations += 1
    return violations


# The select_parent() will select a parent with higher fitness value from the population
def select_parent(population, fitness_value):
    fitness_values = [1 / (1 + v) for v in fitness_value]
    total_fitness = sum(fitness_values)
    pick = random.uniform(0, total_fitness)
    current = 0
    for individual, fit_value in zip(population, fitness_values):
        current += fit_value
        if current >= pick:
            return individual
    return population[0]


# The crossover(parent_one,parent_two) will combine two solutions with each other to produce two new solutions
def crossover(parent_one, parent_two):
    if random.random() < CROSSOVER_RATE:
        # define a point to slice the parents
        crossover_point = random.randint(1, len(parent_one) - 1)
        child_one = parent_one[:crossover_point] + parent_two[crossover_point:]
        child_two = parent_two[:crossover_point] + parent_one[crossover_point:]
        return child_one, child_two
    else:
        return parent_one[:], parent_two[:]


# The mutate() will mutate a given solution, in our case based on a random value, the color value will be changed
def mutate(genome):
    for i in range(len(genome)):
        if random.random() < MUTATION_RATE:
            color_value = random.randint(1, 15)
            if 1 <= color_value < 5:
                genome[i] = "red"
            elif 5 <= color_value < 10:
                genome[i] = "blue"
            else:
                genome[i] = "green"
    return genome


# Lastly, we can create our genetic_algoritm() by combining above implemented functions
def genetic_algorithem():
    # Define the Initial Population
    population = init_population(POPULATION_SIZE, GENOME_LENGTH)
    # The best fitness value should be 0
    min_fitness_value = 0

    for generation in range(GENERATION_SIZE):
        # Calculate the fitness values in each generation
        fitness_values = [fitness(genome) for genome in population]

        # Now we can check if we have found the value that matches to our best fitness value
        if min_fitness_value in fitness_values:
            best_index = fitness_values.index(min_fitness_value)
            best_solution = population[best_index]
            print(
                f"The best possible Solution: A = {best_solution[0]}, B = {best_solution[1]}, C = {best_solution[2]}, D = {best_solution[3]}, E = {best_solution[4]}, F = {best_solution[5]}")
            return best_solution

        # If we were not able to find the best solution, then we have to create a new Generation
        new_population = []

        for _ in range(POPULATION_SIZE // 2):
            # Select two Parents from our population, in our case choose two Color Solution
            parent_one = select_parent(population, fitness_values)
            parent_two = select_parent(population, fitness_values)

            # Perform a Cross-Over to produce two children, in our case split and combine two Color Solutions
            child_one, child_two = crossover(parent_one, parent_two)

            # Mutate the newly produced children, in our case changing the Colors and add them to the new population
            new_population.extend([mutate(child_one), mutate(child_two)])

        population = new_population

    print("No Solution has been found")


for i in range(1, 100):
    genetic_algorithem()
