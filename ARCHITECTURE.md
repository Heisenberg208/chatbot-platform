# System Architecture

## High-Level Overview

```
┌─────────────────────────────────────────────────────────┐
│                     Client Layer                        │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐ │
│  │   Browser    │  │   Streamlit  │  │   Mobile     │ │
│  │   (React)    │  │      UI      │  │     App      │ │
│  └──────────────┘  └──────────────┘  └──────────────┘ │
└───────────────────────┬─────────────────────────────────┘
                        │ HTTPS/REST
┌───────────────────────▼─────────────────────────────────┐
│                  API Gateway Layer                      │
│              (FastAPI Application)                      │
│                                                          │
│  ┌────────────────────────────────────────────────┐    │
│  │           Authentication Middleware            │    │
│  │              (JWT Validation)                  │    │
│  └────────────────────┬───────────────────────────┘    │
│                       │                                 │
│  ┌────────────────────▼───────────────────────────┐    │
│  │              API Routes Layer                  │    │
│  │   /auth  /users  /projects  /prompts  /chat   │    │
│  └────────────────────┬───────────────────────────┘    │
└───────────────────────┼─────────────────────────────────┘
                        │
┌───────────────────────▼─────────────────────────────────┐
│               Business Logic Layer                      │
│                  (Service Classes)                      │
│                                                          │
│  ┌──────────────────┐         ┌──────────────────┐    │
│  │  Chat Service    │◄────────┤  LLM Provider    │    │
│  │  - Session Mgmt  │         │   Abstraction    │    │
│  │  - Message Build │         │  - OpenAI        │    │
│  │  - Response Gen  │         │  - OpenRouter    │    │
│  └────────┬─────────┘         └──────────────────┘    │
└───────────┼─────────────────────────────────────────────┘
            │
┌───────────▼─────────────────────────────────────────────┐
│                   Data Layer                            │
│                                                          │
│  ┌──────────────────────────────────────────────────┐  │
│  │            SQLAlchemy ORM Models                 │  │
│  │  User  Project  Prompt  ChatSession  Message    │  │
│  └────────────────────┬─────────────────────────────┘  │
│                       │                                 │
│  ┌────────────────────▼─────────────────────────────┐  │
│  │           PostgreSQL Database                    │  │
│  │    - User data     - Chat history                │  │
│  │    - Projects      - Relationships               │  │
│  └──────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│                External Services                        │
│  ┌──────────────┐              ┌──────────────┐        │
│  │   OpenAI     │              │  OpenRouter  │        │
│  │     API      │              │     API      │        │
│  └──────────────┘              └──────────────┘        │
└─────────────────────────────────────────────────────────┘
```

## Request Flow: Chat Message

```
1. User sends message
   │
   ▼
2. API Route (/chat)
   │ - Validates request schema
   │ - Extracts JWT token
   ▼
3. Authentication Middleware
   │ - Validates JWT
   │ - Loads user from DB
   ▼
4. Chat Service
   │ - Verifies project ownership
   │ - Gets/creates chat session
   │ - Loads project prompts
   │ - Builds message context
   │
   ├─► 5a. Fetch from Database
   │       - Project details
   │       - System prompts
   │       - Chat history
   │
   └─► 5b. Call LLM Provider
       │   - OpenAI or OpenRouter
       │   - Async HTTP request
       │   - Handle timeout/errors
       ▼
   6. Save Messages
       │ - User message
       │ - Assistant response
       ▼
   7. Return Response
       │ - Session ID
       │ - Message objects
       ▼
   8. Client receives response
```

## Data Model

```
┌─────────────┐
│    User     │
│─────────────│
│ id (PK)     │
│ email       │
│ password    │
│ created_at  │
└──────┬──────┘
       │ 1:N
       ▼
┌─────────────┐
│   Project   │
│─────────────│
│ id (PK)     │
│ user_id (FK)│
│ name        │
│ description │
│ created_at  │
└──┬──────┬───┘
   │      │
   │ 1:N  │ 1:N
   │      │
   ▼      ▼
┌─────┐  ┌────────────┐
│Prompt│  │ChatSession │
│─────│  │────────────│
│id   │  │ id (PK)    │
│proj │  │ project_id │
│text │  │ created_at │
└─────┘  └──────┬─────┘
                │ 1:N
                ▼
         ┌────────────┐
         │  Message   │
         │────────────│
         │ id (PK)    │
         │ session_id │
         │ role       │
         │ content    │
         │ timestamp  │
         └────────────┘
```

## Security Architecture

