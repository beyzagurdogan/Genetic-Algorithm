import matplotlib.pyplot as plt
import numpy as np


# Şehirleri birleştirerek TSP çözüm yolunu görselleştirir.
def plot_solution(cities, solution, best_fitness):
    solution_coords = cities[solution][:, 1:]
    solution_coords = np.vstack((solution_coords, solution_coords[0]))  # Tur tamamla
    plt.plot(solution_coords[:, 0], solution_coords[:, 1], '-o')

    # Başlığın üst kısmına Best Fitness ekle
    plt.title(f"TSP Solution\nBest Fitness (Distance): {best_fitness:.2f}")

    plt.xlabel("X Coordinate")
    plt.ylabel("Y Coordinate")
    plt.show()


# Genetik algoritma boyunca fitness değerinin (toplam mesafe) nasıl geliştiğini gösterir.
def plot_progress(progress):
    plt.plot(progress)
    plt.title("Fitness Progress Over Epochs")
    plt.xlabel("Epoch")
    plt.ylabel("Fitness (Distance)")
    plt.show()

