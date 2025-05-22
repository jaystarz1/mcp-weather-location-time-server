import requests

def get_location(address: str):
    """
    Get latitude and longitude for a given address or place name.
    Uses OpenStreetMap Nominatim API (no API key needed).
    """
    url = "https://nominatim.openstreetmap.org/search"
    params = {
        "q": address,
        "format": "json",
        "limit": 1,
    }
    headers = {
        "User-Agent": "MCP-Location-Server/1.0"
    }
    try:
        resp = requests.get(url, params=params, headers=headers, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        if not data:
            return {"error": f"No results for: {address}"}
        result = data[0]
        return {
            "address": address,
            "latitude": result.get("lat", ""),
            "longitude": result.get("lon", ""),
            "display_name": result.get("display_name", ""),
        }
    except Exception as e:
        return {"error": str(e)}
