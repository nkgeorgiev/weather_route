import os
import requests
from datetime import datetime, timezone, timedelta
from services.http_utils import safe_request
TOMORROW_URL = "https://api.tomorrow.io/v4/timelines"


def get_weather_for_points(tmrw_api_key, points):
    if not points:
        return []

    # ---- 1. Compute time window ----
    etas = [
        datetime.fromisoformat(p["eta"]).astimezone(timezone.utc)
        for p in points
    ]

    start_time = min(etas).replace(minute=0, second=0, microsecond=0)
    end_time = max(etas).replace(minute=0, second=0, microsecond=0) + timedelta(hours=1)

    # ---- 2. Use a representative location (route midpoint) ----
    # Weather grids are spatially smooth; we'll interpolate per point
    mid = points[len(points) // 2]

    body = {
        "location": [mid["lat"], mid["lon"]],
        "fields": [
            "temperature",
            "weatherCode",
            "windSpeed",
            "precipitationIntensity"
        ],
        "timesteps": ["1h"],
        "startTime": start_time.isoformat(),
        "endTime": end_time.isoformat(),
        "units": "metric"
    }

    assert tmrw_api_key, "TOMORROW_API_KEY is not set"

    headers = {
        "apikey": tmrw_api_key,
        "Content-Type": "application/json"
    }

    res = safe_request("POST", TOMORROW_URL, json=body, headers=headers)
    data = res.json()

    intervals = data["data"]["timelines"][0]["intervals"]

    # ---- 3. Index forecast by hour ----
    forecast_by_hour = {
        datetime.fromisoformat(i["startTime"]).astimezone(timezone.utc): i["values"]
        for i in intervals
    }

    # ---- 4. Match each point to closest forecast hour ----
    results = []

    for p, eta in zip(points, etas):
        forecast_hour = eta.replace(minute=0, second=0, microsecond=0)

        values = forecast_by_hour.get(forecast_hour)

        if not values:
            results.append({
                **p,
                "forecast_unavailable": True
            })
            continue

        results.append({
            **p,
            "temp_c": values["temperature"],
            "weather_code": values["weatherCode"],
            "wind_mps": values["windSpeed"],
            "precip_mm_hr": values["precipitationIntensity"]
        })

    return results
