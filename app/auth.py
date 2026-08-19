import os

from dotenv import load_dotenv
from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel


# ==========================================
# LOAD ENVIRONMENT VARIABLES
# ==========================================

load_dotenv()


ADMIN_USERNAME = os.getenv("ADMIN_USERNAME")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")


# ==========================================
# LOGIN REQUEST SCHEMA
# ==========================================

class LoginRequest(BaseModel):
    username: str
    password: str


# ==========================================
# ROUTER
# ==========================================

router = APIRouter(
    prefix="/api/auth",
    tags=["Authentication"]
)


# ==========================================
# LOGIN
# ==========================================

@router.post("/login")
def login(
    login_data: LoginRequest,
    request: Request
):

    # Check whether admin credentials exist
    if not ADMIN_USERNAME or not ADMIN_PASSWORD:
        raise HTTPException(
            status_code=500,
            detail="Admin credentials are not configured"
        )

    # Validate credentials
    if (
        login_data.username != ADMIN_USERNAME
        or login_data.password != ADMIN_PASSWORD
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )

    # Create admin session
    request.session["admin"] = True

    return {
        "message": "Login successful"
    }


# ==========================================
# AUTH STATUS
# ==========================================

@router.get("/status")
def auth_status(
    request: Request
):

    is_admin = request.session.get(
        "admin",
        False
    )

    return {
        "logged_in": bool(is_admin)
    }


# ==========================================
# LOGOUT
# ==========================================

@router.post("/logout")
def logout(
 