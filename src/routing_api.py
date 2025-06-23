import requests
import os
from dotenv import load_dotenv
from tqdm import tqdm

load_dotenv()
TOMTOM_API_KEY = os.getenv("TOMTOM_ROUTING_API_KEY")

def get_route_duration_and_distance(from_lat, from_lon, to_lat, to_lon):
    url = (
        f"https://api.tomtom.com/routing/1/calculateRoute/"
        f"{from_lat},{from_lon}:{to_lat},{to_lon}/json?"
        f"key={TOMTOM_API_KEY}&travelMode=car&traffic=true"
    )

    try:
        response = requests.get(url)
        if response.status_code != 200:
            print(f"TomTom API Hatası: {response.status_code}")
            return 1e9, 1e9

        data = response.json()
        if "routes" not in data or not data["routes"]:
            print("Rota bilgisi bulunamadı.")
            return 1e9, 1e9

        route = data["routes"][0]
        duration = route["summary"]["travelTimeInSeconds"]
        length = route["summary"]["lengthInMeters"]

        return duration, length

    except Exception as e:
        print("TomTom API Hatası:", e)
        return 1e9, 1e9

def get_duration_matrix(users_df, stations_df):
    matrix = {}
    for _, user in tqdm(users_df.iterrows(), total=len(users_df), desc="Kullanıcılar işleniyor"):
        user_id = user["user_id"]
        matrix[user_id] = {}
        for _, station in stations_df.iterrows():
            station_id = station["station_id"]
            from_lat, from_lon = user["Latitude"], user["Longitude"]
            to_lat, to_lon = station["Latitude"], station["Longitude"]
            duration, _ = get_route_duration_and_distance(from_lat, from_lon, to_lat, to_lon)
            matrix[user_id][station_id] = duration
    return matrix

