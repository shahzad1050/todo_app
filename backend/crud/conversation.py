from sqlmodel import Session, select
from typing import List, Optional
from ..models.conversation import Conversation, ConversationBase

def create_conversation(session: Session, conversation: ConversationBase) -> Conversation:
    """
    Create a new conversation in the database
    """
    db_conv = Conversation(
        user_id=conversation.user_id
    )
    session.add(db_conv)
    session.commit()
    session.refresh(db_conv)
    return db_conv

def get_conversation_by_id(session: Session, conv_id: str) -> Optional[Conversation]:
    """
    Get a conversation by its ID
    """
    statement = select(Conversation).where(Conversation.id == conv_id)
    return session.exec(statement).first()

def get_conversations_by_user(session: Session, user_id: str) -> List[Conversation]:
    """
    Get all conversations for a specific user
    """
    statement = select(Conversation).where(Conversation.user_id == user_id).order_by(Conversation.updated_at.desc())
    return session.exec(statement).all()

def update_conversation(session: Session, conv_id: str, conv_data: ConversationBase) -> Optional[Conversation]:
    """
    Update an existing conversation
    """
    db_conv = get_conversation_by_id(session, conv_id)
    if not db_conv:
        return None

    # Update fields if provided
    if hasattr(conv_data, 'user_id') and conv_data.user_id:
        db_conv.user_id = conv_data.user_id

    session.add(db_conv)
    session.commit()
    session.refresh(db_conv)
    return db_conv

def delete_conversation(session: Session, conv_id: str) -> bool:
    """
    Delete a conversation by its ID
    """
    db_conv = get_conversation_by_id(session, conv_id)
    if not db_conv:
        return False

    session.delete(db_conv)
    session.commit()
    return True