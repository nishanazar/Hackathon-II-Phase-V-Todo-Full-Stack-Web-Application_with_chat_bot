# Quickstart Guide: Advanced Features Implementation for Phase V Todo AI Chatbot

## Prerequisites

- Python 3.11+
- Node.js 18+
- Docker and Docker Compose
- Dapr runtime installed and running
- Access to Kafka/Redpanda cluster (local or cloud)
- Neon PostgreSQL account and connection details

## Environment Setup

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd <repository-name>
   ```

2. Install backend dependencies:
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

3. Install frontend dependencies:
   ```bash
   cd ../frontend
   npm install
   ```

4. Set up environment variables:
   ```bash
   # Copy the environment template
   cp .env.example .env.local
   
   # Update the values in .env.local with your specific configurations
   ```

## Dapr Configuration

1. Install Dapr CLI and runtime if not already installed:
   ```bash
   # Follow installation instructions at https://docs.dapr.io/getting-started/install-dapr-cli/
   dapr init
   ```

2. Start Dapr components:
   ```bash
   # From the project root
   dapr run --config dapr/config.yaml --components-path dapr/components
   ```

## Kafka/Redpanda Setup

1. For local development with Docker:
   ```bash
   # From the project root
   docker-compose -f kafka/docker-compose.kafka.yml up -d
   ```

2. Create required topics:
   ```bash
   # Create task-events topic
   docker exec -it kafka-container kafka-topics --create --topic task-events --bootstrap-server localhost:9092
   
   # Create reminders topic
   docker exec -it kafka-container kafka-topics --create --topic reminders --bootstrap-server localhost:9092
   ```

## Database Setup

1. Ensure your Neon PostgreSQL database is created and accessible

2. Run database migrations:
   ```bash
   cd backend
   python -m src.database.migrate
   ```

## Running the Application

### Backend (with Dapr)

```bash
cd backend
dapr run --app-id todo-backend --app-port 8000 --dapr-http-port 3500 -- python src/main.py
```

### Frontend

```bash
cd frontend
npm run dev
```

## API Endpoints

### Task Management
- `GET /api/{user_id}/tasks` - Get all tasks for a user
- `POST /api/{user_id}/tasks` - Create a new task with due_date, priority, tags, recurring_interval
- `PUT /api/{user_id}/tasks/{task_id}` - Update a task
- `DELETE /api/{user_id}/tasks/{task_id}` - Delete a task
- `PATCH /api/{user_id}/tasks/{task_id}/complete` - Mark task as completed

### Advanced Features
- `GET /api/{user_id}/tasks/search?q={query}` - Search tasks
- `GET /api/{user_id}/tasks?filter=priority:{level}&sort=due_date:asc` - Filter and sort tasks

## Testing

### Backend Tests
```bash
cd backend
pytest
```

### Frontend Tests
```bash
cd frontend
npm run test
```

## Key Components

### Backend Structure
- `src/models/task_model.py` - Extended task model with new fields
- `src/services/recurring_service.py` - Logic for recurring tasks
- `src/services/reminder_service.py` - Reminder scheduling and delivery
- `src/api/v1/task_router.py` - Task endpoints with new features

### Frontend Components
- `src/components/TaskForm.tsx` - Form with due date, priority, tags inputs
- `src/components/TaskList.tsx` - Task list with filtering, sorting
- `src/components/DatePicker.tsx` - Date picker component
- `src/components/PrioritySelector.tsx` - Priority selection component

## Troubleshooting

1. **Dapr Issues**: Ensure Dapr runtime is initialized and components are running
2. **Database Connection**: Verify your Neon PostgreSQL connection details in environment variables
3. **Kafka Connection**: Check that Kafka/Redpanda is running and accessible
4. **Environment Variables**: Ensure all required environment variables are set