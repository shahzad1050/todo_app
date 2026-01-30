# Quickstart Guide: AI-Powered Todo Chatbot

**Feature**: AI-Powered Todo Chatbot
**Date**: 2026-01-28
**Version**: 1.0

## Prerequisites

- Python 3.11+
- pip package manager
- Access to OpenAI API key
- Neon Serverless PostgreSQL database
- Better Auth account (or local setup)

## Environment Setup

### 1. Clone and Navigate to Project
```bash
git clone <repository-url>
cd <project-directory>
```

### 2. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install fastapi uvicorn sqlmodel openai python-multipart python-jose[cryptography] passlib[bcrypt]
pip install psycopg2-binary  # For PostgreSQL
pip install better-auth  # Or equivalent auth solution
```

### 4. Environment Variables
Create a `.env` file in the project root:

```env
OPENAI_API_KEY=your_openai_api_key_here
DATABASE_URL=postgresql+psycopg2://username:password@host:port/database_name
SECRET_KEY=your_secret_key_for_jwt_tokens
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

## Running the Application

### 1. Database Setup
```bash
# Run database migrations (if using alembic)
alembic upgrade head

# Or initialize database directly
python -m backend.core.database
```

### 2. Start the Server
```bash
uvicorn backend.main:app --reload --port 8000
```

The application will be available at `http://localhost:8000`

### 3. API Documentation
Access the auto-generated API documentation at:
- `http://localhost:8000/docs` - Swagger UI
- `http://localhost:8000/redoc` - ReDoc

## Testing the Chat Interface

### 1. Authentication
First, register or login to obtain an authentication token:
```bash
POST /auth/login
{
  "username": "your_username",
  "password": "your_password"
}
```

### 2. Chat Endpoint
Send a message to the chat endpoint:
```bash
POST /api/{user_id}/chat
Headers: Authorization: Bearer {token}
{
  "message": "Add a task to buy groceries",
  "conversation_id": "optional_conversation_id"
}
```

### 3. Expected Response
```json
{
  "conversation_id": "generated_or_provided_conversation_id",
  "response": "I've added the task 'buy groceries' to your list.",
  "tool_calls": [
    {
      "tool_name": "add_task",
      "result": {"task_id": "uuid", "title": "buy groceries", "status": "added"}
    }
  ]
}
```

## Key Components

### MCP Tools
Located in `backend/mcp/tools.py`:
- `add_task()` - Creates new tasks
- `list_tasks()` - Retrieves user's tasks
- `update_task()` - Modifies existing tasks
- `delete_task()` - Removes tasks
- `complete_task()` - Marks tasks as complete

### AI Agent Service
Located in `backend/services/ai_agent.py`:
- Processes natural language input
- Maps intents to MCP tools
- Generates contextual responses

### Database Models
Located in `backend/models/`:
- `task.py` - Task entity
- `conversation.py` - Conversation entity
- `message.py` - Message entity

## Troubleshooting

### Common Issues

1. **OpenAI API Connection**: Verify your API key is correct and has sufficient credits
2. **Database Connection**: Check your DATABASE_URL configuration
3. **Authentication Errors**: Ensure proper token is passed in headers
4. **Intent Recognition**: Natural language may not match expected patterns

### Development Tips

- Use the `/docs` endpoint to test API endpoints manually
- Enable debug logging by setting `DEBUG=True` in environment
- Monitor the database directly to verify conversation and task persistence