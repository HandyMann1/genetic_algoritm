import math

import random


class Chromosome:
    def __init__(self, index_num: int, bounds: tuple[float, float]):
        self.GENE_NUMBER: int = 2
        self.gene_1: float = 0.0
        self.gene_2: float = 0.0
        self.gene_1_bin: list[int] = []
        self.gene_2_bin: list[int] = []
        self.lower_bound, self.upper_bound = self.set_bounds(bounds)
        self.result: float = math.inf
        self.index_num = index_num
        self.max_bin_size = 1
        self.get_max_min()

    def generate_random_genes_bin(self):
        for _ in range(self.max_bin_size):
            self.gene_1_bin.append(random.randint(0, 1))
            self.gene_2_bin.append(random.randint(0, 1))
        self.evaluate()

    def set_bounds(self, bounds: tuple[float, float]):
        return bounds[0], bounds[1]

    def generate_random_genes(self):
        self.gene_1 = random.uniform(self.lower_bound, self.upper_bound)
        self.gene_2 = random.uniform(self.lower_bound, self.upper_bound)
        self.evaluate()

    def evaluate(self):
        self.result = (-12) * self.gene_2 + 4 * pow(self.gene_1, 2) + 4 * pow(self.gene_2,
                                                                              2) - 4 * self.gene_1 * self.gene_2

    def get_max_min(self):
        max_number: int = int(max(abs(self.lower_bound), abs(self.upper_bound)))
        self.max_bin_size = len(bin(max_number)[2:])


def genetic_algorithm(chromosomes_number: int, bounds: tuple[float, float], mutation_chance: int,
                      crossover_chance: int, generations_number: int, previous_population=None,
                      crossingover_type="basic"):
    if previous_population is None:
        chromosomes_list = generate_first_population(chromosomes_number, bounds)
    else:
        chromosomes_list = previous_population

    best_eval, best_genes = math.inf, (math.inf, math.inf)
    for generation in range(generations_number):
        scores = get_scores(chromosomes_list)
        for j in range(chromosomes_number):
            if scores[j] < best_eval:
                best_eval = scores[j]
                best_genes = (chromosomes_list[j].gene_1, chromosomes_list[j].gene_2)
                print(
                    f"New best evaluation! in generation number {generation} function evaluation {best_eval + 12}"
                    f" with genes {best_genes}")

        selected = [selection(chromosomes_list, scores) for _ in range(chromosomes_number)]
        children = []
        for k in range(0, chromosomes_number, 2):
            parent_1 = selected[k]
            parent_2 = selected[k + 1] if k + 1 < chromosomes_number else parent_1
            if crossingover_type == "basic":
                for child in crossingover(parent_1, parent_2, crossover_chance):
                    child.gene_1 = mutation(mutation_chance, bounds, child.gene_1)
                    child.gene_2 = mutation(mutation_chance, bounds, child.gene_2)
                    child.evaluate()
                    children.append(child)
            else:
                for child in inter_crossingover(parent_1, parent_2, crossover_chance):
                    child.gene_1 = mutation(mutation_chance, bounds, child.gene_1)
                    child.gene_2 = mutation(mutation_chance, bounds, child.gene_2)
                    child.evaluate()
                    children.append(child)
        chromosomes_list = children
    return chromosomes_list, best_genes, best_eval


