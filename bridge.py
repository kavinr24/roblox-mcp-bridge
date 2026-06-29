import asyncio
import json
import os
import sys
from typing import Dict, Any, Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

mcp_path= "C:\\Users\\kavin\\AppData\\Local\\Roblox\\mcp.bat"

app = FastAPI("Roblox Mcp Bridge")

class BridgeState:
    def __init__(self):
        self.session: Optional[ClientSession] = None
        self.mcp_context = None
        self.read_stream = None
        self.write_stream = None

class ToolExecutionRequest(BaseModel):
    tool_name: str
    arguments: Dict[str, Any]

state = BridgeState()

@app.on_event("startup")
async def launch():
    if not os.path.exists(mcp_path):
        raise RuntimeError("mcp.bat not found")

    params = StdioServerParameters(
        command=mcp_path,
        args=["--stdio"],
        env=os.environ.copy()
    )

    asyncio.create_task(manage_life(params))

async def manage_life(server_params):
    try:
        async with stdio_client(server_params) as (read_stream, write_stream):
            async with ClientSession(read_stream, write_stream) as session:
                state.session = session
                await session.initialize()
                print("\nConnected to studio mcp channel")
                
                tools_response = await session.list_tools()
                print("Found studio tools")
                
                while True:
                    await asyncio.sleep(1)
    except Exception as e:
        print(f"\nLifecycle has broken: {e}")
        state.session = None

@app.post("/execute")
async def execute_tool(payload: ToolExecutionRequest):
    if not state.session:
        raise HTTPException(status_code=503, detail="Studio MCP connection is offline")
    
    try:
        print(f"Sending execution: '{payload.tool_name}'")
        result = await state.session.call_tool(payload.tool_name, arguments=payload.arguments)
        return {"status": "success", "result": result.model_dump() if hasattr(result, 'model_dump') else result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Execution failed on engine: {str(e)}")

@app.get("/tools")
async def get_available_tools():
    if not state.session:
        raise HTTPException(status_code=503, detail="Studio MCP connection is offline")
    tools_response = await state.session.list_tools()
    return tools_response.model_dump() if hasattr(tools_response, 'model_dump') else tools_response

if __name__ == "__main__":
    print(f"Starting bridge on http://localhost:{8000}")
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")