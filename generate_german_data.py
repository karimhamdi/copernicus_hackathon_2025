import random
import json

germany_heatmap_data = {
    "lat": [],
    "lon": [],
    "intensity": []
}

german_regions = [
    (52.5200, 13.4050),  # Berlin
    (48.1351, 11.5820),  # München
    (53.5511, 9.9937),   # Hamburg
    (50.1109, 8.6821),   # Frankfurt
    (51.1657, 10.4515),  # Deutschland Mitte
    (52.0907, 8.6829),   # Dortmund
    (51.5074, 13.0465),  # Dresden
    (49.4875, 8.4660),   # Mannheim
    (48.7758, 9.1829),   # Stuttgart
    (53.3811, 8.8017),   # Bremen
]


for lat, lon in german_regions:
    for _ in range(100):  
        germany_heatmap_data["lat"].append(lat + random.uniform(-0.5, 0.5))  
        germany_heatmap_data["lon"].append(lon + random.uniform(-0.5, 0.5)) 
        germany_heatmap_data["intensity"].append(random.randint(10, 100))  


with open("data_3.json", "w") as json_file:
    json.dump(germany_heatmap_data, json_file, indent=4)