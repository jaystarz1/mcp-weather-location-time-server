import os
from datetime import datetime, timedelta
import re
from dotenv import load_dotenv
from fastmcp import FastMCP
import httpx

load_dotenv()

mcp = FastMCP("weather")
API_KEY = os.getenv("OPENWEATHER_API_KEY")

def parse_when(when: str):
    """Parse time expressions like 'tomorrow', 'next week', etc."""
    now = datetime.now()
    when = when.lower()
    
    if when in ["now", "today"]:
        return now
    elif when == "tomorrow":
        return now + timedelta(days=1)
    elif "next week" in when:
        return now + timedelta(days=7)
    
    # Handle "next [day]"
    days = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
    for i, day in enumerate(days):
        if f"next {day}" in when:
            days_ahead = (i - now.weekday() + 7) % 7
            return now + timedelta(days=days_ahead if days_ahead > 0 else 7)
    
    return now

@mcp.tool()
async def get_weather(location: str, when: str = "now") -> dict:
    """Get weather for any location and time."""
    if not API_KEY:
        return {"error": "No OpenWeather API key configured"}
    
    # First, geocode the location
    geo_url = "http://api.openweathermap.org/geo/1.0/direct"
    
    async with httpx.AsyncClient() as client:
        # Get coordinates
        geo_resp = await client.get(geo_url, params={
            "q": location,
            "limit": 1,
            "appid": API_KEY
        })
        
        if geo_resp.status_code != 200 or not geo_resp.json():
            return {"error": f"Location '{location}' not found"}
        
        geo_data = geo_resp.json()[0]
        lat, lon = geo_data["lat"], geo_data["lon"]
        
        # Parse when
        target_date = parse_when(when)
        days_ahead = (target_date - datetime.now()).days
        
        # Get weather
        if days_ahead <= 0:
            # Current weather
            weather_url = "https://api.openweathermap.org/data/2.5/weather"
            weather_resp = await client.get(weather_url, params={
                "lat": lat,
                "lon": lon,
                "appid": API_KEY,
                "units": "metric"
            })
        else:
            # Forecast (up to 5 days)
            weather_url = "https://api.openweathermap.org/data/2.5/forecast"
            weather_resp = await client.get(weather_url, params={
                "lat": lat,
                "lon": lon,
                "appid": API_KEY,
                "units": "metric"
            })
        
        if weather_resp.status_code != 200:
            return {"error": "Failed to get weather data"}
        
        data = weather_resp.json()
        
        # Format response
        if days_ahead <= 0:
            # Current weather response
            return {
                "location": f"{geo_data['name']}, {geo_data['country']}",
                "when": when,
                "temperature": data["main"]["temp"],
                "description": data["weather"][0]["description"],
                "feels_like": data["main"]["feels_like"],
                "humidity": data["main"]["humidity"]
            }
        else:
            # Find closest forecast
            target_ts = target_date.replace(hour=12).timestamp()
            closest = min(data["list"], key=lambda x: abs(x["dt"] - target_ts))
            
            return {
                "location": f"{geo_data['name']}, {geo_data['country']}",
                "when": when,
                "date": target_date.strftime("%Y-%m-%d"),
                "temperature": closest["main"]["temp"],
                "description": closest["weather"][0]["description"],
                "feels_like": closest["main"]["feels_like"],
                "humidity": closest["main"]["humidity"]
            }

if __name__ == "__main__":
    mcp.run(transport="sse", host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))