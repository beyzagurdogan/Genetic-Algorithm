import numpy as np


def load_tsp_file(file_path):
    cities = []
    with open(file_path, 'r') as file:
        lines = file.readlines()
        node_section = False  # `NODE_COORD_SECTION` kontrolü için bayrak

        for line in lines:
            line = line.strip()

            # `NODE_COORD_SECTION` başlığını bulduğunda veri alma kısmını başlat
            if line == "NODE_COORD_SECTION":
                node_section = True
                continue

            # Eğer `NODE_COORD_SECTION` bölümündeysek ve satır boş değilse
            if node_section:
                # `EOF` veya boş satır geldiğinde döngü sonlandırılır
                if line == "EOF" or not line:
                    break

                # Her satırı boşlukla ayırarak parçalarına ayır
                parts = line.split()

                # Şehir ID, x, ve y koordinatlarını al
                if len(parts) == 3:
                    try:
                        city_id, x, y = map(float, parts)
                        cities.append((int(city_id), x, y))  # Şehir verilerini tuple olarak ekle
                    except ValueError:
                        # Hatalı satırları atla
                        continue

    return np.array(cities)
