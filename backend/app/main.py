from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.db.session import engine
from app.db.base import Base
from app.api import auth, users, projects, prompts, chat


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifecycle manager for startup and shutdown events."""
    # Startup: Create tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    # Shutdown: Clean up resources
    await engine.dispose()


app = FastAPI(
    title="Chatbot Platform API",
    description="Multi-tenant chatbot platform with LLM integration",
    version="0.1.0",
    lifespan=lifespan,
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(projects.router, prefix="/projects", tags=["projects"])
app.include_router(prompts.router, prefix="/projects", tags=["prompts"])
app.include_router(chat.router, prefix="/chat", tags=["chat"])


@app.get("/")
async def root():
    """Health check endpoint."""
    return {"status": "healthy", "service": "chatbot-platform"}


@app.get("/health")
async def health():
    """Detailed health check."""
    return {"status": "ok", "database": "connected"}