```
┌──────────────────────────────────────────┐
│         Security Layers                  │
├──────────────────────────────────────────┤
│                                          │
│  1. Transport Security                  │
│     ├─ HTTPS/TLS encryption             │
│     └─ Secure headers                   │
│                                          │
│  2. Authentication                      │
│     ├─ JWT tokens (stateless)           │
│     ├─ Bcrypt password hashing          │
│     └─ Token expiration                 │
│                                          │
│  3. Authorization                       │
│     ├─ User ownership checks            │
│     ├─ Database-level isolation         │
│     └─ Resource access validation       │
│                                          │
│  4. Input Validation                    │
│     ├─ Pydantic schemas                 │
│     ├─ SQL injection prevention (ORM)   │
│     └─ XSS protection                   │
│                                          │
│  5. Data Protection                     │
│     ├─ Password never stored plaintext  │
│     ├─ API keys in environment vars     │
│     └─ Sensitive data encrypted         │
│                                          │
└──────────────────────────────────────────┘
```

## LLM Provider Abstraction

```
┌─────────────────────────────────────┐
│       LLMProvider (Interface)       │
│─────────────────────────────────────│
│ + generate(messages) → str          │
│ + validate_connection() → bool      │
└──────────────┬──────────────────────┘
               │
       ┌───────┴───────┐
       │               │
       ▼               ▼
┌─────────────┐ ┌──────────────┐
│  OpenAI     │ │ OpenRouter   │
│  Provider   │ │  Provider    │
│─────────────│ │──────────────│
│ - API key   │ │ - API key    │
│ - Timeout   │ │ - Timeout    │
│ - Model     │ │ - Model      │
└─────────────┘ └──────────────┘

Benefits:
• Easy to switch providers
• Test with mock providers
• Support multiple providers
• Isolate provider-specific code
```

## Deployment Architecture

### Development
```
┌─────────────────────────────────┐
│     Developer Machine           │
│  ┌───────────────────────────┐ │
│  │  Python/Poetry            │ │
│  │  FastAPI Dev Server       │ │
│  │  :8000                    │ │
│  └───────────────────────────┘ │
│  ┌───────────────────────────┐ │
│  │  PostgreSQL (Docker)      │ │
│  │  :5432                    │ │
│  └───────────────────────────┘ │
└─────────────────────────────────┘
```

### Docker Compose
```
┌─────────────────────────────────┐
│     Docker Host                 │
│  ┌───────────────────────────┐ │
│  │  Backend Container        │ │
│  │  - FastAPI                │ │
│  │  - Uvicorn                │ │
│  │  :8000                    │ │
│  └───────────────────────────┘ │
│  ┌───────────────────────────┐ │
│  │  Database Container       │ │
│  │  - PostgreSQL             │ │
│  │  :5432                    │ │
│  └───────────────────────────┘ │
│  ┌───────────────────────────┐ │
│  │  Docker Network           │ │
│  └───────────────────────────┘ │
└─────────────────────────────────┘
```

### Production
```
┌────────────────────────────────────────┐
│         Load Balancer / CDN            │
│            (nginx/ALB)                 │
└──────────────┬─────────────────────────┘
               │
    ┌──────────┴──────────┐
    │                     │
    ▼                     ▼
┌─────────┐         ┌─────────┐
│ Backend │         │ Backend │
│  Pod 1  │ ...     │  Pod N  │
└────┬────┘         └────┬────┘
     │                   │
     └─────────┬─────────┘
               │
               ▼
     ┌──────────────────┐
     │   Database       │
     │   (RDS/Managed)  │
     │   - Primary      │
     │   - Read Replica │
     └──────────────────┘
```

## Technology Decisions

### Why Async?
- Non-blocking I/O for database operations
- Concurrent handling of LLM API calls
- Better resource utilization
- Scales horizontally with minimal overhead

### Why PostgreSQL?
- ACID compliance for data integrity
- Strong typing and constraints
- Excellent async support (asyncpg)
- Mature ecosystem and tooling
- Native UUID support

### Why JWT?
- Stateless authentication
- No server-side session storage
- Easy horizontal scaling
- Standard format with library support

### Why Provider Abstraction?
- Flexibility to switch LLM providers
- Test without real API calls
- Support multiple providers
- Isolate provider-specific code

## Scalability Considerations

### Horizontal Scaling
- Stateless design allows infinite horizontal scaling
- No shared memory between instances
- Database handles concurrency
- Load balancer distributes requests

### Database Optimization
- Indexed foreign keys
- Connection pooling
- Async queries
- Read replicas for scale

### Caching Strategy (Future)
- Redis for session caching
- Cache user data
- Cache project/prompt data
- TTL-based invalidation

### Rate Limiting (Future)
- Per-user rate limits
- Per-project rate limits
- Token bucket algorithm
- Database-backed counters
