from fastapi import FastAPI
from fastmcp import FastMCP
import os
from datetime import datetime

app = FastAPI()
mcp = FastMCP("weather-location-time-mcp", app=app)

@app.get("/mcp/healthz")
def healthz():
    return {"status": "ok"}

@mcp.tool()
def get_weather(latitude: float, longitude: float):
    print(f"get_weather called with latitude={latitude}, longitude={longitude}")
    return {"temperature": 20, "condition": "Clear"}

@mcp.tool()
def get_location(address: str):
    print(f"get_location called with address='{address}'")
    return {"lat": 40.7128, "lon": -74.0060}

@mcp.tool()
def get_current_time():
    current_time = datetime.utcnow().isoformat()
    print(f"get_current_time called, returning time={current_time}")
    return {"time": current_time}

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    print("Registered routes:")
    for route in app.routes:
        print(route.path)
    uvicorn.run(app, host="0.0.0.0", port=port)
