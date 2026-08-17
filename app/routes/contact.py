import os

from dotenv import load_dotenv
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr
from email.message import EmailMessage

import aiosmtplib


# Load environment variables
load_dotenv()


router = APIRouter(
    prefix="/api/contact",
    tags=["Contact"]
)


# ==========================================
# CONTACT REQUEST SCHEMA
# ==========================================

class ContactRequest(BaseModel):

    name: str

    email: EmailStr

    message: str


# ==========================================
# SEND CONTACT MESSAGE
# ==========================================

@router.post("/")
async def send_contact_message(
    contact: ContactRequest
):

    email_host = os.getenv("EMAIL_HOST")

    email_port = int(
        os.getenv("EMAIL_PORT", "587")
    )

    email_username = os.getenv(
        "EMAIL_USERNAME"
    )

    email_password = os.getenv(
        "EMAIL_PASSWORD"
    )

    email_to = os.getenv(
        "EMAIL_TO"
    )


    # Check email configuration
    if not all([
        email_host,
        email_username,
        email_password,
        email_to
    ]):

        raise HTTPException(
            status_code=500,
            detail="Email service is not configured"
        )


    # Create email
    email_message = EmailMessage()

    email_message["From"] = email_username

    email_message["To"] = email_to

    email_message["Reply-To"] = contact.email

    email_message["Subject"] = (
        f"Portfolio Contact: {contact.name}"
    )


    email_message.set_content(
        f"""
You received a new message from your portfolio.

Name:
{contact.name}

Email:
{contact.email}

Message:
{contact.message}
"""
    )


    # Send email
    try:

        await aiosmtplib.send(

            email_message,

            hostname=email_host,

            port=email_port,

            start_tls=True,

            username=email_username,

            password=email_password

        )

    except Exception as error:

        print(
            "Email sending error:",
            error
        )

        raise HTTPException(
            status_code=500,
            detail="Failed to send email"
        )


    return {
        "message": "Your message has been sent successfully!"
    }