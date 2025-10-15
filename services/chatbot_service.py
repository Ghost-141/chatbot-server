from services.interface.chat_interface import ChatServiceInterface
from models.schemas import ChatResponse
from utils.groq_client import run_chat_query

class ChatService(ChatServiceInterface):
    async def start_chat(self, message: str) -> ChatResponse:
        response = run_chat_query(message)
        return ChatResponse(model_response=response)
