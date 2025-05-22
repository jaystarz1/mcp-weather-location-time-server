from fastapi import FastAPI
from fastmcp import FastMCP
import os
import asyncio
import uvicorn

# Import MCP tools
from weather_mcp import get_weather
from location_mcp import get_location
from time_mcp import get_current_time

# Initialize FastAPI app
app = FastAPI()

# Initialize MCP server with FastAPI app
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

async def main():
    port = int(os.environ.get("PORT", 8000))

    # Start MCP server event loop
    serve_task = asyncio.create_task(mcp.serve())

    # Configure and start Uvicorn server for FastAPI app
    config = uvicorn.Config(app, host="0.0.0.0", port=port, log_level="info")
    server = uvicorn.Server(config)

    # Run both concurrently
    await asyncio.gather(serve_task, server.serve())

if __name__ == "__main__":
    asyncio.run(main())
