import random
from copy import deepcopy
from collections import defaultdict
from src.fitness import calculate_fitness
from typing import List

def generate_gene_population(users_df, stations_df, matrix_df, population_size=20):
    matrix_df.columns = matrix_df.columns.str.strip()
    population = []
    user_ids = users_df["user_id"].tolist()
    attempts = 0
    max_attempts = 1000

    while len(population) < population_size and attempts < max_attempts:
        gene = user_ids.copy()
        random.shuffle(gene)
        assignments = assignment_from_gene(gene, stations_df, matrix_df)

        if len(assignments) == len(user_ids):
            score = calculate_fitness(assignments, matrix_df)
            population.append((gene, assignments, score))

        attempts += 1

    if len(population) < population_size:
        print(f" Yalnızca {len(population)} geçerli birey üretildi.")

    return population

def assignment_from_gene(gene, stations_df, matrix_df):
    matrix_df.columns = matrix_df.columns.str.strip()
    assignments = {}
    updated_stations_df = deepcopy(stations_df)

    for user_id in gene:
        user_rows = matrix_df[matrix_df["user_id"] == user_id]
        sorted_rows = user_rows.sort_values(by="distance")

        for _, row in sorted_rows.iterrows():
            station_id = row["station_id"]
            station_row = updated_stations_df[updated_stations_df["station_id"] == station_id]
            if station_row.empty:
                continue

            capacity = int(station_row.iloc[0]["capacity"])
            occupied = int(station_row.iloc[0]["occupied_slots"])

            if occupied < capacity:
                assignments[user_id] = station_id
                updated_stations_df.loc[
                    updated_stations_df["station_id"] == station_id, "occupied_slots"
                ] += 1
                break

    return assignments

def two_point_crossover(parent1, parent2):
    start, end = 20, 40
    length = len(parent1)
    child = [None] * length
    child[start:end+1] = parent1[start:end+1]
    parent2_order = parent2[end+1:] + parent2[:end+1]
    insert_pos = (end + 1) % length

    for gene in parent2_order:
        if gene not in child:
            child[insert_pos] = int(gene)
            insert_pos = (insert_pos + 1) % length

    return child

def mutate_gene(gene, mutation_rate=0.2):
    if random.random() < mutation_rate:
        mutated = deepcopy(gene)
        idx1, idx2 = random.sample(range(len(gene)), 2)
        mutated[idx1], mutated[idx2] = mutated[idx2], mutated[idx1]
        return mutated
    else:
        return deepcopy(gene)

def select_best_genes(gene_population, k=4):
    sorted_population = sorted(gene_population, key=lambda x: x[2])
    return sorted_population[:k]

def is_valid_assignment(assignment, stations_df):
    station_usage = defaultdict(int)
    for user_id, station_id in assignment.items():
        station_usage[station_id] += 1

    for station_id, count in station_usage.items():
        station_row = stations_df[stations_df["station_id"] == station_id]
        if station_row.empty:
            return False
        capacity = int(station_row.iloc[0]["capacity"])
        if count > capacity:
            return False

    return True

def create_next_generation(best_genes, users_df, stations_df, matrix_df, child_count=12, mutation_rate=0.2):
    matrix_df.columns = matrix_df.columns.str.strip()
    next_generation = []
    attempts = 0
    max_attempts = 1000

    while len(next_generation) < child_count and attempts < max_attempts:
        parent1 = random.choice(best_genes)[0]
        parent2 = random.choice(best_genes)[0]

        if parent1 == parent2:
            continue

        print(f"\n‍‍ Ebeveynler: {parent1} & {parent2}")
        child_gene = two_point_crossover(parent1, parent2)
        print(f" Crossover Sonucu: {child_gene}")

        mutated_gene = mutate_gene(child_gene, mutation_rate=mutation_rate)
        print(f" Mutasyon Sonucu: {mutated_gene}")

        assignment = assignment_from_gene(mutated_gene, stations_df, matrix_df)

        if len(assignment) == len(users_df):
            fitness = calculate_fitness(assignment, matrix_df)
            print(f" Yeni Birey Fitness Skoru: {fitness:.2f}")
            next_generation.append((mutated_gene, assignment))

        attempts += 1

    return next_generation


