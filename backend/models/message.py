from sqlmodel import SQLModel, Field
from datetime import datetime
from enum import Enum

class RoleEnum(str, Enum):
    user = "user"
    assistant = "assistant"

class MessageBase(SQLModel):
    conversation_id: str = Field(...)
    user_id: str = Field(...)
    role: RoleEnum = Field(...)
    content: str = Field(...)

class Message(MessageBase, table=True):
    __tablename__ = "messages"
    id: str = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)