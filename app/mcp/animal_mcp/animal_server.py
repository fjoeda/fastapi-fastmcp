from fastmcp import FastMCP
from .tools.habitat_tool import register_tools


animal_mcp = FastMCP(
    name="animal_mcp",
)

register_tools(animal_mcp)

animal_mcp_app = animal_mcp.http_app(path="/mcp")  # Optional: Serve MCP at /mcp endpoint
