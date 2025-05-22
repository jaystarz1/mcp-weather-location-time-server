from fastapi import FastAPI
from fastmcp import FastMCP
import os

# Import your MCP tools
from weather_mcp import get_weather
from location_mcp import get_location
from time_mcp import get_current_time

app = FastAPI()
mcp = FastMCP("weather-location-time-mcp", app=app)

@app.get("/")
def root():
    return {"status": "Weather/Location/Time MCP online!"}

@app.get("/mcp/healthz")
def healthz():
    return {"status": "ok"}

# Register all MCP tools
mcp.add_tool(get_weather)
mcp.add_tool(get_location)
mcp.add_tool(get_current_time)

# Run the server (dynamic port for Render)
PORT = int(os.environ.get("PORT", 8000))
mcp.run(transport="sse", host="0.0.0.0", port=PORT)
