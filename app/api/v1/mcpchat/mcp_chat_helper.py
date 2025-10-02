from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_mcp_adapters.tools import load_mcp_tools
from langgraph.prebuilt import create_react_agent
from langchain_ollama.chat_models import ChatOllama
from app.models.v1.chat.llm_chat_schema import (
    CompletionMessageSchema,
    ChatMessageSchema,
    LlmConfig
)


class McpChatHelper:
    @staticmethod
    async def handle_mcp_chat(
        model_name: str,
        system_instruction: str,
        config: LlmConfig,
        mcp_servers: MultiServerMCPClient,
        messages: list[ChatMessageSchema],
    ):
        llm = ChatOllama(
            model=model_name,
            temperature=config.temperature,
            top_k=config.top_k,
            top_p=config.top_p,
            
        )

        tools = await mcp_servers.get_tools()
        agent = create_react_agent(
            model=llm,
            tools=tools,
            prompt=system_instruction,
        )

        inputs = {"messages": [
            item.__dict__ for item in messages
        ]}

        tool_results = []
        agent_results = []

        async for output in agent.astream(inputs, stream_mode="updates"):
            response_from = list(output.keys())[0]
            response_message = output[response_from]["messages"][0]
            if response_from == "tools":
                tool_results.append({
                    "tool_name": response_message.name,
                    "tool_input": response_message.content,
                })

            elif response_from == "agent":
                agent_results.append(response_message)

        final_result = agent_results[-1]
        
        returned_dict = {
            "model": model_name,
            "done": final_result.response_metadata['done'],
            "done_reason": final_result.response_metadata['done_reason'],
            "usage": {
                "input_token_count": final_result.response_metadata['prompt_eval_count'],
                "output_token_count": final_result.response_metadata['eval_count'],
            },
            "messages": {
                "role": "assistant",
                "message": final_result.content,
                "tool_calls": agent_results[0].response_metadata.get('tool_calls', []),
            },
            "tool_results": tool_results,
        }

        return returned_dict
