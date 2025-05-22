# Weather/Location/Time MCP Server

This project provides a remote MCP (Model Context Protocol) server that exposes weather, location, and time context for use by Claude or any MCP-compatible client.

## Features

- Modular architecture with [FastAPI](https://fastapi.tiangolo.com/) and [FastMCP](https://github.com/modelcontextprotocol/fastmcp)
- Health check endpoint for deployment
- Ready to integrate Weather, Location, and Time MCPs

## Quick Start

1. **Clone the repo and open in VS Code**
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
    The server will start on `http://localhost:8000`.

## Deployment

Supports deployment on [Render.com](https://render.com/) with dynamic port binding and health check at `/`.

## To Do

- Integrate Weather, Location, and Time MCP tools from [modelcontextprotocol/servers](https://github.com/modelcontextprotocol/servers)

---

## License

MIT (or your preferred license)
