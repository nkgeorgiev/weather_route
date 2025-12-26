import requests
import polyline
from services.http_utils import safe_request


ORS_URL = "https://api.openrouteservice.org/v2/directions/driving-car"


def get_route(ors_api_key, origin, destination):
    """
    Get the fastest route between origin and destination,
    considering alternatives and avoiding unpaved roads.
    origin/destination: (lon, lat)
    Returns:
        {
            "coordinates": [(lon, lat), ...],
            "distance_km": float,
            "duration_seconds": float
        }
    """
    if not ors_api_key:
        raise RuntimeError("ORS_API_KEY not set")

    headers = {"Authorization": ors_api_key, "Content-Type": "application/json"}

    body = {
            "coordinates": [list(origin), list(destination)],
            "preference": "fastest",
            #"instructions": False,
        }
    res = safe_request("POST", ORS_URL, json=body, headers=headers)
    data = res.json()

    routes = data["routes"]
    if not routes:
        raise RuntimeError("No route returned from OpenRouteService")

    # Pick the route with the shortest duration
    best_route = min(routes, key=lambda r: r["summary"]["duration"])

    # Decode polyline to list of (lon, lat)
    geometry = polyline.decode(best_route["geometry"])
    coords = [(lon, lat) for lat, lon in geometry]

    return {
        "coordinates": coords,
        "distance_km": best_route["summary"]["distance"] / 1000,
        "duration_seconds": best_route["summary"]["duration"]
    }