# TaskMaster - AI-Powered Todo Application

TaskMaster is a modern, responsive todo application with AI-powered task management capabilities. The application allows users to manage their tasks through both traditional UI and natural language processing via an AI assistant.

## Features

- **User Authentication**: Secure login and signup functionality
- **Task Management**: Create, read, update, and delete tasks
- **AI Assistant**: Natural language processing for task management
- **Responsive Design**: Works seamlessly on desktop and mobile devices
- **Real-time Updates**: Instant feedback on task operations
- **Modern UI**: Clean, intuitive interface with smooth animations

## Tech Stack

- **Frontend**: Next.js 14 with App Router
- **Styling**: Tailwind CSS
- **Language**: TypeScript
- **Authentication**: JWT-based authentication
- **API**: REST API integration with the backend

## Getting Started

### Prerequisites

- Node.js 18+
- npm or yarn

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Create a `.env.local` file in the root directory:
```env
NEXT_PUBLIC_API_URL=http://localhost:8002
```

4. Start the development server:
```bash
npm run dev
```

The application will be available at `http://localhost:3000`

### Environment Variables

- `NEXT_PUBLIC_API_URL`: The URL of the backend API server

## Project Structure

```
frontend/
├── src/
│   ├── app/                 # Next.js app router pages
│   │   ├── globals.css      # Global styles
│   │   ├── layout.tsx       # Root layout
│   │   ├── page.tsx         # Home page with AI assistant
│   │   ├── login/          # Login page
│   │   ├── signup/         # Signup page
│   │   └── dashboard/      # Dashboard page
│   ├── components/         # Reusable React components
│   │   ├── AuthProvider.tsx # Authentication context
│   │   ├── ProtectedRoute.tsx # Route protection
│   │   ├── TaskForm.tsx    # Task creation form
│   │   ├── TaskList.tsx    # Task listing component
│   │   └── TodoChatbot.tsx # AI assistant component
│   └── lib/                # Utility functions
│       ├── auth.ts         # Authentication helpers
│       └── api.ts          # API request helpers
```

## API Integration

The frontend communicates with the backend API for all data operations:

- Authentication: `/auth/login`, `/auth/signup`
- Tasks: `/users/{userId}/tasks`
- Chat: `/users/{userId}/chat`

## Key Components

### Authentication System
- Context provider for managing user state
- Protected routes for secured pages
- Login and signup forms with validation

### Task Management
- Task creation form with validation
- Interactive task list with completion toggles
- Task deletion functionality

### AI Assistant
- Natural language processing for task management
- Conversation history tracking
- Quick action suggestions

## Styling

The application uses Tailwind CSS for styling with a consistent design system:
- Gradient backgrounds and accents
- Smooth transitions and animations
- Responsive layouts for all screen sizes
- Consistent color palette

## Deployment

The application is configured for deployment to platforms like Vercel. Ensure that environment variables are properly set in the deployment environment.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

This project is licensed under the MIT License.