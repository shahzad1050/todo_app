from sqlmodel import Session, select
from typing import List, Optional
from ..models.conversation import Conversation, ConversationBase
from uuid import UUID

def create_conversation(session: Session, conversation: ConversationBase) -> Conversation:
    """
    Create a new conversation in the database
    """
    db_conv = Conversation.from_orm(conversation) if hasattr(Conversation, 'from_orm') else Conversation(**conversation.dict())
    session.add(db_conv)
    session.commit()
    session.refresh(db_conv)
    return db_conv

def get_conversation_by_id(session: Session, conv_id: UUID) -> Optional[Conversation]:
    """
    Get a conversation by its ID
    """
    statement = select(Conversation).where(Conversation.id == conv_id)
    return session.exec(statement).first()

def get_conversations_by_user(session: Session, user_id: UUID) -> List[Conversation]:
    """
    Get all conversations for a specific user
    """
    statement = select(Conversation).where(Conversation.user_id == user_id).order_by(Conversation.updated_at.desc())
    return session.exec(statement).all()

def update_conversation(session: Session, conv_id: UUID, conv_data: ConversationBase) -> Optional[Conversation]:
    """
    Update an existing conversation
    """
    db_conv = get_conversation_by_id(session, conv_id)
    if not db_conv:
        return None

    update_data = conv_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_conv, field, value)

    session.add(db_conv)
    session.commit()
    session.refresh(db_conv)
    return db_conv

def delete_conversation(session: Session, conv_id: UUID) -> bool:
    """
    Delete a conversation by its ID
    """
    db_conv = get_conversation_by_id(session, conv_id)
    if not db_conv:
        return False

    session.delete(db_conv)
    session.commit()
    return True