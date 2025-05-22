# Weather/Location/Time MCP Server

This project provides a unified Model Context Protocol (MCP) server for **weather**, **location**, and **time** tools.  
It is designed for use as a remote MCP tool server for AI models (like Claude, GPT, etc.).

## Features

- Modular Python project using [FastAPI](https://fastapi.tiangolo.com/) and [FastMCP](https://github.com/modelcontextprotocol/fastmcp)
- Three integrated MCP tools:
  - **Weather:** US National Weather Service (NWS) API forecasts by latitude/longitude
  - **Location:** Geocoding using OpenStreetMap Nominatim API (no API key required)
  - **Time:** Current date/time for any IANA timezone
- Production-ready: deployable to [Render.com](https://render.com/) or any cloud server

---

## Quick Start (Local)

1. **Clone the repo**
    ```sh
    git clone https://github.com/jaystarz1/mcp-weather-location-time-server.git
    cd mcp-weather-location-time-server
    ```

2. **Create and activate a virtual environment**
    ```sh
    python3.11 -m venv .venv
    source .venv/bin/activate
    ```

3. **Install dependencies**
    ```sh
    pip install -r requirements.txt
    ```

4. **Run the server**
    ```sh
    python main.py
    ```

- Server will run at `http://localhost:8000/`
- Main MCP endpoint is `/sse`
- This server is intended for use by MCP-capable clients, not for human web browsing.

---

## MCP Tools

- **get_weather:** Returns the weather forecast for a given latitude/longitude (US only).
- **get_location:** Looks up latitude/longitude for an address or place name.
- **get_current_time:** Returns the current date/time in any IANA timezone.

---

## Deployment

### Deploy to Render.com

1. Create a new Web Service on [Render.com](https://render.com/) and connect this repo.
2. Set:
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `python main.py`
   - **Environment Variable:** `PYTHON_VERSION = 3.11.12`
3. Click “Deploy”.

### Environment Variables

- None required for open APIs (Weather/Location/Time).

---

## Troubleshooting

See [Troubleshooting Guide](#) for common problems and solutions (update this link if you create a guide).

---

## License

MIT

---

## Credits

- Built by [jaystarz1](https://github.com/jaystarz1) using FastAPI and FastMCP.
- Weather data by [US National Weather Service](https://weather.gov).
- Location/geocoding by [OpenStreetMap Nominatim](https://nominatim.org/).

---

