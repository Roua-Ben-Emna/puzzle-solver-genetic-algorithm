import random

# Genetic Algorithm  parameters
MUTATION_RATE = 0.25  # Probability of mutation for each chromosome
ELITE_COUNT = 2       # Number of top-performing chromosomes to carry over unchanged
CROSS_RATE = 0.8      # Probability of performing crossover between two parents


# Function to create a randomized chromosome
def create_chromosome(pieces):
    chromosome = pieces[:]
    random.shuffle(chromosome)
    return chromosome

# Fitness function to evaluate how close a chromosome is to the target
def fitness_function(chromosome, target):
    correct_positions = sum(1 for i in range(len(target)) if chromosome[i] == target[i])
    return correct_positions

# Initialize the population with random chromosomes
def initialize_population(pieces, population_size):
    return [create_chromosome(pieces) for _ in range(population_size)]

# Tournament selection to choose parents for crossover
def tournament_selection(population, fitness_scores, k=3):
    tournament = random.sample(list(zip(population, fitness_scores)), k) 
    winner = max(tournament, key=lambda x: x[1])
    return winner[0]

# Perform two-point crossover between two parent chromosomes
def two_point_crossover(parent1, parent2):
    if random.random() < CROSS_RATE:
        size = len(parent1)
        point1, point2 = sorted(random.sample(range(size), 2))
        child1 = parent1[:point1] + parent2[point1:point2] + parent1[point2:]
        child2 = parent2[:point1] + parent1[point1:point2] + parent2[point2:]
    else:
        child1, child2 = parent1[:], parent2[:]
    return child1, child2

# Perform adaptive mutation by swapping two random pieces
def adaptive_mutation(chromosome):
    if random.random() < MUTATION_RATE:
        idx1, idx2 = random.sample(range(len(chromosome)), 2)
        chromosome[idx1], chromosome[idx2] = chromosome[idx2], chromosome[idx1]
    return chromosome

# Main Genetic Algorithm function
def genetic_algorithm(target,pieces, population_size, generations):
    population = initialize_population(pieces, population_size)
    history = []            # Keep track of the evolution process
    stagnation = 0          # Track the number of generations without improvement
    last_best_fitness = -1  # Store the fitness score of the previous generation's best chromosome

    for generation in range(generations):
        fitness_scores = [fitness_function(ind, target) for ind in population]
        # Sort the population by fitness score in descending order
        sorted_population = [population[i] for i in sorted(range(len(fitness_scores)), key=lambda x: fitness_scores[x], reverse=True)]
        next_population = sorted_population[:ELITE_COUNT] # Retain elite chromosomes unchanged

        best_solution = sorted_population[0]
        best_fitness = max(fitness_scores)
        print(f"Generation {generation}: Best Solution = {[target.index(tile) for tile in best_solution]}")
        print(f"Fitness: {best_fitness}")

        # Check for stagnation 
        if best_fitness == last_best_fitness:
            stagnation += 1
        else:
            stagnation = 0
        last_best_fitness = best_fitness

        # Terminate early if stagnation persists
        if stagnation > 20:
            print("Stagnation detected. Terminating early.")
            return "stagnation", history 
        # Save generation data for visualization
        history.append((generation, best_solution, best_fitness))

        if best_fitness >= len(target):
            print("Solution Found!")
            return "solution_found", history 

        # Generate offsprings for the next generation
        offspring_count = population_size - len(next_population)
        for _ in range(offspring_count // 2):
            parent1 = tournament_selection(population, fitness_scores)
            parent2 = tournament_selection(population, fitness_scores)
            child1, child2 = two_point_crossover(parent1, parent2)
            next_population.append(adaptive_mutation(child1))
            next_population.append(adaptive_mutation(child2))

        population = next_population[:population_size] # Update the population for the next generation
        
    # If no solution is found after all generations    
    print("No Solution Found")
    return "no_solution", history 