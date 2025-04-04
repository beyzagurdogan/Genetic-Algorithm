import numpy as np


# iki şehir arasındaki mesafeyi ölçer
def calculate_distance(city1, city2):
    return np.sqrt((city1[1] - city2[1]) ** 2 + (city1[2] - city2[2]) ** 2)


# tüm şehirler için birbirleri arasındaki mesafeleri hesaplar ve bir mesafe matrisi döndürür.
def compute_distance_matrix(cities):
    num_cities = len(cities)
    dist_matrix = np.zeros((num_cities, num_cities))
    for i in range(num_cities):
        for j in range(num_cities):
            if i != j:
                dist_matrix[i, j] = calculate_distance(cities[i], cities[j])
    return dist_matrix
