import os
from datetime import datetime, timedelta
import re
import httpx
from dotenv import load_dotenv
from fastmcp import FastMCP

load_dotenv()

MAPBOX_API_KEY = os.getenv("MAPBOX_API_KEY")
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")

mcp = FastMCP("weather-time-location")

@app.get("/")
def root():
   return {"status": "Weather MCP Server online"}

mcp = FastMCP("weather-time-location", app=app)

async def geocode(place: str):
   if MAPBOX_API_KEY:
       url = f"https://api.mapbox.com/geocoding/v5/mapbox.places/{place}.json"
       params = {"access_token": MAPBOX_API_KEY, "limit": 1}
       async with httpx.AsyncClient() as client:
           try:
               resp = await client.get(url, params=params)
               resp.raise_for_status()
               data = resp.json()
               if data.get("features"):
                   coords = data["features"][0]["geometry"]["coordinates"]
                   return coords[1], coords[0]
           except Exception:
               pass
   
   cities = {
       "buffalo": (42.8864, -78.8784),
       "toronto": (43.6532, -79.3832),
       "ottawa": (45.4215, -75.6972),
       "gatineau": (45.4765, -75.7013),
       "montreal": (45.5017, -73.5673),
       "vancouver": (49.2827, -123.1207),
   }
   key = place.lower().strip()
   if key in cities:
       return cities[key]
   return None

def parse_when(when: str):
   now = datetime.now()
   when = when.lower()
   
   if when in ("now", "today"):
       return now
   
   match = re.search(r"next (\w+)", when)
   if match:
       day = match.group(1)
       days = ["monday","tuesday","wednesday","thursday","friday","saturday","sunday"]
       if day in days:
           target = (days.index(day) - now.weekday() + 7) % 7
           return now + timedelta(days=target if target > 0 else 7)
   
   if "afternoon" in when:
       dt = parse_when(when.replace("afternoon", "").strip())
       return dt.replace(hour=14, minute=0, second=0, microsecond=0)
   
   return now

async def fetch_weather(lat, lon, dt: datetime):
   if not OPENWEATHER_API_KEY:
       return {"error": "OpenWeatherMap API key missing"}
   
   url = "https://api.openweathermap.org/data/2.5/forecast"
   params = {
       "lat": lat, 
       "lon": lon, 
       "appid": OPENWEATHER_API_KEY, 
       "units": "metric"
   }
   
   async with httpx.AsyncClient() as client:
       try:
           resp = await client.get(url, params=params)
           resp.raise_for_status()
           data = resp.json()
           
           if abs((dt - datetime.now()).days) < 1:
               curr_url = "https://api.openweathermap.org/data/2.5/weather"
               curr_resp = await client.get(curr_url, params=params)
               curr_resp.raise_for_status()
               curr_data = curr_resp.json()
               
               return {
                   "description": curr_data.get("weather", [{}])[0].get("description", "No data"),
                   "temp": curr_data.get("main", {}).get("temp"),
                   "feels_like": curr_data.get("main", {}).get("feels_like"),
                   "humidity": curr_data.get("main", {}).get("humidity"),
                   "dt": dt.strftime("%Y-%m-%d")
               }
           
           target_timestamp = dt.timestamp()
           closest = None
           min_diff = float('inf')
           
           for forecast in data.get("list", []):
               diff = abs(forecast["dt"] - target_timestamp)
               if diff < min_diff:
                   min_diff = diff
                   closest = forecast
           
           if closest:
               return {
                   "description": closest.get("weather", [{}])[0].get("description", "No data"),
                   "temp": closest.get("main", {}).get("temp"),
                   "feels_like": closest.get("main", {}).get("feels_like"),
                   "humidity": closest.get("main", {}).get("humidity"),
                   "dt": dt.strftime("%Y-%m-%d %H:%M")
               }
           
           return {"error": "Forecast not available"}
           
       except Exception as e:
           return {"error": str(e)}

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
   
   if "rain" in desc or "shower" in desc:
       suggestions["essentials"].append("Umbrella")
       suggestions["recommended"].append("Rain jacket")
   
   if "snow" in desc:
       suggestions["essentials"].append("Winter boots")
   
   return suggestions

if __name__ == "__main__":
    mcp.run(transport="sse", host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))