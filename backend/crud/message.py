from sqlmodel import Session, select
from typing import List, Optional
from ..models.message import Message, MessageBase, RoleEnum

def create_message(session: Session, message: MessageBase) -> Message:
    """
    Create a new message in the database
    """
    db_msg = Message(
        conversation_id=message.conversation_id,
        user_id=message.user_id,
        role=message.role,
        content=message.content
    )
    session.add(db_msg)
    session.commit()
    session.refresh(db_msg)
    return db_msg

def get_message_by_id(session: Session, msg_id: str) -> Optional[Message]:
    """
    Get a message by its ID
    """
    statement = select(Message).where(Message.id == msg_id)
    return session.exec(statement).first()

def get_messages_by_conversation(session: Session, conversation_id: str) -> List[Message]:
    """
    Get all messages for a specific conversation
    """
    statement = select(Message).where(Message.conversation_id == conversation_id).order_by(Message.created_at.asc())
    return session.exec(statement).all()

def get_messages_by_user(session: Session, user_id: str) -> List[Message]:
    """
    Get all messages for a specific user
    """
    statement = select(Message).where(Message.user_id == user_id).order_by(Message.created_at.desc())
    return session.exec(statement).all()

def delete_message(session: Session, msg_id: str) -> bool:
    """
    Delete a message by its ID
    """
    db_msg = get_message_by_id(session, msg_id)
    if not db_msg:
        return False

    session.delete(db_msg)
    session.commit()
    return True