def genetic_algorithm_binary(chromosomes_number: int, bounds: tuple[float, float], mutation_chance: int,
                             crossover_chance: int, generations_number: int, previous_population=None,
                             crossingover_type="basic"):
    if previous_population is None:
        chromosomes_list = generate_first_population_binary(chromosomes_number, bounds)
    else:
        chromosomes_list = previous_population

    best_eval, best_genes = math.inf, (math.inf, math.inf)

    for generation in range(generations_number):
        scores = get_scores(chromosomes_list)
        for j in range(chromosomes_number):
            if scores[j] < best_eval:
                best_eval = scores[j]
                best_genes = (chromosomes_list[j].gene_1, chromosomes_list[j].gene_2)
                print(
                    f"New best evaluation! in generation number {generation} function evaluation {best_eval + 12}"
                    f" with genes {best_genes}")

        selected = [selection(chromosomes_list, scores) for _ in range(chromosomes_number)]
        children = []

        for k in range(0, chromosomes_number, 2):
            parent_1 = selected[k]
            parent_2 = selected[k + 1] if k + 1 < chromosomes_number else parent_1
            if crossingover_type == "basic":
                for child in bin_crossingover(parent_1, parent_2, crossover_chance):
                    child.gene_1 = decode_binary_to_float(child.gene_1_bin, bounds)
                    child.gene_2 = decode_binary_to_float(child.gene_2_bin, bounds)

                    child.gene_1 = mutation(mutation_chance, bounds, child.gene_1)
                    child.gene_2 = mutation(mutation_chance, bounds, child.gene_2)

                    child.evaluate()
                    children.append(child)
            else:
                for child in bin_two_ptr_crossingover(parent_1, parent_2, crossover_chance):
                    child.gene_1 = decode_binary_to_float(child.gene_1_bin, bounds)
                    child.gene_2 = decode_binary_to_float(child.gene_2_bin, bounds)

                    child.gene_1 = mutation(mutation_chance, bounds, child.gene_1)
                    child.gene_2 = mutation(mutation_chance, bounds, child.gene_2)

                    child.evaluate()
                    children.append(child)
        chromosomes_list = children

    return chromosomes_list, best_genes, best_eval


def decode_binary_to_float(binary_list: list[int], bounds: tuple[float, float]) -> float:
    if not binary_list:
        return bounds[0]
    binary_string = ''.join(map(str, binary_list))
    decimal_value = int(binary_string, 2)
    max_value = (1 << len(binary_list)) - 1
    scaled_value = bounds[0] + (decimal_value / max_value) * (bounds[1] - bounds[0])
    return scaled_value


def generate_first_population(chromosomes_number: int, bounds: tuple[float, float]):
    chromosomes_list = []
    for chromosome_index in range(chromosomes_number):
        chromosome = Chromosome(chromosome_index, bounds)
        chromosome.generate_random_genes()

        chromosomes_list.append(chromosome)
    return chromosomes_list


def generate_first_population_binary(chromosomes_number: int, bounds: tuple[float, float]):
    chromosomes_list = []
    for chromosome_index in range(chromosomes_number):
        chromosome = Chromosome(chromosome_index, bounds)
        chromosome.generate_random_genes_bin()
        chromosomes_list.append(chromosome)
    return chromosomes_list


def get_scores(chromosomes: list):
    scores = []
    for chromosome in chromosomes:
        chromosome.evaluate()
        scores.append(chromosome.result)
    return scores


def selection(chromosomes_list: list, scores: list) -> Chromosome:
    selected_x = random.randint(0, len(chromosomes_list) - 1)
    for _ in range(2):
        competitor_x = random.randint(0, len(chromosomes_list) - 1)
        if scores[competitor_x] < scores[selected_x]:
            selected_x = competitor_x

    return chromosomes_list[selected_x]


def mutation(mutation_chance: int, bounds: tuple, current_value: float):
    if random.random() <= (mutation_chance / 100):
        gene = random.uniform(bounds[0], bounds[1])
        return gene
    return current_value


def crossingover(parent_1: Chromosome, parent_2: Chromosome, crossover_chance: int) -> list:
    if random.random() < crossover_chance / 100:

        ptr = random.randint(1, parent_1.GENE_NUMBER)

        child_1 = Chromosome(parent_1.index_num, (parent_1.lower_bound, parent_1.upper_bound))
        child_2 = Chromosome(parent_2.index_num, (parent_2.lower_bound, parent_2.upper_bound))

        if ptr == 1:
            child_1.gene_1 = parent_1.gene_1
            child_1.gene_2 = parent_2.gene_2
            child_2.gene_1 = parent_2.gene_1
            child_2.gene_2 = parent_1.gene_2
        else:
            child_1.gene_1 = parent_2.gene_1
            child_1.gene_2 = parent_1.gene_2
            child_2.gene_1 = parent_1.gene_1
            child_2.gene_2 = parent_2.gene_2

        return [child_1, child_2]
    else:
        return [parent_1, parent_2]


