from fastapi import Depends
from functools import lru_cache

from services.interface.chat_interface import ChatServiceInterface

@lru_cache()
def get_chat_service() -> ChatServiceInterface:
    return ChatService()
