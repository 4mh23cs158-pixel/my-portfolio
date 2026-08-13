import os

from dotenv import load_dotenv
from fastapi import APIRouter, HTTPException, Request
from passlib.context import CryptContext

load_dotenv()

ADMIN_USERNAME = os.getenv("ADMIN_USERNAME")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

router = APIRouter(
    prefix="/api/auth",
    tags=["Authentication"]
)


@router.post("/login")
def login(
    request: Request,
    username: str,
    password: str
):
    if not ADMIN_USERNAME or not ADMIN_PASSWORD:
        raise HTTPException(
            status_code=500,
            detail="Admin credentials are not configured"
        )

    if username != ADMIN_USERNAME or password != ADMIN_PASSWORD:
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )

    request.session["admin"] = True

    return {
        "message": "Login successful"
    }


@router.post("/logout")
def logout(request: Request):

    request.session.clear()

    return {
        "message": "Logged out successfully"
    }