# Data Model: Full-Stack Web Application

## Entities

### User
**Description**: Represents a registered user in the system
**Fields**:
- `id` (UUID/Integer): Unique identifier for the user
- `email` (String): User's email address (unique, required)
- `password_hash` (String): Hashed password for authentication
- `first_name` (String, optional): User's first name
- `last_name` (String, optional): User's last name
- `created_at` (DateTime): Timestamp when user account was created
- `updated_at` (DateTime): Timestamp when user account was last updated

**Validation Rules**:
- Email must be valid and unique
- Password must meet security requirements (handled by auth system)
- Created_at and updated_at are automatically managed

### Task
**Description**: Represents a todo item belonging to a specific user
**Fields**:
- `id` (Integer): Unique identifier for the task
- `user_id` (UUID/Integer): Foreign key linking to the owning user
- `title` (String): Title/description of the task (required)
- `description` (String, optional): Detailed description of the task
- `is_completed` (Boolean): Whether the task is completed (default: false)
- `created_at` (DateTime): Timestamp when task was created
- `updated_at` (DateTime): Timestamp when task was last updated

**Validation Rules**:
- Title must not be empty
- User_id must reference an existing user
- Is_completed defaults to false
- Created_at and updated_at are automatically managed

### Session
**Description**: Represents an authenticated user session
**Fields**:
- `id` (String/UUID): Unique session identifier
- `user_id` (UUID/Integer): Foreign key linking to the user
- `expires_at` (DateTime): When the session expires
- `created_at` (DateTime): When the session was created

**Validation Rules**:
- Session must be linked to an existing user
- Session must not be expired to be valid

## Relationships

### User → Task (One-to-Many)
- One user can have many tasks
- Foreign key: `tasks.user_id` → `users.id`
- When user is deleted, their tasks should be deleted (cascade)

### User → Session (One-to-Many)
- One user can have multiple active sessions
- Foreign key: `sessions.user_id` → `users.id`

## State Transitions

### Task State Transitions
- `pending` → `completed`: When user marks task as complete
- `completed` → `pending`: When user unmarks task as complete

## Database Constraints

1. **Unique Constraints**:
   - User email must be unique
   - Task ID must be unique within the system

2. **Foreign Key Constraints**:
   - Task.user_id must reference valid User.id
   - Session.user_id must reference valid User.id

3. **Check Constraints**:
   - Task title cannot be empty or whitespace only
   - Session expiration time must be in the future

## Indexing Strategy

1. **Users table**:
   - Index on email (for login queries)
   - Index on created_at (for user analytics)

2. **Tasks table**:
   - Index on user_id (for user-specific task queries)
   - Index on user_id and is_completed (for filtered task queries)
   - Index on created_at (for chronological ordering)

3. **Sessions table**:
   - Index on user_id (for session management)
   - Index on expires_at (for session cleanup)