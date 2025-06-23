import pandas as pd
import sys
import matplotlib.pyplot as plt
from src.fitness import calculate_fitness
from src.visualize import visualize_final_assignment
from src.genetic import (
    generate_gene_population,
    select_best_genes,
    create_next_generation,
    assignment_from_gene
)
from src.plot_utils import plot_fitness_trend

if __name__ == "__main__":
    population_size = 20
    num_generations = 1000
    mutation_rate= 0.4
    elite_count = 6
    child_count = 14
    patience = 20 

    # Yeni verileri yükle
    users_df = pd.read_csv("data/users.csv")
    stations_df = pd.read_csv("data/stations.csv")
    user_station_matrix_df = pd.read_csv("data/user_station_matrix.csv")
    user_station_matrix_df.columns = user_station_matrix_df.columns.str.strip()
    user_station_matrix_df["user_id"] = user_station_matrix_df["user_id"].astype(int)

    # Başlangıç popülasyonu
    population = generate_gene_population(users_df, stations_df, user_station_matrix_df, population_size)

    fitness_history = []
    no_improvement_counter = 0
    best_fitness_so_far = float('inf')

    with open("logs/genetic_log.txt", "w", encoding="utf-8") as log_file, \
         open("logs/genetic_summary.txt", "w", encoding="utf-8") as summary_file, \
         open("logs/fitness_values.txt", "w", encoding="utf-8") as fitness_file:

        original_stdout = sys.stdout
        sys.stdout = log_file

        try:
            for generation in range(num_generations):
                print(f"\n================= 🧪 Generation {generation + 1} =================")
                summary_file.write(f"\n================= 🧪 Generation {generation + 1} =================\n")

                # Başlangıç Popülasyonu Yazdır
                print("\n Initial Population:")
                summary_file.write("\n Initial Population:\n")
                for i, (gene, assignment, fitness) in enumerate(population):
                    print(f"Birey {i+1}: Gen = {gene}, Fitness = {fitness}")
                    summary_file.write(f"Individual {i+1}: Gen = {gene}, Fitness = {fitness}\n")
                    print("Atamalar:")
                    for uid in gene:
                        if uid in assignment:
                            print(f"  User {uid} → Station {assignment[uid]}")
                    print("-" * 50)

                # En iyi bireyleri seç
                best_genes = select_best_genes(population, k=elite_count)
                print("\n Selected Individuals:")
                summary_file.write("\n Selected Individuals:\n")
                for i, (gene, assignment, score) in enumerate(best_genes, 1):
                    print(f"Individual {i}: Gen = {gene}, Fitness = {score}")
                    summary_file.write(f"Individual {i}: Gen = {gene}, Fitness = {score}\n")
                    print("-" * 50)

                # Nesil En İyi Fitness Takibi
                best_fitness = best_genes[0][2]
                fitness_history.append(best_fitness)
                fitness_file.write(f"Generation {generation + 1}: {best_fitness}\n")
                print(f" Generation {generation + 1} Best Fitness: {best_fitness}")

                if best_fitness < best_fitness_so_far:
                    best_fitness_so_far = best_fitness
                    no_improvement_counter = 0
                else:
                    no_improvement_counter += 1

                if no_improvement_counter >= patience:
                    print(f"\n Last {patience} generations no improvement. Algorithm is being stopped.")
                    break

                # Yeni bireyler (çocuklar)
                children = create_next_generation(best_genes, users_df, stations_df, user_station_matrix_df, child_count=child_count, mutation_rate=mutation_rate)
                print("\n Children Formed:")
                summary_file.write("\n Children Formed:\n")
                for i, (gene, assignment) in enumerate(children, 1):
                    fitness = calculate_fitness(assignment, user_station_matrix_df)
                    print(f"Children {i}: Gen = {gene}, Fitness = {fitness}")
                    summary_file.write(f"Children {i}: Gen = {gene}, Fitness = {fitness}\n")
                    print("Assigments:")
                    for uid in gene:
                        if uid in assignment:
                            print(f"  User {uid} → Station {assignment[uid]}")
                    print("-" * 50)
                    summary_file.write("-" * 50 + "\n")

                # Yeni popülasyonu oluştur
                new_population = best_genes + [(gene, assignment, calculate_fitness(assignment, user_station_matrix_df)) for gene, assignment in children]

                print("\n New Generation Population:")
                for i, (gene, assignment, fitness) in enumerate(new_population):
                    print(f"Individual {i+1}: Gen = {gene}, Fitness = {fitness}")
                    print("Assigments:")
                    for uid in gene:
                        if uid in assignment:
                            print(f"  User {uid} → Station {assignment[uid]}")
                    print("-" * 50)

                population = new_population

            # Son nesilde en iyi bireyi yazdır
            final_best = select_best_genes(population, k=1)[0]
            print("\n Best Result:")
            print(f"Gen = {final_best[0]}")
            print(f"Fitness = {final_best[2]}")
            summary_file.write("\n Best Result:\n")
            summary_file.write(f"Gen = {final_best[0]}\n")
            summary_file.write(f"Fitness = {final_best[2]}\n")
        finally:
            sys.stdout = original_stdout

    plot_fitness_trend(fitness_history, "logs/fitness_trend.png")
    visualize_final_assignment(final_best[1], users_df, stations_df)




