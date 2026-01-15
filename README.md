# Chatbot Platform

A production-ready, multi-tenant chatbot platform built with FastAPI, PostgreSQL, and LLM integration. This platform enables users to create AI-powered chatbots (agents) with customizable system prompts and persistent chat sessions.

> **Get started in 2 minutes**: See [GROQ_SETUP.md](GROQ_SETUP.md)

## Table of Contents

- [Architecture Overview](#architecture-overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Setup Instructions](#setup-instructions)
- [Environment Variables](#environment-variables)
- [API Documentation](#api-documentation)
- [Usage Flow](#usage-flow)
- [Development](#development)
- [Production Considerations](#production-considerations)

## Architecture Overview

### System Design

The platform follows a clean, layered architecture:

```
┌─────────────┐
│   Client    │
└──────┬──────┘
       │
┌──────▼──────┐
│  FastAPI    │  ← Stateless REST API
│   Routes    │
└──────┬──────┘
       │
┌──────▼──────┐
│  Services   │  ← Business Logic Layer
│   Layer     │
└──────┬──────┘
       │
┌──────▼──────┬──────────┐
│  Database   │   LLM    │
│ (Postgres)  │ Provider │
└─────────────┴──────────┘
```

### Key Design Principles

1. **Stateless Backend**: No session state stored in memory; all state persisted in PostgreSQL
2. **Multi-tenancy**: User isolation enforced at the database query level
3. **Provider Abstraction**: LLM providers swappable via configuration
4. **Async I/O**: Full async support for database and LLM calls
5. **Type Safety**: Pydantic v2 for request/response validation
6. **Clean Separation**: Routes → Services → Models pattern

## Features

- **User Authentication**: JWT-based authentication with secure password hashing
- **Project Management**: Create and manage multiple chatbot projects (agents)
- **Custom Prompts**: Define system prompts to customize agent behavior
- **Chat Sessions**: Persistent conversation history per project
- **LLM Integration**: Support for Groq (FREE!), OpenAI, and OpenRouter APIs
- **Multi-tenant**: Complete user isolation and data security
- **Database Migrations**: Alembic for version-controlled schema changes
- **Docker Support**: Containerized deployment with Docker Compose

## Tech Stack

### Backend
- **Python 3.11+**: Modern Python with type hints
- **FastAPI**: High-performance async web framework
- **SQLAlchemy 2.0**: Async ORM with type-safe queries
- **Alembic**: Database migration tool
- **PostgreSQL**: Relational database with async support
- **Pydantic v2**: Data validation and settings management

### Authentication
- **JWT**: JSON Web Tokens for stateless auth
- **OAuth2**: Password flow implementation
- **bcrypt**: Secure password hashing

### LLM Providers
- **Groq API**: Fast inference with FREE tier (recommended!)
  - Llama 3.3 70B, Mixtral, Gemma 2, and more
  - 30 requests/minute free
  - 10-100x faster than traditional APIs
- **OpenAI API**: GPT-3.5/GPT-4 integration (paid)
- **OpenRouter**: Multi-model API gateway (paid)

### Infrastructure
- **Docker**: Containerization
- **Poetry**: Python dependency management
- **asyncpg**: High-performance async PostgreSQL driver

## Project Structure

```
chatbot-platform/
├── backend/
│   ├── app/
│   │   ├── main.py                 # FastAPI application entry point
│   │   ├── core/
│   │   │   ├── config.py           # Settings and configuration
│   │   │   ├── security.py         # JWT and password utilities
│   │   │   └── dependencies.py     # FastAPI dependencies
│   │   ├── models/
│   │   │   ├── user.py             # User ORM model
│   │   │   ├── project.py          # Project ORM model
│   │   │   ├── prompt.py           # Prompt ORM model
│   │   │   ├── chat.py             # Chat session/message models
│   │   │   └── file.py             # File upload model
│   │   ├── schemas/
│   │   │   ├── auth.py             # Authentication schemas
│   │   │   ├── user.py             # User schemas
│   │   │   ├── project.py          # Project schemas
│   │   │   ├── prompt.py           # Prompt schemas
│   │   │   └── chat.py             # Chat schemas
│   │   ├── api/
│   │   │   ├── auth.py             # Auth endpoints
│   │   │   ├── users.py            # User endpoints
│   │   │   ├── projects.py         # Project endpoints
│   │   │   ├── prompts.py          # Prompt endpoints
│   │   │   └── chat.py             # Chat endpoints
│   │   ├── services/
│   │   │   ├── llm/
│   │   │   │   ├── base.py         # LLM provider interface
│   │   │   │   ├── openai.py       # OpenAI implementation
│   │   │   │   └── openrouter.py   # OpenRouter implementation
│   │   │   └── chat_service.py     # Chat business logic
│   │   └── db/
│   │       ├── base.py             # SQLAlchemy base class
│   │       └── session.py          # Database session management
│   ├── alembic/
│   │   ├── env.py                  # Alembic environment
│   │   ├── script.py.mako          # Migration template
│   │   └── versions/               # Migration files
│   ├── alembic.ini                 # Alembic configuration
├── pyproject.toml                  # Poetry dependencies
├── docker-compose.yml              # Docker orchestration
├── Dockerfile                      # Container definition
├── .env.example                    # Environment template
└── README.md                       # This file
```

## Setup Instructions

### Prerequisites

- Python 3.11+
- Poetry 1.7+
- Docker and Docker Compose (optional)
- PostgreSQL 15+ (if not using Docker)
- **Groq API key (FREE!)** - Get it at https://console.groq.com/keys
  - OR OpenAI API key (paid)
  - OR OpenRouter API key (paid)

### Local Development Setup

1. **Clone the repository**:
```bash
git clone <repository-url>
cd chatbot-platform
```

2. **Install Poetry** (if not already installed):
```bash
curl -sSL https://install.python-poetry.org | python3 -
```

3. **Install dependencies**:
```bash
poetry install
```

4. **Set up environment variables**:
```bash
cp .env.example .env
# Edit .env with your configuration
```

5. **Start PostgreSQL** (if not using Docker):
```bash
# Using Docker for just the database
docker run -d \
  --name chatbot-postgres \
  -e POSTGRES_USER=chatbot \
  -e POSTGRES_PASSWORD=chatbot_password \
  -e POSTGRES_DB=chatbot_db \
  -p 5432:5432 \
  postgres:15-alpine
```

6. **Run database migrations**:
```bash
cd backend
poetry run alembic upgrade head
```

7. **Start the development server**:
```bash
poetry run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

8. **Access the API**:
- API: http://localhost:8000
- Interactive docs: http://localhost:8000/docs
- Alternative docs: http://localhost:8000/redoc

### Docker Setup (Recommended)

1. **Set environment variables**:
```bash
cp .env.example .env
# Edit .env with your API keys
```

2. **Start all services**:
```bash
docker-compose up -d
```

3. **Check logs**:
```bash
docker-compose logs -f backend
```

4. **Access the API**:
- API: http://localhost:8000
- Docs: http://localhost:8000/docs

### Creating Database Migrations

When you modify models:

```bash
cd backend
poetry run alembic revision --autogenerate -m "Description of changes"
poetry run alembic upgrade head
```

## Environment Variables

Create a `.env` file based on `.env.example`:

### Required Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `DATABASE_URL` | PostgreSQL connection string | `postgresql+asyncpg://user:pass@localhost:5432/db` |
| `SECRET_KEY` | JWT signing key (generate with `openssl rand -hex 32`) | `your-secret-key` |
| `LLM_PROVIDER` | LLM provider to use (`groq`, `openai`, or `openrouter`) | `groq` |
| `GROQ_API_KEY` | **Groq API key (FREE!)** - Get at https://console.groq.com/keys | `gsk-...` |
| `OPENAI_API_KEY` | OpenAI API key (if using OpenAI - paid) | `sk-...` |
| `OPENROUTER_API_KEY` | OpenRouter API key (if using OpenRouter - paid) | `sk-or-v1-...` |

### Optional Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `ALGORITHM` | JWT algorithm | `HS256` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Token expiration time | `30` |
| `DEBUG` | Debug mode | `false` |
| `LLM_MODEL` | Model to use | `llama-3.3-70b-versatile` (Groq) |
| `LLM_TEMPERATURE` | Response randomness (0-2) | `0.7` |
| `LLM_MAX_TOKENS` | Max response length | `1000` |
| `LLM_TIMEOUT` | LLM request timeout (seconds) | `30` |

## API Documentation

### Authentication

#### Register a new user
```http
POST /auth/register
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "securepassword123"
}
```

Response:
```json
{
  "id": "uuid",
  "email": "user@example.com",
  "created_at": "2024-01-01T00:00:00"
}
```

#### Login
```http
POST /auth/login
Content-Type: application/x-www-form-urlencoded

username=user@example.com&password=securepassword123
```

Response:
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "token_type": "bearer"
}
```

### Projects

All project endpoints require authentication (`Authorization: Bearer <token>`).

#### Create a project
```http
POST /projects
Authorization: Bearer <token>
Content-Type: application/json

{
  "name": "Customer Support Bot",
  "description": "Handles customer inquiries"
}
```

#### List projects
```http
GET /projects
Authorization: Bearer <token>
```

#### Get specific project
```http
GET /projects/{project_id}
Authorization: Bearer <token>
```

### Prompts

#### Create a prompt
```http
POST /projects/{project_id}/prompts
Authorization: Bearer <token>
Content-Type: application/json

{
  "content": "You are a helpful customer support agent. Be polite and professional."
}
```

#### List prompts
```http
GET /projects/{project_id}/prompts
Authorization: Bearer <token>
```

### Chat

#### Send a message
```http
POST /chat
Authorization: Bearer <token>
Content-Type: application/json

{
  "project_id": "uuid",
  "message": "Hello, I need help with my order",
  "session_id": "uuid" // Optional, creates new session if omitted
}
```

Response:
```json
{
  "session_id": "uuid",
  "message": {
    "id": "uuid",
    "role": "user",
    "content": "Hello, I need help with my order",
    "timestamp": "2024-01-01T00:00:00",
    "chat_session_id": "uuid"
  },
  "assistant_message": {
    "id": "uuid",
    "role": "assistant",
    "content": "Hello! I'd be happy to help you with your order...",
    "timestamp": "2024-01-01T00:00:01",
    "chat_session_id": "uuid"
  }
}
```

## Usage Flow

### 1. User Registration and Authentication

```bash
# Register
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","password":"password123"}'

# Login
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=user@example.com&password=password123"

# Save the access_token from response
TOKEN="<access_token>"
```

### 2. Create a Project

```bash
curl -X POST http://localhost:8000/projects \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "My Chatbot",
    "description": "A helpful assistant"
  }'

# Save the project id
PROJECT_ID="<project_id>"
```

### 3. Add System Prompts

```bash
curl -X POST http://localhost:8000/projects/$PROJECT_ID/prompts \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "content": "You are a knowledgeable AI assistant. Provide clear, concise answers."
  }'
```

### 4. Start Chatting

```bash
# First message (creates new session)
curl -X POST http://localhost:8000/chat \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "project_id": "'$PROJECT_ID'",
    "message": "What is machine learning?"
  }'

# Continue conversation (use session_id from previous response)
curl -X POST http://localhost:8000/chat \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "project_id": "'$PROJECT_ID'",
    "session_id": "'$SESSION_ID'",
    "message": "Can you explain neural networks?"
  }'
```

## Development

### Code Style

The project uses:
- **Black**: Code formatting
- **Ruff**: Linting
- **Type hints**: Throughout the codebase

Run formatters:
```bash
poetry run black backend/
poetry run ruff check backend/ --fix
```

### Testing

```bash
poetry run pytest
```

### Database Console

Access PostgreSQL:
```bash
docker-compose exec db psql -U chatbot -d chatbot_db
```

### Useful Commands

```bash
# View logs
docker-compose logs -f backend

# Restart services
docker-compose restart

# Stop services
docker-compose down

# Reset database
docker-compose down -v
docker-compose up -d
```

## Production Considerations

### Security

1. **Change SECRET_KEY**: Generate a strong secret key:
   ```bash
   openssl rand -hex 32
   ```

2. **HTTPS Only**: Deploy behind a reverse proxy (nginx) with SSL/TLS

3. **CORS Configuration**: Restrict allowed origins in production

4. **Environment Variables**: Use secrets management (AWS Secrets Manager, HashiCorp Vault)

5. **Rate Limiting**: Implement rate limiting for API endpoints

6. **Input Validation**: Already implemented via Pydantic

### Performance

1. **Database Connection Pooling**: Configure appropriate pool size
2. **Caching**: Consider Redis for session caching
3. **Async Workers**: Scale uvicorn workers based on CPU cores
4. **Database Indexes**: Already indexed on foreign keys and common queries
5. **LLM Timeout**: Configure based on your needs

### Monitoring

1. **Logging**: Implement structured logging (JSON format)
2. **Metrics**: Add Prometheus metrics
3. **Error Tracking**: Integrate Sentry or similar
4. **Health Checks**: Use `/health` endpoint for monitoring

### Scaling

1. **Horizontal Scaling**: Stateless design allows easy horizontal scaling
2. **Load Balancing**: Use nginx or cloud load balancer
3. **Database**: Consider read replicas for high read loads
4. **LLM Calls**: Implement queueing for high-volume scenarios

### Deployment Example (Docker)

```bash
# Build production image
docker build -t chatbot-platform:latest .

# Run with production settings
docker run -d \
  --name chatbot-api \
  -e DATABASE_URL=$DATABASE_URL \
  -e SECRET_KEY=$SECRET_KEY \
  -e OPENAI_API_KEY=$OPENAI_API_KEY \
  -p 8000:8000 \
  chatbot-platform:latest
```

## Architecture Decisions

### Why AsyncIO?

- Non-blocking I/O for database and LLM calls
- Better resource utilization
- Handles concurrent requests efficiently

### Why PostgreSQL?

- ACID compliance for data integrity
- Strong typing and constraints
- Excellent async support via asyncpg
- Battle-tested in production

### Why JWT?

- Stateless authentication
- No server-side session storage
- Easy to scale horizontally
- Standard and well-supported

### Why Provider Abstraction?

- Easily switch between LLM providers
- Test with mock providers
- Support multiple providers simultaneously
- Isolate provider-specific code

## Troubleshooting

### Database Connection Issues

```bash
# Check if PostgreSQL is running
docker-compose ps

# Check database logs
docker-compose logs db

# Verify connection string
echo $DATABASE_URL
```

### Migration Issues

```bash
# Check current migration
poetry run alembic current

# View migration history
poetry run alembic history

# Rollback one migration
poetry run alembic downgrade -1
```

### LLM Provider Errors

```bash
# Test OpenAI connection
curl https://api.openai.com/v1/models \
  -H "Authorization: Bearer $OPENAI_API_KEY"

# Check provider configuration
grep LLM_PROVIDER .env
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Run formatters and linters
6. Submit a pull request

## License

MIT License - see LICENSE file for details

## Support

For issues and questions:
- GitHub Issues: [repository]/issues
- Email: support@example.com

---

Built with ❤️ using FastAPI and modern Python practices.
