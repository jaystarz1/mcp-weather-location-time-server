from fastapi import FastAPI
from fastmcp import FastMCP
import os

# Import MCP tools
from weather_mcp import get_weather
from location_mcp import get_location
from time_mcp import get_current_time

# Initialize FastAPI app and MCP server
app = FastAPI()
mcp = FastMCP("weather-location-time-mcp", app=app)

# Health check endpoint
@app.get("/")
def root():
    return {"status": "Weather/Location/Time MCP online!"}

@app.get("/mcp/healthz")
def healthz():
    return {"status": "ok"}

# Register MCP tools
mcp.add_tool(get_weather)
mcp.add_tool(get_location)
mcp.add_tool(get_current_time)

# Run MCP server with dynamic port for Render deployment
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    mcp.run(transport="sse", host="0.0.0.0", port=port)
