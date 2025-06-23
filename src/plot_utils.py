import matplotlib.pyplot as plt

def plot_fitness_trend(fitness_history, output_path="logs/fitness_trend.png"):
    plt.figure(figsize=(10, 6))
    plt.plot(fitness_history, marker='o', linestyle='-', color='blue')
    plt.title("Genetik Algoritma - Nesillere Göre En İyi Fitness Değeri")
    plt.xlabel("Nesil")
    plt.ylabel("En İyi Fitness")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()
