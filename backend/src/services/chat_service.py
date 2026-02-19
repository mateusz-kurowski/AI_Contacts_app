import json

import litellm

# Import to ensure API key & settings are loaded
import src.model.litellm_client  # noqa: F401
from src.config.config import model_config
from src.services.mpc_client import get_mcp_client


class ChatService:
    def __init__(self, model: str = model_config.model_id):
        self._model = model
        self._system_instruction = model_config.system_instruction
        self._api_base = model_config.api_base
        self._mcp_client = get_mcp_client()

    def _build_messages(self, user_input: str) -> list[dict]:
        return [
            {"role": "system", "content": self._system_instruction},
            {"role": "user", "content": user_input},
        ]

    async def _get_mcp_tools(self) -> list[dict]:
        """Fetch tool definitions from MCP and convert to OpenAI function-calling format."""
        tools = await self._mcp_client.list_tools()
        openai_tools = []
        for tool in tools:
            openai_tools.append(
                {
                    "type": "function",
                    "function": {
                        "name": tool.name,
                        "description": tool.description or "",
                        "parameters": tool.inputSchema,
                    },
                }
            )
        return openai_tools

    async def get_chat_response_with_mcp(self, user_input: str) -> str:
        """Generate response with MCP tools available (agentic loop)."""
        async with self._mcp_client:
            tools = await self._get_mcp_tools()
            messages = self._build_messages(user_input)

            # Agentic loop: keep going while the model calls tools
            while True:
                response = await litellm.acompletion(
                    model=self._model,
                    messages=messages,
                    tools=tools if tools else None,
                    api_base=self._api_base,
                )
                choice = response.choices[0]

                if choice.finish_reason == "tool_calls" and choice.message.tool_calls:
                    # Append assistant message with tool calls
                    messages.append(choice.message.model_dump())

                    # Execute each tool call via MCP
                    for tool_call in choice.message.tool_calls:
                        fn = tool_call.function
                        args = json.loads(fn.arguments) if fn.arguments else {}
                        result = await self._mcp_client.call_tool(fn.name, args)

                        # Collect text from MCP result content blocks
                        result_text = "\n".join(
                            block.text
                            for block in result.content
                            if hasattr(block, "text")
                        )

                        messages.append(
                            {
                                "role": "tool",
                                "tool_call_id": tool_call.id,
                                "content": result_text,
                            }
                        )
                else:
                    # Model produced a final text response
                    return choice.message.content or ""

    async def get_chat_response_async(self, user_input: str) -> str:
        """Async completion without MCP tools."""
        messages = self._build_messages(user_input)
        response = await litellm.acompletion(
            model=self._model,
            messages=messages,
            api_base=self._api_base,
        )
        return response.choices[0].message.content or ""

    def get_chat_response(self, user_input: str) -> str:
        """Synchronous completion without MCP tools."""
        messages = self._build_messages(user_input)
        response = litellm.completion(
            model=self._model,
            messages=messages,
            api_base=self._api_base,
        )
        return response.choices[0].message.content or ""


def get_chat_service() -> ChatService:
    return ChatService()