def bin_crossingover(parent_1: Chromosome, parent_2: Chromosome, crossover_chance: int) -> list:
    if random.random() < crossover_chance / 100:
        ptr = random.randint(1, parent_1.max_bin_size - 1)

        child_1 = Chromosome(parent_1.index_num, (parent_1.lower_bound, parent_1.upper_bound))
        child_2 = Chromosome(parent_2.index_num, (parent_2.lower_bound, parent_2.upper_bound))

        child_1.gene_1_bin = parent_1.gene_1_bin[:ptr] + parent_2.gene_1_bin[ptr:]
        child_1.gene_2_bin = parent_1.gene_2_bin[:ptr] + parent_2.gene_2_bin[ptr:]

        child_2.gene_1_bin = parent_2.gene_1_bin[:ptr] + parent_1.gene_1_bin[ptr:]
        child_2.gene_2_bin = parent_2.gene_2_bin[:ptr] + parent_1.gene_2_bin[ptr:]

        return [child_1, child_2]
    else:
        return [parent_1, parent_2]


# promezhutochniy crossingover
def inter_crossingover(parent_1: Chromosome, parent_2: Chromosome, crossover_chance) -> list:
    if random.random() < crossover_chance / 100:
        child_1 = Chromosome(parent_1.index_num, (parent_1.lower_bound, parent_1.upper_bound))
        child_2 = Chromosome(parent_2.index_num, (parent_2.lower_bound, parent_2.upper_bound))

        alpha = random.uniform(0, 1)
        child_1.gene_1 = alpha * parent_1.gene_1 + (1 - alpha) * parent_2.gene_1
        child_2.gene_1 = (1-alpha) * parent_1.gene_1 + alpha *parent_2.gene_1

        alpha = random.uniform(0, 1)
        child_1.gene_2 = alpha * parent_1.gene_2 + (1 - alpha) * parent_2.gene_2
        child_2.gene_2 = (1 - alpha) * parent_1.gene_2 + alpha * parent_2.gene_2
    else:
        child_1, child_2 = parent_1, parent_2
    return [child_1, child_2]


def bin_two_ptr_crossingover(parent_1: Chromosome, parent_2: Chromosome, crossover_chance: int) -> list:
    if random.random() < crossover_chance / 100:
        size = parent_1.max_bin_size
        point1 = random.randint(0, size - 1)
        point2 = random.randint(0, size - 1)

        if point1 > point2:
            point1, point2 = point2, point1

        child_1 = Chromosome(parent_1.index_num, (parent_1.lower_bound, parent_1.upper_bound))
        child_2 = Chromosome(parent_2.index_num, (parent_1.lower_bound, parent_1.upper_bound))

        child_1.gene_1_bin = (
                parent_1.gene_1_bin[:point1] +
                parent_2.gene_1_bin[point1:point2] +
                parent_1.gene_1_bin[point2:]
        )
        child_1.gene_1_bin = (
                parent_1.gene_2_bin[:point1] +
                parent_2.gene_2_bin[point1:point2] +
                parent_1.gene_2_bin[point2:]
        )
        child_1.evaluate()
        child_2.gene_1_bin = (
                parent_2.gene_1_bin[:point1] +
                parent_1.gene_1_bin[point1:point2] +
                parent_2.gene_1_bin[point2:]
        )
        child_2.gene_2_bin = (
                parent_2.gene_2_bin[:point1] +
                parent_1.gene_2_bin[point1:point2] +
                parent_2.gene_2_bin[point2:]
        )
        child_2.evaluate()
    else:
        child_1 = parent_1
        child_2 = parent_2
    return [child_1, child_2]

# best_val_list = []
# best_genes_2 = 0
# for i in range(10000):
#     _, best_genes, best_val = genetic_algorithm(50, (-10, 10), 10, 60, 100)
#     best_val_list.append(best_val + 12)
#     if best_genes[1] == 2.0:
#         best_genes_2 += 1
# total = 0.0
# for val in best_val_list:
#     total += val
# print(
#     f"the mid value is {total / len(best_val_list)}, the max value is {max(best_val_list)}, the min value is {min(best_val_list)}")
# print(f"the percent of chromosomes with the second gene value that is 2.0: {best_genes_2 / 1000}")
