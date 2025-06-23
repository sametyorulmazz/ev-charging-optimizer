import pandas as pd

def calculate_fitness(assignments, user_station_matrix_df):

    total_distance = 0

    for user_id, station_id in assignments.items():
        row = user_station_matrix_df[
            (user_station_matrix_df["user_id"] == user_id) &
            (user_station_matrix_df["station_id"] == station_id)
        ]

        if not row.empty:
            distance = row.iloc[0]["distance"]
            total_distance += distance
        else:
            total_distance += 1e9

    return total_distance
