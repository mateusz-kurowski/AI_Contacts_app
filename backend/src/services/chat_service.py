from src.model.gemini import google_client, default_config
from google import genai
from google.genai import types
from src.config.config import model_config
from src.services.mpc_client import get_mcp_client


class ChatService:
    def __init__(
        self,
        genai_client: genai.Client | None = None,
        model: str = model_config.model_id,
    ):
        self._client = genai_client or google_client
        self._model = model
        self._config = default_config
        self._mcp_client = get_mcp_client()

    async def get_chat_response_with_mcp(self, user_input: str) -> str:
        """Generate response with MCP tools available"""
        async with self._mcp_client:
            config_dict = model_config.model_client.model_dump(exclude={"tools"})
            mcp_config = types.GenerateContentConfig(
                **config_dict,
                tools=[self._mcp_client.session],
            )

            resp = await self._client.aio.models.generate_content(
                model=self._model,
                contents=user_input,
                config=mcp_config,
            )
            return resp.text or ""

    def get_chat_response(self, user_input: str) -> str:
        """Original method without MCP (synchronous)"""
        resp = self._client.models.generate_content(
            model=self._model,
            contents=user_input,
            config=self._config,
        )
        return resp.text or ""

    async def get_chat_response_async(self, user_input: str) -> str:
        """Async version without MCP"""
        resp = await self._client.aio.models.generate_content(
            model=self._model,
            contents=user_input,
            config=self._config,
        )
        return resp.text or ""


def get_chat_service() -> ChatService:
    return ChatService()
