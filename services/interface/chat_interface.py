from abc import ABC, abstractmethod
from models.schemas import ChatQuery


class ChatServiceInterface(ABC):
    @abstractmethod
    async def start_chat(
        self, message: str) -> ChatQuery:
        raise NotImplementedError()
