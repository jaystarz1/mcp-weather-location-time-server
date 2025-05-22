import requests

NWS_API_BASE = "https://api.weather.gov"
USER_AGENT = "weather-mcp/1.0"

def get_weather(latitude: float, longitude: float):
    """
    Get weather forecast for a location using the US National Weather Service API.
    Args:
        latitude: Latitude of the location
        longitude: Longitude of the location
    """
    # Get the forecast grid endpoint
    points_url = f"{NWS_API_BASE}/points/{latitude},{longitude}"
    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "application/geo+json"
    }
    try:
        points_resp = requests.get(points_url, headers=headers, timeout=15)
        points_resp.raise_for_status()
        points_data = points_resp.json()
    except Exception as e:
        return {"error": f"Unable to fetch grid point: {e}"}

    try:
        forecast_url = points_data["properties"]["forecast"]
        forecast_resp = requests.get(forecast_url, headers=headers, timeout=15)
        forecast_resp.raise_for_status()
        forecast_data = forecast_resp.json()
    except Exception as e:
        return {"error": f"Unable to fetch forecast: {e}"}

    # Format the periods into a readable forecast
    periods = forecast_data["properties"].get("periods", [])
    if not periods:
        return {"error": "No forecast periods returned."}

    # Return just the next 5 periods, more compact
    result = []
    for period in periods[:5]:
        result.append({
            "name": str(period.get("name", "")),
            "temperature": str(period.get("temperature", "")),
            "temperatureUnit": str(period.get("temperatureUnit", "")),
            "windSpeed": str(period.get("windSpeed", "")),
            "windDirection": str(period.get("windDirection", "")),
            "shortForecast": str(period.get("shortForecast", "")),
            "detailedForecast": str(period.get("detailedForecast", "")),
        })

    return {"forecasts": result}
