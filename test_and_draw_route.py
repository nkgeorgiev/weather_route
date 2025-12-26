import requests
from datetime import datetime
from services.geocoding import geocode_place
from services.routing import get_route
from draw_map import draw_route_weather_map
from settings import settings

API_URL = "http://127.0.0.1:8000/route-weather"



def main():
    origin = "Silistra, Bulgaria"
    destination = "Sofia, Bulgaria"
    departure_date = "2025-12-29"
    departure_time = "10:00:00"
    departure_datetime = f"{departure_date}T{departure_time}"

    print("Calling backend API...")
    res = requests.get(
        API_URL,
        params={
            "origin": origin,
            "destination": destination,
            "departure_time": departure_datetime
        },
        timeout=60
    )
    res.raise_for_status()
    data = res.json()

    print("Geocoding locations...")
    origin_coords = geocode_place(origin)
    destination_coords = geocode_place(destination)

    print("Fetching full route geometry...")
    route = get_route(settings.ORS_API_KEY, origin_coords, destination_coords)

    output_file = f"route_weather_{departure_datetime}.html"
    print("Drawing map...")
    draw_route_weather_map(
        route_coords=route["coordinates"],
        weather_points=data["points"],
        output_file=output_file
    )

    print(f"Done. Open {output_file} in your browser.")


if __name__ == "__main__":
    main()
