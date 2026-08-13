import os

from dotenv import load_dotenv
from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware

from app.database import Base, engine
from app import models
from app.routes.projects import router as projects_router
from app.auth import router as auth_router


# Load environment variables from .env
load_dotenv()


# Get session secret from .env
SESSION_SECRET = os.getenv("SESSION_SECRET")

if not SESSION_SECRET:
    raise ValueError(
        "SESSION_SECRET is not set in the .env file"
    )


# Create database tables
Base.metadata.create_all(bind=engine)


# Create FastAPI application
app = FastAPI(
    title="My Portfolio API",
    description="Backend API for my personal portfolio",
    version="1.0.0"
)


# Add session middleware for admin authentication
app.add_middleware(
    SessionMiddleware,
    secret_key=SESSION_SECRET,
    same_site="lax",
    https_only=False
)


# Register authentication routes
app.include_router(auth_router)


# Register project routes
app.include_router(projects_router)


# Home endpoint
@app.get("/")
def home():
    return {
        "message": "Portfolio Backend is running!"
    }


# Health check endpoint
@app.get("/api/health")
def health_check():
    return {
        "status": "healthy"
    }