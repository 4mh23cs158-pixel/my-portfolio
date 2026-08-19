import os

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware

from app.database import Base, engine
from app import models

from app.auth import router as auth_router

from app.routes.projects import (
    router as projects_router
)

from app.routes.certifications import (
    router as certifications_router
)

from app.routes.contact import (
    router as contact_router
)


# ==========================================
# LOAD ENVIRONMENT VARIABLES
# ==========================================

load_dotenv()


SESSION_SECRET = os.getenv("SESSION_SECRET")

if not SESSION_SECRET:
    raise ValueError(
        "SESSION_SECRET is not set in the .env file"
    )


# ==========================================
# CREATE DATABASE TABLES
# ==========================================

Base.metadata.create_all(bind=engine)


# ==========================================
# CREATE FASTAPI APP
# ==========================================

app = FastAPI(
    title="My Portfolio API",
    description="Backend API for my personal portfolio",
    version="1.0.0"
)


# ==========================================
# CORS
# ==========================================

app.add_middleware(
    CORSMiddleware,

    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "https://my-portfolio-frontend-olive-phi.vercel.app"
    ],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"],
)


# ==========================================
# SESSION MIDDLEWARE
# ==========================================

app.add_middleware(
    SessionMiddleware,

    secret_key=SESSION_SECRET,

    same_site="lax",

    https_only=False
)


# ==========================================
# REGISTER ROUTES
# ==========================================

app.include_router(auth_router)

app.include_router(projects_router)

app.include_router(certifications_router)

app.include_router(contact_router)


# ==========================================
# HOME
# ==========================================

@app.get("/")
def home():

    return {
        "message": "Portfolio Backend is running!"
    }


# ==========================================
# HEALTH CHECK
# ==========================================

@app.get("/api/health")
def health_check():

    return {
        "status": "healthy"
    }