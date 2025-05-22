from fastapi import FastAPI
from fastmcp import FastMCP
import uvicorn
import os

# Import MCP tools
from weather_mcp import get_weather
from location_mcp import get_location
from time_mcp import get_current_time

# Initialize FastAPI app
app = FastAPI()

# Initialize MCP server
mcp = FastMCP("weather-location-time-mcp", app=app)

# Health check endpoints
@app.get("/")
def root():
    return {"status": "Weather/Location/Time MCP online!"}

@app.get("/health")
def health():
    return {"status": "ok"}

# Register MCP tools
mcp.add_tool(get_weather)
mcp.add_tool(get_location)
mcp.add_tool(get_current_time)

# Run with uvicorn instead of mcp.run()
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)