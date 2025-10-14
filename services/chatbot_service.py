from services.chat_interface import ChatServiceInterface
from models.schemas import ChatQuery

class ChatService(ChatServiceInterface):
    async def start_chat(self, message: str) -> None:
        return None
