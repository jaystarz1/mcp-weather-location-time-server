from fastmcp import FastMCP
import os

# Import your MCP tools
from weather_mcp import get_weather
from location_mcp import get_location
from time_mcp import get_current_time

# Initialize MCP instance (no separate FastAPI app)
mcp = FastMCP("weather-location-time-mcp")

# Register MCP tools
mcp.add_tool(get_weather)
mcp.add_tool(get_location)
mcp.add_tool(get_current_time)

# Root endpoint on MCP's internal FastAPI app
@mcp.app.get("/")
def root():
    return {"status": "Weather/Location/Time MCP online!"}

# Health check endpoint on MCP's internal FastAPI app
@mcp.app.get("/health")
def health():
    return {"status": "ok"}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    print(f"Starting MCP server on port {port}...")
    mcp.run(transport="sse", host="0.0.0.0", port=port)
