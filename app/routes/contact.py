import os

from dotenv import load_dotenv
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr
from email.message import EmailMessage

import aiosmtplib


# =========================================================
# LOAD ENVIRONMENT VARIABLES
# =========================================================

load_dotenv()


# =========================================================
# ROUTER
# =========================================================

router = APIRouter(
    prefix="/api/contact",
    tags=["Contact"]
)


# =========================================================
# CONTACT REQUEST SCHEMA
# =========================================================

class ContactRequest(BaseModel):
    name: str
    email: EmailStr
    message: str


# =========================================================
# SEND CONTACT MESSAGE
# =========================================================

@router.post("/")
async def send_contact_message(contact: ContactRequest):

    # -----------------------------------------------------
    # READ EMAIL CONFIGURATION
    # -----------------------------------------------------

    email_host = os.getenv("EMAIL_HOST")
    email_port_string = os.getenv("EMAIL_PORT", "587")
    email_username = os.getenv("EMAIL_USERNAME")
    email_password = os.getenv("EMAIL_PASSWORD")
    email_to = os.getenv("EMAIL_TO")

    # -----------------------------------------------------
    # VALIDATE PORT
    # -----------------------------------------------------

    try:
        email_port = int(email_port_string)
    except ValueError:
        raise HTTPException(
            status_code=500,
            detail="EMAIL_PORT must be a valid number"
        )

    # -----------------------------------------------------
    # CHECK EMAIL CONFIGURATION
    # -----------------------------------------------------

    missing_variables = []

    if not email_host:
        missing_variables.append("EMAIL_HOST")

    if not email_username:
        missing_variables.append("EMAIL_USERNAME")

    if not email_password:
        missing_variables.append("EMAIL_PASSWORD")

    if not email_to:
        missing_variables.append("EMAIL_TO")

    if missing_variables:

        print(
            "Missing email environment variables:",
            ", ".join(missing_variables)
        )

        raise HTTPException(
            status_code=500,
            detail="Email service is not configured correctly"
        )

    # -----------------------------------------------------
    # CREATE EMAIL
    # -----------------------------------------------------

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

    # -----------------------------------------------------
    # SEND EMAIL
    # -----------------------------------------------------

    try:

        print("Attempting to send email...")
        print("SMTP Host:", email_host)
        print("SMTP Port:", email_port)
        print("SMTP Username:", email_username)
        print("Email To:", email_to)

        await aiosmtplib.send(
            email_message,
            hostname=email_host,
            port=email_port,
            start_tls=True,
            username=email_username,
            password=email_password,
            timeout=30
        )

        print("Email sent successfully!")

    except aiosmtplib.SMTPAuthenticationError as error:

        print("SMTP AUTHENTICATION ERROR:", repr(error))

        raise HTTPException(
            status_code=500,
            detail="Email authentication failed. Check EMAIL_USERNAME and EMAIL_PASSWORD."
        )

    except aiosmtplib.SMTPConnectError as error:

        print("SMTP CONNECTION ERROR:", repr(error))

        raise HTTPException(
            status_code=500,
            detail="Could not connect to the email server."
        )

    except aiosmtplib.SMTPException as error:

        print("SMTP ERROR:", repr(error))

        raise HTTPException(
            status_code=500,
            detail="SMTP email service error."
        )

    except Exception as error:

        print("UNEXPECTED EMAIL ERROR:", repr(error))

        raise HTTPException(
            status_code=500,
            detail="Failed to send email."
        )

    # -----------------------------------------------------
    # SUCCESS
    # -----------------------------------------------------

    return {
        "message": "Your message has been sent successfully!"
    }