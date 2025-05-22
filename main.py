from fastapi import FastAPI
from fastmcp import FastMCP
import os

# Import your MCP tool functions
from weather_mcp import get_weather
from location_mcp import get_location
from time_mcp import get_current_time

# Initialize FastAPI app
app = FastAPI()

# Initialize MCP server with the FastAPI app
mcp = FastMCP("weather-location-time-mcp", app=app)

# Basic root endpoint to verify server is online
@app.get("/")
def root():
    return {"status": "Weather/Location/Time MCP online!"}

# Health check endpoint
@app.get("/health")
def health():
    return {"status": "ok"}

# Register your MCP tools here
mcp.add_tool(get_weather)
mcp.add_tool(get_location)
mcp.add_tool(get_current_time)

# Run the server with SSE transport on the dynamic port (default 8000)
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    mcp.run(transport="sse", host="0.0.0.0", port=port)
