"""
Integrated Todo Web App and Chatbot Backend
===========================================

This backend integrates both the Todo Web App and Todo Chatbot into a single system
with shared authentication and data layer.
"""

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlmodel import SQLModel, Field, create_engine, Session, select
from sqlmodel.ext.asyncio.session import AsyncSession
from contextlib import asynccontextmanager
import os
import uuid
import asyncio
import httpx
from enum import Enum
import re

# Security settings
SECRET_KEY = os.getenv("SECRET_KEY", "your-super-secret-key-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Database setup
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./todo_chatbot.db")
engine = create_engine(DATABASE_URL, echo=True)

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Initialize FastAPI app
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create database tables
    SQLModel.metadata.create_all(bind=engine)
    yield

app = FastAPI(
    title="Integrated Todo App & Chatbot API",
    description="Unified backend for Todo Web App and AI Chatbot",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Enums
class UserRole(str, Enum):
    admin = "admin"
    user = "user"

class TaskStatus(str, Enum):
    pending = "pending"
    in_progress = "in_progress"
    completed = "completed"

class MessageRole(str, Enum):
    user = "user"
    assistant = "assistant"

# Models
class User(SQLModel, table=True):
    __tablename__ = "users"

    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    email: str = Field(sa_column_kwargs={"unique": True, "index": True})
    hashed_password: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    role: str = UserRole.user.value
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class Task(SQLModel, table=True):
    __tablename__ = "tasks"

    id: int = Field(default=None, primary_key=True)
    user_id: str = Field(sa_column_kwargs={"index": True})  # Foreign key reference to User
    title: str
    description: Optional[str] = None
    status: str = TaskStatus.pending.value
    is_completed: bool = False
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class Conversation(SQLModel, table=True):
    __tablename__ = "conversations"

    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    user_id: str = Field(sa_column_kwargs={"index": True})  # Foreign key reference to User
    title: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class Message(SQLModel, table=True):
    __tablename__ = "messages"

    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    conversation_id: str = Field(sa_column_kwargs={"index": True})  # Foreign key reference to Conversation
    user_id: str = Field(sa_column_kwargs={"index": True})  # Foreign key reference to User
    role: str
    content: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

# Pydantic models for API
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    user_id: str

class UserCreate(BaseModel):
    email: str
    password: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None

class UserLogin(BaseModel):
    email: str
    password: str

class UserResponse(BaseModel):
    id: str
    email: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    role: UserRole = UserRole.user

class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    is_completed: Optional[bool] = None

class TaskResponse(BaseModel):
    id: int
    user_id: str
    title: str
    description: Optional[str] = None
    is_completed: bool
    created_at: datetime
    updated_at: datetime

class ChatMessage(BaseModel):
    message: str
    conversation_id: Optional[str] = None

class ChatResponse(BaseModel):
    conversation_id: str
    response: str
    task_action: Optional[Dict[str, Any]] = None

# Security functions
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: str = None):  # Placeholder for dependency injection
    if token is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No authorization token provided",
            headers={"WWW-Authenticate": "Bearer"},
        )

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
        token_data = TokenData(user_id=user_id)
    except JWTError:
        raise credentials_exception

    # Here you would fetch the user from the database
    # For now, we'll just return the user_id
    return token_data.user_id

# Helper function to verify user access
def verify_user_access(current_user_id: str, requested_user_id: str):
    if current_user_id != requested_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this resource"
        )

# Authentication endpoints
@app.post("/auth/signup", response_model=UserResponse)
async def signup(user_data: UserCreate):
    # Check if user already exists
    with Session(engine) as session:
        existing_user = session.exec(select(User).where(User.email == user_data.email)).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email already registered"
            )

        # Create new user
        hashed_password = get_password_hash(user_data.password)
        user = User(
            email=user_data.email,
            hashed_password=hashed_password,
            first_name=user_data.first_name,
            last_name=user_data.last_name,
            role=UserRole.user.value
        )
        session.add(user)
        session.commit()
        session.refresh(user)

        return UserResponse(
            id=user.id,
            email=user.email,
            first_name=user.first_name,
            last_name=user.last_name,
            role=UserRole(user.role)
        )

@app.post("/auth/login", response_model=Token)
async def login(login_data: UserLogin):
    with Session(engine) as session:
        user = session.exec(select(User).where(User.email == login_data.email)).first()
        if not user or not verify_password(login_data.password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password"
            )

        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user.id}, expires_delta=access_token_expires
        )

        return {"access_token": access_token, "token_type": "bearer"}

# Task endpoints (for web app)
@app.get("/users/{user_id}/tasks", response_model=List[TaskResponse])
async def get_tasks(user_id: str, token: str = None):
    current_user_id = await get_current_user(token)
    verify_user_access(current_user_id, user_id)

    with Session(engine) as session:
        tasks = session.exec(select(Task).where(Task.user_id == user_id)).all()
        return [
            TaskResponse(
                id=task.id,
                user_id=task.user_id,
                title=task.title,
                description=task.description,
                is_completed=task.is_completed,
                created_at=task.created_at,
                updated_at=task.updated_at
            )
            for task in tasks
        ]

