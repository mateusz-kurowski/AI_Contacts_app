from src.model.gemini import gemma_client, default_config
from google import genai
from src.config.config import app_config


class ChatService:
    def __init__(
        self, genai_client: genai.Client | None = None, model: str = app_config.model_id
    ):
        self._client = genai_client or gemma_client
        self._model = model
        self._config = default_config

    def get_chat_response(self, user_input: str) -> str:
        resp = self._client.models.generate_content(
            model=self._model, contents=user_input, config=self._config
        )
        return resp.text or ""

def get_chat_service() -> ChatService:
    return ChatService()