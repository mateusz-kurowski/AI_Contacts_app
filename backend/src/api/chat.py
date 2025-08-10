from datetime import datetime, timezone
from uuid import uuid4

from fastapi import Depends, HTTPException
from fastapi.routing import APIRouter
from pydantic import ValidationError

from src.db.schemas import ChatResponse, NewChatMessage
from src.services.chat_service import ChatService

router = APIRouter(prefix="/chat", tags=["chat"])


def get_chat_service() -> ChatService:
    return ChatService()


@router.post("/", response_model=ChatResponse)
@router.post("", response_model=ChatResponse)
def read_chat(input: NewChatMessage, svc: ChatService = Depends(get_chat_service)):
    try:
        print(input)
        response = svc.get_chat_response(input.content)
        # Return ISO string
        current_timestamp = datetime.now(timezone.utc).isoformat()
        return ChatResponse(
            content=response,
            id=str(uuid4()),
            role="assistant",
            createdAt=current_timestamp,
        )
    except ValidationError as e:
        raise HTTPException(status_code=422, detail=str(e))


@router.get("/hello", response_model=ChatResponse)
@router.get("hello", response_model=ChatResponse)
def get_hello_message(svc: ChatService = Depends(get_chat_service)):
    response = svc.get_chat_response("Hello! Please introduce yourself")
    current_timestamp = datetime.now(timezone.utc).isoformat()
    return ChatResponse(
        content=response, id=str(uuid4()), role="assistant", createdAt=current_timestamp
    )
