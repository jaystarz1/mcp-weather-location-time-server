from fastapi import FastAPI
from fastmcp import FastMCP
import os

app = FastAPI()
mcp = FastMCP("weather-location-time-mcp", app=app)

@mcp.tool()
def get_weather(latitude: float, longitude: float):
    # Your weather function implementation here
    return {"temperature": 20, "condition": "Clear"}

@mcp.tool()
def get_location(address: str):
    # Your location function implementation here
    return {"lat": 40.7128, "lon": -74.0060}

@mcp.tool()
def get_current_time():
    from datetime import datetime
    return {"time": datetime.utcnow().isoformat()}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    mcp.run(transport="sse", host="0.0.0.0", port=port)
