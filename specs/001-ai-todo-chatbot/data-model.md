# Data Model: AI-Powered Todo Chatbot

**Feature**: AI-Powered Todo Chatbot
**Date**: 2026-01-28
**Model Version**: 1.0

## Entity Relationship Diagram

```
User (Better Auth) --< Task
User --< Conversation
Conversation --< Message
```

## Entity Definitions

### Task
Represents a todo item managed by the user

**Fields**:
- `id`: UUID | Primary Key | Auto-generated
- `user_id`: UUID | Foreign Key | References User
- `title`: String(255) | Required | Task title/description
- `description`: Text | Optional | Extended task details
- `completed`: Boolean | Default: False | Completion status
- `created_at`: DateTime | Auto-generated | Timestamp
- `updated_at`: DateTime | Auto-generated | Last update timestamp

**Relationships**:
- Belongs to: User (via user_id)
- Constraints: Unique combination of (user_id, id)

### Conversation
Represents an AI chat session with message history

**Fields**:
- `id`: UUID | Primary Key | Auto-generated
- `user_id`: UUID | Foreign Key | References User
- `created_at`: DateTime | Auto-generated | Session start time
- `updated_at`: DateTime | Auto-generated | Last activity timestamp

**Relationships**:
- Belongs to: User (via user_id)
- Has many: Messages (via conversation_id)
- Constraints: Unique combination of (user_id, id)

### Message
Represents individual messages in a conversation

**Fields**:
- `id`: UUID | Primary Key | Auto-generated
- `conversation_id`: UUID | Foreign Key | References Conversation
- `user_id`: UUID | Foreign Key | References User
- `role`: Enum('user', 'assistant') | Required | Sender type
- `content`: Text | Required | Message content
- `created_at`: DateTime | Auto-generated | Message timestamp

**Relationships**:
- Belongs to: Conversation (via conversation_id)
- Belongs to: User (via user_id)
- Constraints: Unique combination of (conversation_id, id)

## Database Indexes

### Task Table
- Index on `user_id` for efficient user-specific queries
- Index on `completed` for filtering completed/incomplete tasks
- Composite index on `(user_id, completed)` for common queries

### Conversation Table
- Index on `user_id` for user-specific conversation retrieval
- Index on `updated_at` for chronological ordering

### Message Table
- Index on `conversation_id` for conversation-specific queries
- Index on `user_id` for user-specific message retrieval
- Index on `created_at` for chronological ordering

## Business Rules

1. **Data Isolation**: All data access is restricted to the authenticated user
2. **Task Ownership**: Users can only view and modify their own tasks
3. **Conversation Context**: Messages belong to conversations and maintain chronological order
4. **Audit Trail**: All entities have created_at and updated_at timestamps
5. **Soft Deletes**: Consider implementing soft deletes for conversation history preservation

## API Contract Considerations

### Task Operations
- GET /tasks - Retrieve user's tasks with optional filtering
- POST /tasks - Create new task
- PUT /tasks/{id} - Update existing task
- DELETE /tasks/{id} - Remove task
- PATCH /tasks/{id}/complete - Toggle completion status

### Conversation Operations
- POST /conversations - Start new conversation
- GET /conversations/{id} - Retrieve conversation history

### Message Operations
- POST /messages - Add message to conversation
- GET /messages?conversation_id={id} - Retrieve conversation messages