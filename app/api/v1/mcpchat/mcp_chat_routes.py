from fastapi import APIRouter, Form
from app.api.v1.mcpchat.mcp_chat_service import McpChatService


mcp_client_routes = APIRouter(tags=["mcpchat"])


@mcp_client_routes.post("/ask")
async def ask_mcp_chat(
    query: str = Form(..., description="Question to ask the MCP chat model")
):
    response = await McpChatService.handle_mcp_chat(query)
    return {
        "message": "ok",
        "payload": response
    }
