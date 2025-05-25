import os
from datetime import datetime, timedelta
import re
import httpx
from dotenv import load_dotenv
from fastmcp import FastMCP

load_dotenv()

MAPBOX_API_KEY = os.getenv("MAPBOX_API_KEY")
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")

# Initialize FastMCP WITHOUT FastAPI app for SSE transport
mcp = FastMCP("weather-time-location")

# [Keep all your helper functions exactly as they are]
# geocode, parse_when, fetch_weather - no changes needed

@mcp.tool()
async def get_weather(place: str, when: str = "now") -> dict:
    """Get weather for a location and time."""
    coords = await geocode(place)
    if not coords:
        return {"error": f"Place '{place}' not found"}
    
    lat, lon = coords
    dt = parse_when(when)
    result = await fetch_weather(lat, lon, dt)
    
    return {
        "place": place,
        "when": when,
        "parsed_date": dt.isoformat(),
        **result
    }

@mcp.tool()
async def get_location(place: str) -> dict:
    """Get coordinates for a location."""
    coords = await geocode(place)
    if not coords:
        return {"error": f"Place '{place}' not found"}
    
    lat, lon = coords
    return {
        "place": place,
        "latitude": lat,
        "longitude": lon
    }

@mcp.tool()
async def pack_for_weather(place: str, when: str = "now") -> dict:
    """Get packing suggestions based on weather."""
    weather = await get_weather(place, when)
    
    if "error" in weather:
        return weather
    
    temp = weather.get("temp", 20)
    desc = weather.get("description", "").lower()
    
    suggestions = {
        "weather_summary": weather,
        "essentials": [],
        "recommended": []
    }
    
    # Temperature-based suggestions
    if temp < 0:
        suggestions["essentials"] = ["Winter coat", "Gloves", "Hat", "Scarf"]
        suggestions["recommended"] = ["Thermal underwear", "Winter boots"]
    elif temp < 10:
        suggestions["essentials"] = ["Warm jacket", "Long pants"]
        suggestions["recommended"] = ["Sweater", "Light gloves"]
    elif temp < 20:
        suggestions["essentials"] = ["Light jacket", "Comfortable shoes"]
        suggestions["recommended"] = ["Long-sleeve shirt"]
    else:
        suggestions["essentials"] = ["Sunscreen", "Sunglasses"]
        suggestions["recommended"] = ["Hat", "Light clothing"]
    
    # Weather-based additions
    if "rain" in desc or "shower" in desc:
        suggestions["essentials"].append("Umbrella")
        suggestions["recommended"].append("Rain jacket")
    
    if "snow" in desc:
        suggestions["essentials"].append("Winter boots")
    
    return suggestions

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 8000))
    mcp.run(transport="sse", host="0.0.0.0", port=port)