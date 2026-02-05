"""
Simple Todo Web App and Chatbot Backend
========================================

This is a simple backend for the Todo Web App and Todo Chatbot with minimal dependencies.
"""

from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware

# Security scheme
security = HTTPBearer()
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
import bcrypt
import os
import uuid
import json
import sqlite3
from contextlib import contextmanager
import re

# Security settings
SECRET_KEY = os.getenv("SECRET_KEY", "your-super-secret-key-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Database setup
DATABASE_FILE = "todo_chatbot_simple.db"

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Initialize FastAPI app
app = FastAPI(
    title="Simple Todo App & Chatbot API",
    description="Simple backend for Todo Web App and AI Chatbot",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database initialization
def init_db():
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()

    # Create users table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id TEXT PRIMARY KEY,
            email TEXT UNIQUE NOT NULL,
            hashed_password TEXT NOT NULL,
            first_name TEXT,
            last_name TEXT,
            role TEXT DEFAULT 'user',
            created_at TEXT,
            updated_at TEXT
        )
    """)

    # Create tasks table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT NOT NULL,
            title TEXT NOT NULL,
            description TEXT,
            status TEXT DEFAULT 'pending',
            is_completed BOOLEAN DEFAULT 0,
            created_at TEXT,
            updated_at TEXT,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    """)

    # Create conversations table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS conversations (
            id TEXT PRIMARY KEY,
            user_id TEXT NOT NULL,
            title TEXT,
            created_at TEXT,
            updated_at TEXT,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    """)

    # Create messages table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id TEXT PRIMARY KEY,
            conversation_id TEXT NOT NULL,
            user_id TEXT NOT NULL,
            role TEXT NOT NULL,
            content TEXT NOT NULL,
            created_at TEXT,
            FOREIGN KEY (conversation_id) REFERENCES conversations (id),
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    """)

    conn.commit()
    conn.close()

# Initialize database
init_db()

# Models
class Token(BaseModel):
    access_token: str
    token_type: str

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
    role: str = "user"

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
    created_at: str
    updated_at: str

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
    """Hash a password directly using bcrypt, ensuring it's not longer than 72 bytes"""
    # Ensure password is not longer than 72 bytes before hashing
    password_bytes = password.encode('utf-8')
    if len(password_bytes) > 72:
        # Truncate to 72 bytes max
        password_bytes = password_bytes[:72]
        # Decode back to string, handling potential multi-byte character issues
        password = password_bytes.decode('utf-8', errors='ignore')
    else:
        password = password_bytes.decode('utf-8')

    # Hash with bcrypt
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against a hash using bcrypt directly"""
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            return None
        return user_id
    except JWTError:
        return None

def verify_user_access(current_user_id: str, requested_user_id: str):
    if current_user_id != requested_user_id:
        raise HTTPException(
            status_code=403,
            detail="Not authorized to access this resource"
        )

# Database helper functions
@contextmanager
def get_db():
    conn = sqlite3.connect(DATABASE_FILE)
    conn.row_factory = sqlite3.Row  # Enable column access by name
    try:
        yield conn
    finally:
        conn.close()

# Authentication endpoints
@app.post("/auth/signup", response_model=UserResponse)
async def signup(user_data: UserCreate):
    with get_db() as conn:
        cursor = conn.cursor()

        # Check if user already exists
        cursor.execute("SELECT id FROM users WHERE email = ?", (user_data.email,))
        existing_user = cursor.fetchone()
        if existing_user:
            raise HTTPException(
                status_code=409,
                detail="Email already registered"
            )

        # Create new user
        user_id = str(uuid.uuid4())
        hashed_password = get_password_hash(user_data.password)
        created_at = datetime.utcnow().isoformat()

        cursor.execute("""
            INSERT INTO users (id, email, hashed_password, first_name, last_name, role, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (user_id, user_data.email, hashed_password, user_data.first_name, user_data.last_name, "user", created_at, created_at))

        conn.commit()

        return UserResponse(
            id=user_id,
            email=user_data.email,
            first_name=user_data.first_name,
            last_name=user_data.last_name,
            role="user"
        )

