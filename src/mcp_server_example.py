# mcp_server_example.py (illustrative)
from fastapi import FastAPI
from pydantic import BaseModel
import json

app = FastAPI(title="Example MCP Server", version="0.1.0")

class ToolRequest(BaseModel):
    tool_name: str
    params: dict # Parameters for the tool

@app.post("/mcp/invoke", summary="Invoke an MCP Tool")
async def invoke_tool(request: ToolRequest):
    """
    Receives a tool invocation request and simulates execution.
    In a real server, this would dispatch to actual tool functions
    based on request.tool_name and validate params.
    """
    # Example:
    # if request.tool_name == "read_file":
    #   try:
    #     content = await read_file_tool(request.params.get("path"))
    #     return {"status": "success", "result": content}
    #   except Exception as e:
    #     return {"status": "error", "message": str(e)}
    #
    # This example just echoes the request.
    print(f"MCP Invoke Request: Tool='{request.tool_name}', Params='{request.params}'")
    return {
        "status": "success",
        "result": f"Tool '{request.tool_name}' would be executed with params: {json.dumps(request.params)}."
    }

@app.get("/mcp/tools", summary="List Available MCP Tools")
async def list_tools():
    """
    Lists tools that this MCP server hypothetically makes available.
    In a real system, this might be dynamically generated or read from a config.
    """
    return {
        "tools": [
            {
                "name": "read_file",
                "description": "Reads the content of a specified file.",
                "parameters": {"path": "string (filepath)"}
            },
            {
                "name": "execute_shell_command",
                "description": "Executes a shell command.",
                "parameters": {"command": "string (shell command)"}
            },
            {
                "name": "project_linter",
                "description": "Runs the project's linter on specified files or directories.",
                "parameters": {"target_path": "string (optional, defaults to project root)"}
            }
        ]
    }

# To run this example server (ensure FastAPI and Uvicorn are installed: pip install fastapi uvicorn):
# uvicorn src.mcp_server_example:app --reload --port 8001
#
# Then you could POST to http://127.0.0.1:8001/mcp/invoke with JSON like:
# {
#   "tool_name": "read_file",
#   "params": {"path": "README.md"}
# }
# Or GET http://127.0.0.1:8001/mcp/tools
if __name__ == "__main__":
    import uvicorn
    # This is for direct execution a_example:app --reload --port 8001` from the project root.
    uvicorn.run("mcp_server_example:app", host="127.0.0.1", port=8001, reload=True)
