from datetime import datetime, timezone
from uuid import uuid4

from fastapi import Depends
from fastapi.routing import APIRouter

from src.db.schemas import ChatResponse, NewChatMessage
from src.services.chat_service import ChatService

chat_router = APIRouter(prefix="/chat", tags=["chat"])


def get_chat_service() -> ChatService:
    return ChatService()


@chat_router.post("/", response_model=ChatResponse)
def read_chat(input: NewChatMessage, svc: ChatService = Depends(get_chat_service)):
    response = svc.get_chat_response(input.content)
    # Return ISO string
    current_timestamp = datetime.now(timezone.utc).isoformat()
    return ChatResponse(
        content=response, id=str(uuid4()), role="assistant", createdAt=current_timestamp
    )
