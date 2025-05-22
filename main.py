from fastapi import FastAPI
from fastmcp import FastMCP
import os

# Import your MCP tool functions
from weather_mcp import get_weather
from location_mcp import get_location
from time_mcp import get_current_time

app = FastAPI()
mcp = FastMCP("weather-location-time-mcp", app=app)

# Register your tools
mcp.add_tool(get_weather)
mcp.add_tool(get_location)
mcp.add_tool(get_current_time)

# Basic root endpoint for quick status check
@app.get("/")
def root():
    return {"status": "Weather/Location/Time MCP online!"}

# Health check endpoint
@app.get("/health")
def health():
    return {"status": "ok"}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    mcp.run(transport="sse", host="0.0.0.0", port=port)
