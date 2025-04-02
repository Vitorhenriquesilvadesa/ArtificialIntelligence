import random

items = {
    1: 2,   2: 10,  3: 8,   4: 5,   5: 3,  
    6: 12,  7: 2,   8: 6,   9: 15,  10: 7,  
    11: 4,  12: 9,  13: 1,  14: 11, 15: 14,
    16: 13, 17: 3,  18: 30,  19: 4,  20: 8, 21: 21, 22: 23, 30: 3, 
}

max_weight = 20
optimal_fitness = 45
population_size = 10000

class Individual:
    def __init__(self, genes=None):
        self.genes = genes if genes else [random.randint(0, 1) for _ in range(len(items))]
        self.fitness = self.evaluate_fitness()

    def evaluate_fitness(self):
        weight, value = 0, 0
        for i, selected in enumerate(self.genes):
            if selected:
                item_weight = list(items.keys())[i]
                item_value = list(items.values())[i]
                weight += item_weight
                value += item_value

        return value if weight <= max_weight else 0

def crossover(parent1, parent2):
    crossover_point = random.randint(1, len(parent1.genes) - 1)
    child_genes = parent1.genes[:crossover_point] + parent2.genes[crossover_point:]
    
    if random.random() < 0.01 / (population_size / 2):  
        mutate_index = random.randint(0, len(child_genes) - 1)
        child_genes[mutate_index] = 1 if child_genes[mutate_index] == 0 else 0
    
    return Individual(child_genes)

def tournament_selection(population):
    return max(random.sample(population, 2), key=lambda ind: ind.fitness)

population = [Individual() for _ in range(population_size)]
generation = 0

current_best_coeff = 0.0
current_best_fit = 0.0
current_best_genes = [0 for _ in range(len(items))]

while 1:
    best_individual = max(population, key=lambda ind: ind.fitness)
    
    if best_individual.fitness / optimal_fitness > current_best_coeff:
        current_best_coeff = best_individual.fitness / optimal_fitness
        current_best_genes = best_individual.genes
        current_best_fit = best_individual.evaluate_fitness()
    
    print(f"\rGeração {generation}: Melhor fitness: {int(current_best_fit)} | [Genes: {best_individual.genes} | Avaliação percentual: {(current_best_coeff * 100):.1f}%]")
    
    if best_individual.fitness >= optimal_fitness:
        break
    
    new_population = []
    for _ in range(len(population)):
        parent1 = tournament_selection(population)
        parent2 = tournament_selection(population)
        child = crossover(parent1, parent2)
        new_population.append(child)
    
    population = new_population
    generation += 1

print(f"\nMelhor solução encontrada: {current_best_genes}, Best fit: {current_best_fit}")