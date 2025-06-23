import folium
from src.visualize_api import get_route_duration_and_distance


def visualize_final_assignment(final_assignments, users_df, stations_df, output_file="final_assignment_map.html"):
    
    start_location = [users_df['Latitude'].mean(), users_df['Longitude'].mean()]
    m = folium.Map(location=start_location, zoom_start=11)

    # Kullanıcı ve istasyon konumlarını dict'e çevir
    user_coords = {
        row['user_id']: (row['Latitude'], row['Longitude'])
        for _, row in users_df.iterrows()
    }
    station_coords = {
        row['station_id']: (row['Latitude'], row['Longitude'])
        for _, row in stations_df.iterrows()
    }

    for user_id, station_id in final_assignments.items():
        if user_id not in user_coords or station_id not in station_coords:
            continue

        user_loc = user_coords[user_id]
        station_loc = station_coords[station_id]

        # Rota verisi al
        duration, distance, points = get_route_duration_and_distance(
            user_loc[0], user_loc[1], station_loc[0], station_loc[1]
        )

        # Noktaları haritaya ekle
        folium.Marker(
            location=user_loc,
            popup=f"Kullanıcı {user_id}",
            icon=folium.Icon(color="blue", icon="user", prefix="fa")
        ).add_to(m)

        folium.Marker(
            location=station_loc,
            popup=f"İstasyon {station_id}",
            icon=folium.Icon(color="green", icon="flash", prefix="fa")
        ).add_to(m)

        # Rota çizimi
        if points:
            folium.PolyLine(points, color="red", weight=4, opacity=0.6).add_to(m)

    m.save(output_file)
    print(f" Harita kaydedildi: {output_file}")
