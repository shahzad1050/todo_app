from typing import Dict, Any, List
from uuid import UUID
from sqlmodel import Session
import sys
import os
from pathlib import Path
# Add backend directory to path to resolve relative imports
backend_dir = Path(__file__).parent.parent
backend_path = str(backend_dir.resolve())
if backend_path not in sys.path:
    sys.path.insert(0, backend_path)

from core.database import engine
from models.message import MessageBase, RoleEnum
from models.conversation import ConversationBase
from crud.message import create_message, get_messages_by_conversation
from crud.conversation import create_conversation, get_conversation_by_id
from services.ai_agent import AIAgent
from datetime import datetime

class ChatService:
    """
    Service class to handle chat operations and conversation management
    """

    def __init__(self):
        self.ai_agent = AIAgent()

    def process_chat_message(self, user_id: str, message: str, conversation_id: str = None) -> Dict[str, Any]:
        """
        Process a chat message and return response with conversation context
        """
        with Session(engine) as session:
            # Create or retrieve conversation
            if conversation_id:
                try:
                    conv_uuid = UUID(conversation_id)
                    existing_conv = get_conversation_by_id(session, conv_uuid)
                    if not existing_conv or str(existing_conv.user_id) != user_id:
                        raise ValueError("Conversation not found or access denied")
                    conversation = existing_conv
                except ValueError:
                    raise ValueError("Invalid conversation ID format")
            else:
                # Create new conversation
                conv_base = ConversationBase(user_id=UUID(user_id))
                conversation = create_conversation(session, conv_base)
                conversation_id = str(conversation.id)

            # Save user message
            user_message = MessageBase(
                conversation_id=UUID(conversation_id),
                user_id=UUID(user_id),
                role=RoleEnum.user,
                content=message
            )
            saved_user_message = create_message(session, user_message)

            # Process message with AI agent
            ai_result = self.ai_agent.process_message(user_id, message)

            # Save AI response
            ai_message = MessageBase(
                conversation_id=UUID(conversation_id),
                user_id=UUID(user_id),  # AI responses are associated with the user
                role=RoleEnum.assistant,
                content=ai_result["response"]
            )
            saved_ai_message = create_message(session, ai_message)

            # Update conversation timestamp
            conversation.updated_at = datetime.utcnow()
            session.add(conversation)
            session.commit()

            return {
                "conversation_id": conversation_id,
                "response": ai_result["response"],
                "tool_calls": ai_result["tool_calls"],
                "timestamp": datetime.utcnow().isoformat()
            }

    def get_conversation_history(self, user_id: str, conversation_id: str) -> List[Dict[str, Any]]:
        """
        Retrieve conversation history for a specific conversation
        """
        with Session(engine) as session:
            # Verify that the user owns this conversation
            conv_uuid = UUID(conversation_id)
            conversation = get_conversation_by_id(session, conv_uuid)

            if not conversation or str(conversation.user_id) != user_id:
                raise ValueError("Conversation not found or access denied")

            # Get all messages in the conversation
            messages = get_messages_by_conversation(session, conv_uuid)

            # Format messages for response
            formatted_messages = []
            for msg in messages:
                formatted_messages.append({
                    "id": str(msg.id),
                    "role": msg.role.value,
                    "content": msg.content,
                    "created_at": msg.created_at.isoformat()
                })

            return formatted_messages

    def create_new_conversation(self, user_id: str) -> str:
        """
        Create a new conversation and return its ID
        """
        with Session(engine) as session:
            conv_base = ConversationBase(user_id=UUID(user_id))
            conversation = create_conversation(session, conv_base)
            return str(conversation.id)