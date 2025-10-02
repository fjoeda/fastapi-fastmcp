from fastmcp import FastMCP
from .tools import calculation, caffee

sample_mcp = FastMCP(
    name="sample_mcp",
)

calculation.register_tools(sample_mcp)
caffee.register_tools(sample_mcp)

sample_mcp_app = sample_mcp.http_app(path="/mcp")  # Optional: Serve MCP at /mcp endpoint