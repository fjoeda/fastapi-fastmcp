# FastAPI FastMCP
This repository contains a FastAPI app that serves multiple endpoints of Model Context Protocol (MCP) servers. It is designed to be a lightweight and efficient way to interact with MCP servers, providing a simple interface for users to access various functionalities.

This is still kind of a exploration project on how to best serve multiple MCP servers with FastAPI. It is not intended to be a production-ready solution, but rather a starting point for further development and experimentation.

## Exploration that has been done and future plans
- [x] Basic FastAPI app structure
- [x] Serving multiple MCP servers
- [x] Handling server lifecycles and integrate them with FastAPI
- [x] Basic tools for interacting with MCP servers
- [ ] Handling elicitations and responses both in server side and client side
- [ ] Authentication and authorization
- [ ] MCP client integration

The items above may be updated as the project evolves.

## Testing Methods
Since the mcp servers are wrapped in FastAPI, the only possible mcp transport is streamable http. There are several mcp clients that can be used to test the endpoints such as :
- mcp-client-for-ollama [GitHub Repository](https://github.com/jonigl/mcp-client-for-ollama)
- mcp inspector [GitHub Repository](https://github.com/modelcontextprotocol/inspector) to test the tools endpoints.
- langgraph agent + lanchain-mcp-adapters [GitHub Repository](https://github.com/langchain-ai/langchain-mcp-adapters).

It is recommended to use multiple clients to test the endpoints and ensure compatibility.

## Installation
To install the required dependencies, run the following command:
```
# create the virtual environment
uv venv

# install the dependencies
uv pip install -r requirements.txt

# run the app
uv uvicorn app.main:app
```