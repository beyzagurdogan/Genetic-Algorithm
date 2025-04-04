from file_parser import load_tsp_file
from distance import compute_distance_matrix
from genetic_algorithm import run_genetic_algorithm
from utils import plot_solution, plot_progress
from animate_solution import animate_genetic_algorithm_3d # Animasyon fonksiyonunu ekliyoruz

if __name__ == "__main__":
    tsp_file = "data/berlin52.tsp"
    cities = load_tsp_file(tsp_file)
    distance_matrix = compute_distance_matrix(cities)
    num_cities = len(cities)

    best_solution, best_fitness, fitness_progress, best_solutions_per_epoch = run_genetic_algorithm(
        distance_matrix, num_cities, population_size=300, epochs=500, mutation_rate=0.001, greedy_fraction=0.9
    )

    print(f"Best Solution: {best_solution}")
    print(f"Best Fitness (Total Distance): {best_fitness:.2f}")

    # Önce çözümü çiziyoruz
    plot_solution(cities, best_solution, best_fitness)
    plot_progress(fitness_progress)

    # Sonra animasyonu başlatıyoruz ve mp4 olarak kaydediyoruz
    animate_genetic_algorithm_3d(cities, best_solution, best_fitness, fitness_progress, best_solutions_per_epoch, interval=500, output_file="tsp_solution_animation.mp4")