@app.post("/auth/login", response_model=Token)
async def login(login_data: UserLogin):
    with get_db() as conn:
        cursor = conn.cursor()

        # Get user from database
        cursor.execute("SELECT id, hashed_password FROM users WHERE email = ?", (login_data.email,))
        user_row = cursor.fetchone()

        if not user_row or not verify_password(login_data.password, user_row['hashed_password']):
            raise HTTPException(
                status_code=401,
                detail="Incorrect email or password"
            )

        user_id = user_row['id']
        access_token = create_access_token(data={"sub": user_id})

        return {"access_token": access_token, "token_type": "bearer"}

# Task endpoints (for web app)
@app.get("/users/{user_id}/tasks", response_model=List[TaskResponse])
async def get_tasks(user_id: str, credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    current_user_id = verify_token(token)
    if not current_user_id:
        raise HTTPException(status_code=401, detail="Invalid token")

    verify_user_access(current_user_id, user_id)

    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, user_id, title, description, is_completed, created_at, updated_at
            FROM tasks WHERE user_id = ?
            ORDER BY created_at DESC
        """, (user_id,))

        tasks = cursor.fetchall()

        return [
            TaskResponse(
                id=task['id'],
                user_id=task['user_id'],
                title=task['title'],
                description=task['description'],
                is_completed=bool(task['is_completed']),
                created_at=task['created_at'],
                updated_at=task['updated_at']
            )
            for task in tasks
        ]

@app.post("/users/{user_id}/tasks", response_model=TaskResponse)
async def create_task(user_id: str, task_data: TaskCreate, credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    current_user_id = verify_token(token)
    if not current_user_id:
        raise HTTPException(status_code=401, detail="Invalid token")

    verify_user_access(current_user_id, user_id)

    with get_db() as conn:
        cursor = conn.cursor()
        created_at = datetime.utcnow().isoformat()

        cursor.execute("""
            INSERT INTO tasks (user_id, title, description, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?)
        """, (user_id, task_data.title, task_data.description, created_at, created_at))

        task_id = cursor.lastrowid
        conn.commit()

        # Return the created task
        cursor.execute("""
            SELECT id, user_id, title, description, is_completed, created_at, updated_at
            FROM tasks WHERE id = ?
        """, (task_id,))

        task = cursor.fetchone()

        return TaskResponse(
            id=task['id'],
            user_id=task['user_id'],
            title=task['title'],
            description=task['description'],
            is_completed=bool(task['is_completed']),
            created_at=task['created_at'],
            updated_at=task['updated_at']
        )

@app.put("/users/{user_id}/tasks/{task_id}", response_model=TaskResponse)
async def update_task(user_id: str, task_id: int, task_data: TaskUpdate, credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    current_user_id = verify_token(token)
    if not current_user_id:
        raise HTTPException(status_code=401, detail="Invalid token")

    verify_user_access(current_user_id, user_id)

    with get_db() as conn:
        cursor = conn.cursor()

        # Get the task to update
        cursor.execute("SELECT user_id FROM tasks WHERE id = ?", (task_id,))
        task = cursor.fetchone()

        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
        if task['user_id'] != user_id:
            raise HTTPException(status_code=403, detail="Not authorized to update this task")

        # Prepare update data
        update_fields = []
        params = []

        if task_data.title is not None:
            update_fields.append("title = ?")
            params.append(task_data.title)
        if task_data.description is not None:
            update_fields.append("description = ?")
            params.append(task_data.description)
        if task_data.is_completed is not None:
            update_fields.append("is_completed = ?")
            params.append(int(task_data.is_completed))

        update_fields.append("updated_at = ?")
        params.append(datetime.utcnow().isoformat())
        params.append(task_id)

        if update_fields:
            query = f"UPDATE tasks SET {', '.join(update_fields)} WHERE id = ?"
            cursor.execute(query, params)
            conn.commit()

        # Return updated task
        cursor.execute("""
            SELECT id, user_id, title, description, is_completed, created_at, updated_at
            FROM tasks WHERE id = ?
        """, (task_id,))

        updated_task = cursor.fetchone()

        return TaskResponse(
            id=updated_task['id'],
            user_id=updated_task['user_id'],
            title=updated_task['title'],
            description=updated_task['description'],
            is_completed=bool(updated_task['is_completed']),
            created_at=updated_task['created_at'],
            updated_at=updated_task['updated_at']
        )

@app.delete("/users/{user_id}/tasks/{task_id}")
async def delete_task(user_id: str, task_id: int, credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    current_user_id = verify_token(token)
    if not current_user_id:
        raise HTTPException(status_code=401, detail="Invalid token")

    verify_user_access(current_user_id, user_id)

    with get_db() as conn:
        cursor = conn.cursor()

        # Check if task exists and belongs to user
        cursor.execute("SELECT user_id FROM tasks WHERE id = ?", (task_id,))
        task = cursor.fetchone()

        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
        if task['user_id'] != user_id:
            raise HTTPException(status_code=403, detail="Not authorized to delete this task")

        cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        conn.commit()

        return {"message": "Task deleted successfully"}

@app.patch("/users/{user_id}/tasks/{task_id}/complete", response_model=TaskResponse)
async def toggle_task_completion(user_id: str, task_id: int, completion_data: Dict[str, bool], credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    current_user_id = verify_token(token)
    if not current_user_id:
        raise HTTPException(status_code=401, detail="Invalid token")

    verify_user_access(current_user_id, user_id)

    is_completed = completion_data.get("is_completed", False)

    with get_db() as conn:
        cursor = conn.cursor()

        # Check if task exists and belongs to user
        cursor.execute("SELECT user_id FROM tasks WHERE id = ?", (task_id,))
        task = cursor.fetchone()

        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
        if task['user_id'] != user_id:
            raise HTTPException(status_code=403, detail="Not authorized to update this task")

        # Update completion status
        updated_at = datetime.utcnow().isoformat()
        cursor.execute("""
            UPDATE tasks
            SET is_completed = ?, updated_at = ?
            WHERE id = ?
        """, (int(is_completed), updated_at, task_id))

        conn.commit()

        # Return updated task
        cursor.execute("""
            SELECT id, user_id, title, description, is_completed, created_at, updated_at
            FROM tasks WHERE id = ?
        """, (task_id,))

        updated_task = cursor.fetchone()

        return TaskResponse(
            id=updated_task['id'],
            user_id=updated_task['user_id'],
            title=updated_task['title'],
            description=updated_task['description'],
            is_completed=bool(updated_task['is_completed']),
            created_at=updated_task['created_at'],
            updated_at=updated_task['updated_at']
        )

# Chat endpoints (for chatbot)
@app.post("/users/{user_id}/chat", response_model=ChatResponse)
async def chat_endpoint(user_id: str, chat_message: ChatMessage, credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer(auto_error=False))):
    # Extract token from credentials if available
    token = credentials.credentials if credentials else None
    if token:
        current_user_id = verify_token(token)
        if not current_user_id:
            raise HTTPException(status_code=401, detail="Invalid token")
    else:
        # If no token is provided, we'll assume the user_id in the URL is valid
        # In a real application, you might want to implement a different authentication scheme
        current_user_id = user_id

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
            with get_db() as conn:
                cursor = conn.cursor()
                created_at = datetime.utcnow().isoformat()

                cursor.execute("""
                    INSERT INTO tasks (user_id, title, created_at, updated_at)
                    VALUES (?, ?, ?, ?)
                """, (user_id, task_title, created_at, created_at))

                conn.commit()

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
                with get_db() as conn:
                    cursor = conn.cursor()
                    created_at = datetime.utcnow().isoformat()

                    cursor.execute("""
                        INSERT INTO tasks (user_id, title, created_at, updated_at)
                        VALUES (?, ?, ?, ?)
                    """, (user_id, task_title, created_at, created_at))

                    conn.commit()

                response = f"I've added the task '{task_title}' to your list."
            else:
                response = "I understood you wanted to add a task, but I couldn't identify what task to add."
    elif "list" in message_text or "show" in message_text or "my tasks" in message_text or "what" in message_text:
        # Get user's tasks
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, title, is_completed
                FROM tasks
                WHERE user_id = ?
                ORDER BY created_at DESC
            """, (user_id,))

            tasks = cursor.fetchall()

            if tasks:
                if "completed" in message_text or "done" in message_text:
                    # Show only completed tasks
                    completed_tasks = [task for task in tasks if task['is_completed']]
                    if completed_tasks:
                        task_list = "\n".join([f"- {task['id']}: {task['title']}" for task in completed_tasks])
                        response = f"Here are your completed tasks:\n{task_list}"
                    else:
                        response = "You don't have any completed tasks yet."
                elif "pending" in message_text or "not done" in message_text:
                    # Show only pending tasks
                    pending_tasks = [task for task in tasks if not task['is_completed']]
                    if pending_tasks:
                        task_list = "\n".join([f"- {task['id']}: {task['title']}" for task in pending_tasks])
                        response = f"Here are your pending tasks:\n{task_list}"
                    else:
                        response = "You don't have any pending tasks."
                else:
                    # Show all tasks
                    task_list = "\n".join([f"- {task['id']}: {task['title']} ({'completed' if task['is_completed'] else 'pending'})" for task in tasks])
                    response = f"Here are your tasks:\n{task_list}"
            else:
                response = "You don't have any tasks yet."
    elif "complete" in message_text or "done" in message_text or "finish" in message_text:
        # Extract task ID (simplified)
        numbers = re.findall(r'\d+', message_text)
        if numbers:
            task_id = int(numbers[0])

            # Update task as completed
            with get_db() as conn:
                cursor = conn.cursor()

                cursor.execute("""
                    UPDATE tasks
                    SET is_completed = 1, updated_at = ?
                    WHERE id = ? AND user_id = ?
                """, (datetime.utcnow().isoformat(), task_id, user_id))

                if cursor.rowcount > 0:
                    response = f"I've marked task {task_id} as completed."
                else:
                    response = f"Task {task_id} not found or doesn't belong to you."
        else:
            response = "I understood you wanted to complete a task, but I couldn't identify which task. Please specify the task number."
    elif "delete" in message_text or "remove" in message_text or "cancel" in message_text:
        # Extract task ID to delete
        numbers = re.findall(r'\d+', message_text)
        if numbers:
            task_id = int(numbers[0])

            # Delete task
            with get_db() as conn:
                cursor = conn.cursor()

                cursor.execute("DELETE FROM tasks WHERE id = ? AND user_id = ?", (task_id, user_id))

                if cursor.rowcount > 0:
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
    with get_db() as conn:
        cursor = conn.cursor()

        # Check if conversation exists
        cursor.execute("SELECT id FROM conversations WHERE id = ?", (conversation_id,))
        existing_conversation = cursor.fetchone()

        if not existing_conversation:
            created_at = datetime.utcnow().isoformat()
            cursor.execute("""
                INSERT INTO conversations (id, user_id, created_at, updated_at)
                VALUES (?, ?, ?, ?)
            """, (conversation_id, user_id, created_at, created_at))

        # Save user message
        created_at = datetime.utcnow().isoformat()
        cursor.execute("""
            INSERT INTO messages (id, conversation_id, user_id, role, content, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (str(uuid.uuid4()), conversation_id, user_id, "user", chat_message.message, created_at))

        # Save AI response
        cursor.execute("""
            INSERT INTO messages (id, conversation_id, user_id, role, content, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (str(uuid.uuid4()), conversation_id, user_id, "assistant", response, created_at))

        conn.commit()

    return ChatResponse(
        conversation_id=conversation_id,
        response=response,
        task_action=task_action
    )

@app.get("/")
def read_root():
    return {"message": "Simple Todo App & Chatbot API", "status": "running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8002)