from abc import ABC, abstractmethod
from models.schemas import ChatResponse


class ChatServiceInterface(ABC):
    @abstractmethod
    async def start_chat(self, message: str) -> ChatResponse:
        raise NotImplementedError()
