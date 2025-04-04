import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.animation as animation

def animate_genetic_algorithm_3d(cities, best_solution, best_fitness, fitness_progress, best_solutions_per_epoch, interval=500, output_file="tsp_solution_animation_3d.mp4"):
    # Şehir koordinatlarını alıyoruz (X, Y)
    city_coords = cities[:, 1:]

    # 3D figür ve eksen oluşturuyoruz
    fig = plt.figure(figsize=(12, 12))
    ax = fig.add_subplot(111, projection='3d')

    # Arka plan rengini siyah yapıyoruz
    ax.set_facecolor('black')

    # Z koordinatını sıfır yapıyoruz
    city_coords = np.hstack((city_coords, np.zeros((city_coords.shape[0], 1))))  # Z'yi sıfırla ekliyoruz

    # Şehirleri beyaz noktalarla çiziyoruz
    ax.scatter(city_coords[:, 0], city_coords[:, 1], city_coords[:, 2], c='w', s=40)  # Beyaz renkli noktalar

    # Fitness bilgisini ekliyoruz
    fitness_text = ax.text2D(0.05, 0.95, f"Best Fitness: {best_fitness:.2f}", transform=ax.transAxes, fontsize=12, verticalalignment="bottom", color='white')

    # Harita sınırlarını ayarlıyoruz (X, Y, Z eksen sınırları)
    ax.set_xlim(city_coords[:, 0].min() - 10, city_coords[:, 0].max() + 10)
    ax.set_ylim(city_coords[:, 1].min() - 10, city_coords[:, 1].max() + 10)
    ax.set_zlim(city_coords[:, 2].min() - 10, city_coords[:, 2].max() + 10)

    # Grafik eksen numaralarını kaldırıyoruz
    ax.set_xticks([])  # X eksenindeki sayıları kaldırıyoruz
    ax.set_yticks([])  # Y eksenindeki sayıları kaldırıyoruz
    ax.set_zticks([])  # Z eksenindeki sayıları kaldırıyoruz

    # Başlangıçta çizgiyi oluşturalım
    line, = ax.plot([], [], [], 'w-', lw=2)  # Beyaz çizgi

    # Animasyon güncelleme fonksiyonu
    def update(frame):
        # Genetik algoritmadan gelen epoch çözümünü alıyoruz
        current_solution = best_solutions_per_epoch[frame]
        current_solution_coords = city_coords[current_solution]
        current_solution_coords = np.vstack((current_solution_coords, current_solution_coords[0]))  # Çizgiyi tamamlıyoruz

        # Çizgiyi güncelliyoruz
        line.set_data(current_solution_coords[:, 0], current_solution_coords[:, 1])
        line.set_3d_properties(current_solution_coords[:, 2])

        # Fitness değerini güncelliyoruz
        fitness_text.set_text(f"Best Fitness: {fitness_progress[frame]:.2f} (Epoch: {frame + 1})")

        return line, fitness_text

    # Animasyonu oluşturuyoruz
    ani = animation.FuncAnimation(fig, update, frames=len(best_solutions_per_epoch), interval=interval, repeat=False)

    # Animasyonu mp4 olarak kaydediyoruz
    ani.save(output_file, writer="ffmpeg", fps=30)

    # Görselleştirmeyi gösteriyoruz
    plt.show()
