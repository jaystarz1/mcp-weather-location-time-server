from fastapi import FastAPI
from fastmcp import FastMCP
from datetime import datetime
import os

app = FastAPI()
mcp = FastMCP("weather-location-time-mcp", app=app)

@app.get("/")
def root():
    return {"status": "Weather MCP Server online!"}

@app.get("/mcp/healthz")
def healthz():
    return {"status": "ok"}

@mcp.tool()
def get_weather(latitude: float, longitude: float):
    """Get weather for a specific location"""
    # Your weather implementation here
    return {"temperature": 20, "condition": "Clear", "latitude": latitude, "longitude": longitude}

@mcp.tool()
def get_location(address: str):
    """Get coordinates for an address"""
    # Your location implementation here
    return {"lat": 40.7128, "lon": -74.0060, "address": address}

@mcp.tool()
def get_current_time():
    """Get the current UTC time"""
    from datetime import datetime
    return {"time": datetime.utcnow().isoformat()}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    mcp.run(transport="sse", host="0.0.0.0", port=port)