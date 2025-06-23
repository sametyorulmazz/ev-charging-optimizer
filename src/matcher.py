import pandas as pd
from routing_api import get_route_duration_and_distance
from tqdm import tqdm
import time


def build_user_station_matrix(users_df, stations_df):

    rows = []

    for _, user in tqdm(users_df.iterrows(), total=len(users_df), desc="Kullanıcı-İstasyon eşleştirmesi"):
        user_id = user['user_id']
        user_lat = user['Latitude']
        user_lon = user['Longitude']

        for _, station in stations_df.iterrows():
            station_id = station['station_id']
            station_lat = station['Latitude']
            station_lon = station['Longitude']

            duration, distance = get_route_duration_and_distance(user_lat, user_lon, station_lat, station_lon)

            # API limiti için küçük gecikme
            time.sleep(0.1)

            if duration is not None and distance is not None:
                rows.append({
                    "user_id": user_id,
                    "station_id": station_id,
                    "duration": duration,
                    "distance": distance
                })

    return pd.DataFrame(rows)


if __name__ == "__main__":
    users_df = pd.read_csv("data/users.csv")
    stations_df = pd.read_csv("data/stations.csv")

    result_df = build_user_station_matrix(users_df, stations_df)

    result_df["user_id"] = result_df["user_id"].astype(int)

    result_df.to_csv("data/user_station_matrix.csv", index=False)
    print("✔ Kullanıcı-istasyon mesafe/süre matrisi oluşturuldu ve kaydedildi.")

