from sqlmodel import SQLModel, Field
from datetime import datetime
from enum import Enum

class RoleEnum(str, Enum):
    user = "user"
    assistant = "assistant"

# Define the Message model using the same inheritance pattern as the working Task model
class MessageBase(SQLModel):
    conversation_id: str = Field(min_length=1)
    user_id: str = Field(min_length=1)
    role: RoleEnum = Field()
    content: str = Field(min_length=1)

class Message(MessageBase, table=True):
    __tablename__ = "messages"
    id: int = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)