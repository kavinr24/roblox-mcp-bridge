# Agent Context: Roblox Studio Developer Bridge

This file provides context for external development tools, autonomous CLI systems, and LLM coding assistants interacting with this codebase.

## Purpose
This project is an open-source bridge that exposes Roblox Studio’s internal Model Context Protocol (MCP) server as a local REST API. It allows terminal-based agents to inspect, query, and modify a live Roblox Studio workspace via standard HTTP calls instead of relying on closed-source, proprietary software.

## Architecture & Communication Flow
1. **Host Connection:** `bridge.py` connects to the native Roblox Studio assistant process on your machine using an asynchronous stdio pipeline pointed at the local path inside `config.json`.
2. **Local Port Integration:** The bridge mounts a FastAPI loop listening by default on `http://127.0.0.1:8000`.
3. **Execution Loop:** External tools interact with the bridge via web requests. The bridge automatically wraps these payloads inside the required schema objects and pipes them to the active Studio process.

## Available Endpoints

### 1. Get Available Capabilities
* **Method/Route:** `GET /tools`
* **Purpose:** Queries the underlying Roblox Studio MCP process to list the active tools, functions, and argument constraints exposed by the game engine.

### 2. Execute Studio Commands
* **Method/Route:** `POST /execute`
* **Payload Structure:**
  ```json
  {
    "tool_name": "string_name_of_discovered_mcp_tool",
    "arguments": {
      "param1": "value1"
    }
  }