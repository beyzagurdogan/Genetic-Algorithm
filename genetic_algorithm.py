import random
import numpy as np


# Fitness Calculation
def calculate_fitness(solution, distance_matrix):
    total_distance = sum(  # Tüm bu mesafeleri toplar.
        distance_matrix[solution[i - 1], solution[i]] for i in range(len(solution))
        # Bu iki şehir arasındaki mesafeyi alır.
    )
    total_distance += distance_matrix[
        solution[-1], solution[0]]  # son şehrinden tekrar başlangıç şehrine dönüş mesafesini ekleme
    return total_distance


# Solution and Population Generation
def generate_random_solution(num_cities):  # Toplam şehir sayısını belirtir.
    solution = list(range(num_cities))  # Şehirleri temsil eden bir liste oluşturur
    random.shuffle(solution)  # Listeyi rastgele bir sıraya göre karıştırır
    return solution


def generate_population(num_cities, population_size, distance_matrix, greedy_solution=None, greedy_fraction=0.1):
    population = []
    greedy_count = int(population_size * greedy_fraction)  # Greedy ile oluşturulacak birey sayısı

    for _ in range(greedy_count):
        start_city = random.randint(0, num_cities - 1)
        greedy_sol = greedy_algorithm(start_city, distance_matrix)
        population.append(greedy_sol)

    while len(population) < population_size:
        population.append(generate_random_solution(num_cities))

    return population


def greedy_algorithm(start_city, distance_matrix):  # 5 ŞEHİR VARSA 5X5LİK BİR MATRİS OLUŞTURACAK
    num_cities = len(distance_matrix)
    unvisited = set(range(num_cities))  # Tüm şehirleri buraya ekliyoruz.
    unvisited.remove(start_city)  # Başlangıç şehrini ziyaret edildi olarak işaretliyoruz.
    solution = [start_city]  # Başlangıç şehrini çözüm listesine ekliyoruz.

    while unvisited:  # Ziyaret edilmemiş şehirler varken devam et.
        current_city = solution[-1]  # Şu anda bulunduğumuz şehir
        next_city = min(unvisited, key=lambda city: distance_matrix[current_city, city])  # En yakın şehri buluyoruz.
        solution.append(next_city)  # En yakın şehri çözüm listesine ekliyoruz.
        unvisited.remove(next_city)  # O şehri ziyaret ettik, artık onu gezmeyeceğiz.

    return solution



def tournament_selection(population, distance_matrix, k=12):
    tournament = random.sample(population, k)  # population içinden k kadar rastgele birey sırası seçiyoruz
    fitness_scores = [calculate_fitness(ind, distance_matrix) for ind in
                      tournament]  # Seçilen her bir şehir sırası için fitness hesaplıyoruz
    return tournament[np.argmin(fitness_scores)]  # Fitness skorlarına göre en iyi (en düşük mesafe) bireyi seçiyoruz


def ordered_crossover(parent1, parent2):
    size = len(parent1)  # Ebeveynlerin uzunluğunu alıyoruz.parent1'den belirli bir kesim alacağız.
    start, end = sorted(
        random.sample(range(size), 2))  # iki rastgele sayı seçiyor ve bunları küçükten büyüğe sıralıyoruz

    child = [None] * size  # Çocuğun başlangıçta tüm pozisyonları None (boş) olacak şekilde bir liste oluşturuyoruz.
    child[start:end] = parent1[start:end]  # Ebeveyn 1'den seçilen aralıktaki değerleri çocuğa ekliyoruz.

    # Şimdi parent2'yi kullanarak çocuğun eksik kalan yerlerini dolduracağız.
    pointer = 0  # çocuğun nereye değer koyacağımızı takip ediyor
    for gene in parent2:  # parent2'yi sırayla inceliyoruz
        if gene not in child:  # Eğer gene çocuğun içinde yoksa (tekrarlamamak için)
            while child[pointer] is not None:
                pointer += 1  # pointer'ı arttırıyoruz
            child[pointer] = gene  # Gene'yi çocuğun uygun yerine koyuyoruz
    return child


# random sayı üretti 0 ile 1 arasında. ürettiği sayı 0.1den küçükse(mutasyon rate inden) sayıyı mutasyona uğratacak.
# 2.sayıyı rastgele seçti ve ilk sayı ile ikinci sayının yerini değiştirdi. böylece
def swap_mutation(individual, mutation_rate=0.1):
    for i in range(len(individual)):
        if random.random() < mutation_rate:
            j = random.randint(0, len(individual) - 1)
            individual[i], individual[j] = individual[j], individual[i]
    return individual


def create_new_epoch(population, distance_matrix, mutation_rate=0.1):
    new_population = []
    while len(new_population) < len(population):
        parent1 = tournament_selection(population, distance_matrix)  # Rastgele İki ebeveyn (parent1 ve parent2) seçilir
        parent2 = tournament_selection(population, distance_matrix)  # turnuva yöntemi kullanılarak seçilir. Random yani
        child = ordered_crossover(parent1,
                                  parent2)  # Seçilen iki ebeveynin genetik materyalleri, sıralı çaprazlama (ordered crossover) yöntemi ile birleştirilir
        child = swap_mutation(child,
                              mutation_rate)  # Çaprazlama sonrası oluşan çocuk, swap mutasyonu ile rastgele değişikliklere uğrar.
        new_population.append(child)  # iki ebeveynin genetikleri karıştırılmış ve mutasyona uğramış çocuk oluşur.
    return new_population


def run_genetic_algorithm(distance_matrix, num_cities, population_size=100, epochs=100, mutation_rate=0.1,
                          greedy_fraction=0.1):
    best_solution = None
    best_fitness = float('inf')
    fitness_progress = []
    best_solutions_per_epoch = []

    population = generate_population(num_cities, population_size, distance_matrix, greedy_solution=None,
                                     greedy_fraction=greedy_fraction)

    for epoch in range(epochs):
        population = create_new_epoch(population, distance_matrix, mutation_rate)
        fitness_scores = [calculate_fitness(ind, distance_matrix) for ind in population]
        epoch_best = min(fitness_scores)
        fitness_progress.append(epoch_best)

        if epoch_best < best_fitness:
            best_fitness = epoch_best
            best_solution = population[np.argmin(fitness_scores)]

        best_solutions_per_epoch.append(population[np.argmin(fitness_scores)])  # Her epoch'taki en iyi çözümü sakla

        print(f"Epoch {epoch + 1}: Best Fitness = {epoch_best:.2f}")

    return best_solution, best_fitness, fitness_progress, best_solutions_per_epoch
