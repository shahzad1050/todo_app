# API Contracts: AI-Powered Todo Chatbot

**Feature**: AI-Powered Todo Chatbot
**Date**: 2026-01-28
**Version**: 1.0

## Overview

This document defines the API contracts for the AI-Powered Todo Chatbot, including request/response schemas, authentication requirements, and error handling patterns.

## Authentication Contract

All API endpoints require authentication via JWT token in the Authorization header:

```
Authorization: Bearer {jwt_token}
```

## Chat API Contract

### Endpoint: POST /api/{user_id}/chat

#### Request

**Path Parameters:**
- `user_id` (string, required): The authenticated user's ID

**Request Body:**
```json
{
  "message": "string (required): The user's natural language message",
  "conversation_id": "string (optional): Existing conversation ID to continue"
}
```

**Example Request:**
```json
{
  "message": "Add a task to buy groceries",
  "conversation_id": "abc123xyz"
}
```

#### Response

**Success Response (200 OK):**
```json
{
  "conversation_id": "string: The conversation ID (newly created or existing)",
  "response": "string: AI-generated response to the user",
  "tool_calls": [
    {
      "tool_name": "string: Name of the MCP tool called",
      "input": "object: Input parameters sent to the tool",
      "result": "object: Result returned by the tool",
      "status": "string: Status of the tool call (success/error)"
    }
  ],
  "timestamp": "string: ISO 8601 timestamp"
}
```

**Example Response:**
```json
{
  "conversation_id": "def456uvw",
  "response": "I've added the task 'buy groceries' to your list.",
  "tool_calls": [
    {
      "tool_name": "add_task",
      "input": {
        "user_id": "user123",
        "title": "buy groceries",
        "description": ""
      },
      "result": {
        "task_id": "task789",
        "title": "buy groceries",
        "status": "added"
      },
      "status": "success"
    }
  ],
  "timestamp": "2026-01-28T10:30:00Z"
}
```

#### Error Responses

**Unauthorized (401):**
```json
{
  "detail": "Not authenticated"
}
```

**Validation Error (422):**
```json
{
  "detail": [
    {
      "loc": ["body", "message"],
      "msg": "Field required",
      "type": "value_error.missing"
    }
  ]
}
```

**Internal Server Error (500):**
```json
{
  "detail": "Internal server error occurred"
}
```

## MCP Tools Contract

### add_task(user_id, title, description)

**Input:**
```json
{
  "user_id": "string",
  "title": "string",
  "description": "string (optional)"
}
```

**Output:**
```json
{
  "task_id": "string",
  "status": "string",
  "title": "string"
}
```

### list_tasks(user_id, status)

**Input:**
```json
{
  "user_id": "string",
  "status": "string (optional, default: 'all')"
}
```

**Output:**
```json
{
  "tasks": [
    {
      "id": "string",
      "title": "string",
      "description": "string",
      "completed": "boolean",
      "created_at": "string (ISO 8601)",
      "updated_at": "string (ISO 8601)"
    }
  ]
}
```

### update_task(user_id, task_id, title, description)

**Input:**
```json
{
  "user_id": "string",
  "task_id": "string",
  "title": "string",
  "description": "string (optional)"
}
```

**Output:**
```json
{
  "task_id": "string",
  "title": "string",
  "description": "string",
  "updated_at": "string (ISO 8601)"
}
```

### delete_task(user_id, task_id)

**Input:**
```json
{
  "user_id": "string",
  "task_id": "string"
}
```

**Output:**
```json
{
  "task_id": "string",
  "status": "deleted",
  "title": "string"
}
```

### complete_task(user_id, task_id)

**Input:**
```json
{
  "user_id": "string",
  "task_id": "string"
}
```

**Output:**
```json
{
  "task_id": "string",
  "completed": "boolean",
  "title": "string",
  "updated_at": "string (ISO 8601)"
}
```

## Database Schema Contract

### Task Table
```sql
CREATE TABLE tasks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    completed BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

### Conversation Table
```sql
CREATE TABLE conversations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

### Message Table
```sql
CREATE TABLE messages (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    conversation_id UUID NOT NULL,
    user_id UUID NOT NULL,
    role VARCHAR(20) NOT NULL, -- 'user' or 'assistant'
    content TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

## Error Handling Contract

All API endpoints follow these error handling patterns:

1. **Client Errors (4xx)**: Return JSON with `detail` field
2. **Server Errors (5xx)**: Log error details and return generic error message
3. **Validation Errors**: Return 422 with detailed field-level validation errors
4. **Authentication Errors**: Return 401 with "Not authenticated" detail

## Rate Limiting Contract

All endpoints are subject to rate limiting:
- 100 requests per minute per IP address
- 10 requests per minute per authenticated user for chat endpoints
- Exceeding limits returns 429 Too Many Requests with retry-after header