@app.post("/users/{user_id}/tasks", response_model=TaskResponse)
async def create_task(user_id: str, task_data: TaskCreate, token: str = None):
    current_user_id = await get_current_user(token)
    verify_user_access(current_user_id, user_id)

    with Session(engine) as session:
        task = Task(
            user_id=user_id,
            title=task_data.title,
            description=task_data.description,
            status=TaskStatus.pending.value
        )
        session.add(task)
        session.commit()
        session.refresh(task)

        return TaskResponse(
            id=task.id,
            user_id=task.user_id,
            title=task.title,
            description=task.description,
            is_completed=task.is_completed,
            created_at=task.created_at,
            updated_at=task.updated_at
        )

@app.put("/users/{user_id}/tasks/{task_id}", response_model=TaskResponse)
async def update_task(user_id: str, task_id: int, task_data: TaskUpdate, token: str = None):
    current_user_id = await get_current_user(token)
    verify_user_access(current_user_id, user_id)

    with Session(engine) as session:
        task = session.get(Task, task_id)
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
        if task.user_id != user_id:
            raise HTTPException(status_code=403, detail="Not authorized to update this task")

        # Update task
        if task_data.title is not None:
            task.title = task_data.title
        if task_data.description is not None:
            task.description = task_data.description
        if task_data.is_completed is not None:
            task.is_completed = task_data.is_completed

        task.updated_at = datetime.utcnow()
        session.add(task)
        session.commit()
        session.refresh(task)

        return TaskResponse(
            id=task.id,
            user_id=task.user_id,
            title=task.title,
            description=task.description,
            is_completed=task.is_completed,
            created_at=task.created_at,
            updated_at=task.updated_at
        )

@app.delete("/users/{user_id}/tasks/{task_id}")
async def delete_task(user_id: str, task_id: int, token: str = None):
    current_user_id = await get_current_user(token)
    verify_user_access(current_user_id, user_id)

    with Session(engine) as session:
        task = session.get(Task, task_id)
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
        if task.user_id != user_id:
            raise HTTPException(status_code=403, detail="Not authorized to delete this task")

        session.delete(task)
        session.commit()

        return {"message": "Task deleted successfully"}

@app.patch("/users/{user_id}/tasks/{task_id}/complete", response_model=TaskResponse)
async def toggle_task_completion(user_id: str, task_id: int, completion_data: Dict[str, bool], token: str = None):
    current_user_id = await get_current_user(token)
    verify_user_access(current_user_id, user_id)

    is_completed = completion_data.get("is_completed", False)

    with Session(engine) as session:
        task = session.get(Task, task_id)
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
        if task.user_id != user_id:
            raise HTTPException(status_code=403, detail="Not authorized to update this task")

        # Update completion status
        task.is_completed = is_completed
        task.updated_at = datetime.utcnow()
        session.add(task)
        session.commit()
        session.refresh(task)

        return TaskResponse(
            id=task.id,
            user_id=task.user_id,
            title=task.title,
            description=task.description,
            is_completed=task.is_completed,
            created_at=task.created_at,
            updated_at=task.updated_at
        )

