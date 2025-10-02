from .mcp_chat_helper import McpChatHelper
from app.models.v1.chat.llm_chat_schema import (
    ChatMessageSchema,
    LlmConfig
)
from langchain_mcp_adapters.client import MultiServerMCPClient


servers = MultiServerMCPClient({
    "sample_server": {
        "url": "http://127.0.0.1:8008/mcp",
        "transport": "streamable_http",
    }
})


class McpChatService:
    @staticmethod
    async def handle_mcp_chat(
        query: str,
    ):
        system_instruction = """
You are a helpful assistant that can call tools to answer user queries.
Please use the tools when necessary.
If the provided tools are not sufficient to answer the question, politely inform the user that you are unable to assist with that request.
When answering about tools unavailability, don't mention 'tools' or 'functions' terms, instead use the term 'services' or 'inquiries'.
        """

        config = LlmConfig(
            temperature=0.3,
        )
        messages = [
            ChatMessageSchema(
                role="user",
                content=query,
            )
        ]

        response = await McpChatHelper.handle_mcp_chat(
            model_name="llama3.2",
            system_instruction=system_instruction,
            config=config,
            mcp_servers=servers,
            messages=messages,
        )

        return response