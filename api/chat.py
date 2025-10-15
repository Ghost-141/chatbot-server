from fastapi import APIRouter, Depends, Body
from typing import Annotated
from core.dependency import get_chat_service
from models.schemas import ChatQuery, ChatResponse
from services.interface.chat_interface import ChatServiceInterface

router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("", response_model=ChatResponse)
async def start_chat(
    chat_query: Annotated[
        ChatQuery,
        Body(
            openapi_examples={
                "session-1": {
                    "summary": "Product information request",
                    "description": "User asking about kiwi.",
                    "value": {"message": "Tell me more about kiwi"},
                }
            }
        ),
    ],
    chat_service: ChatServiceInterface = Depends(get_chat_service),
) -> ChatResponse:
    return await chat_service.start_chat(chat_query.message)
