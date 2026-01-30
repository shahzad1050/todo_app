import sys
import os
from pathlib import Path
# Add backend directory to path to resolve relative imports
backend_dir = Path(__file__).parent.parent
backend_path = str(backend_dir.resolve())
if backend_path not in sys.path:
    sys.path.insert(0, backend_path)

from fastapi import APIRouter, Depends, HTTPException, status
from typing import Dict, Any
from uuid import UUID
from pydantic import BaseModel
from core.security import get_current_user
from services.chat_service import ChatService

router = APIRouter()
chat_service = ChatService()

class ChatRequest(BaseModel):
    message: str
    conversation_id: str = None

@router.post("/users/{user_id}/chat")
async def chat_endpoint(
    user_id: str,
    request: ChatRequest
) -> Dict[str, Any]:
    """
    Chat endpoint that processes natural language and returns AI response
    """
    # Note: user_id validation happens inside chat_service.process_chat_message
    try:
        result = chat_service.process_chat_message(user_id, request.message, request.conversation_id)
        return result
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred processing your request: {str(e)}"
        )