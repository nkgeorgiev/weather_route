from geopy.distance import geodesic
from datetime import timedelta
from services.http_utils import safe_request

def sample_route_every_km(
    coordinates,
    total_distance_km,
    total_duration_seconds,
    interval_km,
    departure_time
):
    sampled = []
    accumulated = 0.0
    last_point = coordinates[0]
    last_time = departure_time
    avg_speed_km_s = total_distance_km / total_duration_seconds

    for point in coordinates[1:]:
        segment_distance = geodesic(
            (last_point[1], last_point[0]),
            (point[1], point[0])
        ).km

        accumulated += segment_distance

        if accumulated >= interval_km:
            travel_seconds = accumulated / avg_speed_km_s
            eta = last_time + timedelta(seconds=travel_seconds)
            last_time = eta
            sampled.append({
                "lon": point[0],
                "lat": point[1],
                "eta": eta.isoformat()
            })

            accumulated = 0.0

        last_point = point

    return sampled
