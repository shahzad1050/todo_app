from sqlmodel import SQLModel, Field
from datetime import datetime

class ConversationBase(SQLModel):
    user_id: str = Field(...)

class Conversation(ConversationBase, table=True):
    __tablename__ = "conversations"
    id: str = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Update updated_at timestamp before each update
    def __setattr__(self, name, value):
        if name == "updated_at":
            super().__setattr__(name, datetime.utcnow())
        elif name != "updated_at":
            super().__setattr__(name, value)