# Chat endpoints (for chatbot)
@app.post("/users/{user_id}/chat", response_model=ChatResponse)
async def chat_endpoint(user_id: str, chat_message: ChatMessage, token: str = None):
    current_user_id = await get_current_user(token)
    verify_user_access(current_user_id, user_id)

    # This is a simplified implementation - in a real system, you'd connect to an AI service
    # For now, we'll just echo back the message with some simple processing
    message_text = chat_message.message.lower()

    # Simple intent detection
    task_action = None

    if "add" in message_text or "create" in message_text or "new" in message_text:
        # Extract task title (simplified)
        # Look for patterns like "add task buy groceries" or "create task to call mom"
        pattern = r'(?:add|create|make|new)\s+(?:task|a task|to)\s+(.+)'
        match = re.search(pattern, chat_message.message, re.IGNORECASE)

        if match:
            task_title = match.group(1).strip()
            # Clean up the title
            if task_title.endswith(".") or task_title.endswith("!") or task_title.endswith("?"):
                task_title = task_title[:-1]

            # Create task via API call (simulated)
            task_action = {
                "action": "create_task",
                "title": task_title,
                "user_id": user_id
            }

            # Simulate creating the task in the database
            with Session(engine) as session:
                task = Task(
                    user_id=user_id,
                    title=task_title,
                    status=TaskStatus.pending.value
                )
                session.add(task)
                session.commit()
                session.refresh(task)

            response = f"I've added the task '{task_title}' to your list."
        else:
            # Try to extract the task in a simpler way
            parts = message_text.split()
            if "add" in parts:
                idx = parts.index("add")
            elif "create" in parts:
                idx = parts.index("create")
            elif "new" in parts:
                idx = parts.index("new")
            else:
                idx = -1

            if idx >= 0 and idx < len(parts) - 1:
                task_title = " ".join(parts[idx + 1:])
                if task_title.endswith(".") or task_title.endswith("!") or task_title.endswith("?"):
                    task_title = task_title[:-1]

                # Create task via API call (simulated)
                task_action = {
                    "action": "create_task",
                    "title": task_title,
                    "user_id": user_id
                }

                # Simulate creating the task in the database
                with Session(engine) as session:
                    task = Task(
                        user_id=user_id,
                        title=task_title,
                        status=TaskStatus.pending.value
                    )
                    session.add(task)
                    session.commit()
                    session.refresh(task)

                response = f"I've added the task '{task_title}' to your list."
            else:
                response = "I understood you wanted to add a task, but I couldn't identify what task to add."
    elif "list" in message_text or "show" in message_text or "my tasks" in message_text or "what" in message_text:
        # Get user's tasks
        with Session(engine) as session:
            tasks = session.exec(select(Task).where(Task.user_id == user_id)).all()

            if tasks:
                if "completed" in message_text or "done" in message_text:
                    # Show only completed tasks
                    completed_tasks = [task for task in tasks if task.is_completed]
                    if completed_tasks:
                        task_list = "\n".join([f"- {task.id}: {task.title}" for task in completed_tasks])
                        response = f"Here are your completed tasks:\n{task_list}"
                    else:
                        response = "You don't have any completed tasks yet."
                elif "pending" in message_text or "not done" in message_text:
                    # Show only pending tasks
                    pending_tasks = [task for task in tasks if not task.is_completed]
                    if pending_tasks:
                        task_list = "\n".join([f"- {task.id}: {task.title}" for task in pending_tasks])
                        response = f"Here are your pending tasks:\n{task_list}"
                    else:
                        response = "You don't have any pending tasks."
                else:
                    # Show all tasks
                    task_list = "\n".join([f"- {task.id}: {task.title} ({'completed' if task.is_completed else 'pending'})" for task in tasks])
                    response = f"Here are your tasks:\n{task_list}"
            else:
                response = "You don't have any tasks yet."
    elif "complete" in message_text or "done" in message_text or "finish" in message_text:
        # Extract task ID (simplified)
        import re
        numbers = re.findall(r'\d+', message_text)
        if numbers:
            task_id = int(numbers[0])

            # Update task as completed
            with Session(engine) as session:
                task = session.get(Task, task_id)
                if task and task.user_id == user_id:
                    task.is_completed = True
                    task.updated_at = datetime.utcnow()
                    session.add(task)
                    session.commit()

                    response = f"I've marked task {task_id} as completed."
                else:
                    response = f"Task {task_id} not found or doesn't belong to you."
        else:
            response = "I understood you wanted to complete a task, but I couldn't identify which task. Please specify the task number."
    elif "delete" in message_text or "remove" in message_text or "cancel" in message_text:
        # Extract task ID to delete
        import re
        numbers = re.findall(r'\d+', message_text)
        if numbers:
            task_id = int(numbers[0])

            # Delete task
            with Session(engine) as session:
                task = session.get(Task, task_id)
                if task and task.user_id == user_id:
                    session.delete(task)
                    session.commit()

                    response = f"I've deleted task {task_id}."
                else:
                    response = f"Task {task_id} not found or doesn't belong to you."
        else:
            response = "I understood you wanted to delete a task, but I couldn't identify which task. Please specify the task number."
    elif "hello" in message_text or "hi" in message_text or "hey" in message_text:
        response = f"Hello! I'm your AI Todo assistant. You can ask me to add, list, update, delete, or complete tasks using natural language. What would you like to do?"
    else:
        response = f"I received your message: '{chat_message.message}'. I can help you manage your tasks using commands like 'Add task buy groceries' or 'Show my tasks'."

    # Create or retrieve conversation
    conversation_id = chat_message.conversation_id or str(uuid.uuid4())

    # Save the message to the conversation
    with Session(engine) as session:
        # Check if conversation exists
        conversation = session.get(Conversation, conversation_id)
        if not conversation:
            conversation = Conversation(id=conversation_id, user_id=user_id)
            session.add(conversation)

        # Save user message
        user_message = Message(
            conversation_id=conversation_id,
            user_id=user_id,
            role=MessageRole.user.value,
            content=chat_message.message
        )
        session.add(user_message)

        # Save AI response
        ai_message = Message(
            conversation_id=conversation_id,
            user_id=user_id,
            role=MessageRole.assistant.value,
            content=response
        )
        session.add(ai_message)

        session.commit()

    return ChatResponse(
        conversation_id=conversation_id,
        response=response,
        task_action=task_action
    )

@app.get("/")
def read_root():
    return {"message": "Integrated Todo App & Chatbot API", "status": "running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8002)