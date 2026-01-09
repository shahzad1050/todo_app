---
id: 4
title: create-fullstack-web-app-tasks
stage: tasks
date: 2025-12-31
surface: agent
model: Claude Sonnet 4.5
feature: 1-fullstack-web-app
branch: 1-fullstack-web-app
user: shahz
command: /sp.tasks
labels: [tasks, fullstack, webapp, todo]
links:
  spec: ./specs/1-fullstack-web-app/spec.md
  ticket: null
  adr: null
  pr: null
files:
 - ./specs/1-fullstack-web-app/tasks.md
tests:
 - ./specs/1-fullstack-web-app/tests/
---

## Prompt

prompt /sp.task
Phase: II – Full-Stack Web Application
Reference Plan: /sp.plan
Reference Spec: /sp.specify
Reference Constitution: /sp.constitution

Objective:
Break Phase II plan into actionable tasks for generating a complete full-stack Todo web application. Backend files reside in backend/ folder, frontend files in frontend/ folder. All tasks must follow spec-driven development.

Tasks:

-----------------------------------------------------
Task 1: Project Setup
-----------------------------------------------------
- Create project folder: todo_webapp
- Create backend/ folder for backend code
- Create frontend/ folder for Next.js app
- Initialize Python virtual environment in backend/
- Initialize Node.js environment in frontend/

-----------------------------------------------------
Task 2: Backend Entry Point
-----------------------------------------------------
- File: backend/main.py
- Initialize FastAPI app
- Include CORS middleware for frontend
- Mount API routers (to be created later)

-----------------------------------------------------
Task 3: Database Setup
-----------------------------------------------------
- File: backend/database.py
- Configure Neon Serverless PostgreSQL connection
- Create session and engine
- Provide helper function to get DB session

-----------------------------------------------------
Task 4: Database Models
-----------------------------------------------------
- File: backend/models.py
- Task model: id, user_id, title, description, completed, created_at, updated_at
- User model: user_id, email, hashed_password, created_at, updated_at
- Ensure proper relationships

-----------------------------------------------------
Task 5: CRUD Operations
-----------------------------------------------------
- File: backend/crud.py
- Functions:
    add_task(user_id, title, description)
    delete_task(user_id, task_id)
    update_task(user_id, task_id, title=None, description=None)
    list_tasks(user_id, status="all")
    toggle_task_completion(user_id, task_id)
- Handle invalid IDs and errors

-----------------------------------------------------
Task 6: Authentication
-----------------------------------------------------
- File: backend/auth.py
- Implement signup and login using Better Auth
- Include token generation and verification
- Ensure tasks are user-scoped

-----------------------------------------------------
Task 7: API Endpoints
-----------------------------------------------------
- File: backend/api/tasks.py
- Implement REST API endpoints:
    GET /api/{user_id}/tasks
    POST /api/{user_id}/tasks
    GET /api/{user_id}/tasks/{id}
    PUT /api/{user_id}/tasks/{id}
    DELETE /api/{user_id}/tasks/{id}
    PATCH /api/{user_id}/tasks/{id}/complete
- Validate inputs, return JSON responses
- Protect endpoints with auth

-----------------------------------------------------
Task 8: Backend Utilities
-----------------------------------------------------
- File: backend/utils.py
- Add any helper functions (e.g., formatting responses, timestamps)
- Keep code modular and reusable

-----------------------------------------------------
Task 9: Backend Tests
-----------------------------------------------------
- File: backend/tests/test_tasks.py
- Unit tests for CRUD operations
- Integration tests for API endpoints
- Test authentication and database persistence

----------------------------------------------pecify and /sp.constitution

End of Tasks

## Response snapshot

Successfully generated comprehensive implementation tasks for the full-stack web application based on the spec, plan, data model, and API contracts. The tasks.md file contains 46 specific, actionable tasks organized by user story and priority:

- Phase 1: Project Setup (4 tasks)
- Phase 2: Foundational Components (5 tasks)
- Phase 3: User Story 1 - User Authentication and Task Management (8 tasks)
- Phase 4: User Story 2 - Secure Task Access (6 tasks)
- Phase 5: User Story 3 - Responsive Web Interface (6 tasks)
- Phase 6: Error Handling and Edge Cases (6 tasks)
- Phase 7: Testing and Quality Assurance (5 tasks)
- Phase 8: Polish and Cross-Cutting Concerns (6 tasks)

All tasks follow the required format with proper IDs, story labels, and file paths. Tasks are organized by user story to enable independent implementation and testing as required by the constitution.

## Outcome

- ✅ Impact: Created comprehensive task breakdown for full-stack web application implementation
- 🧪 Tests: 5 testing-related tasks included throughout implementation phases
- 📁 Files: 1 tasks file created with 46 actionable tasks
- 🔁 Next prompts: Ready for implementation with /sp.implement or individual task execution
- 🧠 Reflection: Tasks organized by user stories enabling independent development and testing

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): PASS
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Begin implementation of Phase 1 tasks