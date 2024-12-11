import random

# Genetic Algorithm 
MUTATION_RATE = 0.25
ELITE_COUNT = 2
CROSS_RATE = 0.8



def create_chromosome(pieces):
    chromosome = pieces[:]
    random.shuffle(chromosome)
    return chromosome

def fitness_function(chromosome, target):
    correct_positions = sum(1 for i in range(len(target)) if chromosome[i] == target[i])
    return correct_positions

def initialize_population(pieces, population_size):
    return [create_chromosome(pieces) for _ in range(population_size)]

def tournament_selection(population, fitness_scores, k=3):
    tournament = random.sample(list(zip(population, fitness_scores)), k)
    winner = max(tournament, key=lambda x: x[1])
    return winner[0]

def two_point_crossover(parent1, parent2):
    if random.random() < CROSS_RATE:
        size = len(parent1)
        point1, point2 = sorted(random.sample(range(size), 2))
        child1 = parent1[:point1] + parent2[point1:point2] + parent1[point2:]
        child2 = parent2[:point1] + parent1[point1:point2] + parent2[point2:]
    else:
        child1, child2 = parent1[:], parent2[:]
    return child1, child2

def adaptive_mutation(chromosome):
    if random.random() < MUTATION_RATE:
        idx1, idx2 = random.sample(range(len(chromosome)), 2)
        chromosome[idx1], chromosome[idx2] = chromosome[idx2], chromosome[idx1]
    return chromosome

# Genetic Algorithm
def genetic_algorithm(target,pieces, population_size, generations):
    population = initialize_population(pieces, population_size)
    history = []
    stagnation = 0
    last_best_fitness = -1

    for generation in range(generations):
        fitness_scores = [fitness_function(ind, target) for ind in population]
        sorted_population = [population[i] for i in sorted(range(len(fitness_scores)), key=lambda x: fitness_scores[x], reverse=True)]
        next_population = sorted_population[:ELITE_COUNT]

        best_solution = sorted_population[0]
        best_fitness = max(fitness_scores)
        print(f"Generation {generation}: Best Solution = {[target.index(tile) for tile in best_solution]}")
        print(f"Fitness: {best_fitness}")

        if best_fitness == last_best_fitness:
            stagnation += 1
        else:
            stagnation = 0
        last_best_fitness = best_fitness

        if stagnation > 20:
            print("Stagnation detected. Terminating early.")
            return "stagnation", history 
      
        history.append((generation, best_solution, best_fitness))

        if best_fitness >= len(target):
            print("Solution Found!")
            return "solution_found", history 


        offspring_count = population_size - len(next_population)
        for _ in range(offspring_count // 2):
            parent1 = tournament_selection(population, fitness_scores)
            parent2 = tournament_selection(population, fitness_scores)
            child1, child2 = two_point_crossover(parent1, parent2)
            next_population.append(adaptive_mutation(child1))
            next_population.append(adaptive_mutation(child2))

        population = next_population[:population_size]
    print("No Solution Found")
    return "no_solution", history 