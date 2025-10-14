from fastapi import APIRouter, Depends

router = APIRouter(prefix="/chat", tags=["chat"])

@router.post('start_chat')
async def start_chat() -> None:
    
    
