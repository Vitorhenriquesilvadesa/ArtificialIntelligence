import random
import matplotlib.pyplot as plt

items = {
    7: 15,  # Corda de alpinismo
    10: 30,  # Lanterna de alta duração
    5: 12,  # Canivete multifunção
    20: 50,  # Kit médico completo
    8: 20,  # Mapa detalhado da ilha
    12: 25,  # Rádio comunicador de longo alcance
    9: 22,  # Barraca resistente a tempestades
    18: 45,  # Saco de dormir térmico
    14: 40,  # Fogareiro e combustível extra
    6: 10,  # Kit de pesca
    2: 5,  # Isqueiro resistente à água
    17: 35,  # Estoque de alimentos desidratados
    11: 28,  # Mochila adicional
    3: 8,  # Apito de emergência
    4: 9,  # Espelho para sinalização
    16: 38,  # Kit de ferramentas básicas
    13: 32,  # Jaqueta térmica
    19: 48,  # Purificador de água portátil
    15: 36,  # Roupas extras para frio extremo
    1: 2,  # Pequena bússola
}

max_weight = 80
optimal_fitness = 300
population_size = 1000
history = []


class Individual:
    def __init__(self, genes=None):
        self.genes = (
            genes if genes else [random.randint(0, 1) for _ in range(len(items))]
        )
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

for i in range(1000):
    best_individual = max(population, key=lambda ind: ind.fitness)

    sum = 0
    for individual in population:
        sum += individual.evaluate_fitness()

    history.append(best_individual.evaluate_fitness())

    if best_individual.fitness / optimal_fitness > current_best_coeff:
        current_best_coeff = best_individual.fitness / optimal_fitness
        current_best_genes = best_individual.genes
        current_best_fit = best_individual.evaluate_fitness()

    print(
        f"\rGeração {generation}: Melhor fitness: {int(current_best_fit)} | [Genes: {best_individual.genes} | Avaliação percentual: {(current_best_coeff * 100):.1f}%]"
    )

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

print(
    f"\nMelhor solução encontrada: {current_best_genes}, Best fit: {current_best_fit}"
)

plt.scatter(range(len(history)), history, color="blue", alpha=0.6, s=5)
plt.title("Evolução do Fitness ao Longo das Gerações")
plt.xlabel("Geração")
plt.ylabel("Melhor Fitness da Geração")
plt.grid(True)
plt.show()
