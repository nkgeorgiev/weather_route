import folium


def classify_severity(point):
    precip = point.get("precip_mm_hr", 0) or 0
    wind = point.get("wind_mps", 0) or 0

    if precip > 2 or wind > 10:
        return 3, "red"
    if precip > 0.1 or wind > 6:
        return 2, "orange"
    if wind > 3:
        return 1, "blue"
    return 0, "green"


def draw_route_weather_map(route_coords, weather_points, output_file="route_weather.html"):
    start_lat, start_lon = route_coords[0][1], route_coords[0][0]

    m = folium.Map(
        location=[start_lat, start_lon],
        zoom_start=6,
        tiles="OpenStreetMap"
    )

    # ---- Route line ----
    folium.PolyLine(
        locations=[(lat, lon) for lon, lat in route_coords],
        color="blue",
        weight=4,
        opacity=0.7
    ).add_to(m)

    # ---- Weather points ----
    for p in weather_points:
        severity, color = classify_severity(p)

        popup_html = f"""
        <b>ETA:</b> {p['eta']}<br>
        <b>Temp:</b> {p.get('temp_c', 'N/A')} °C<br>
        <b>Wind:</b> {p.get('wind_mps', 'N/A')} m/s<br>
        <b>Precip:</b> {p.get('precip_mm_hr', 'N/A')} mm/hr<br>
        <b>Severity:</b> {severity}
        """

        folium.CircleMarker(
            location=(p["lat"], p["lon"]),
            radius=7,
            color=color,
            fill=True,
            fill_color=color,
            fill_opacity=0.9,
            popup=popup_html
        ).add_to(m)

    m.save(output_file)
    print(f"Map saved to {output_file}")