import os
import html

from dotenv import load_dotenv
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr

import resend


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
# RESEND CONFIGURATION
# =========================================================

RESEND_API_KEY = os.getenv("RESEND_API_KEY")
EMAIL_TO = os.getenv("EMAIL_TO")

# For testing, Resend provides this sender.
# Later, you can replace it with an address from your
# verified domain.
EMAIL_FROM = os.getenv(
    "EMAIL_FROM",
    "Portfolio <onboarding@resend.dev>"
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
    # CHECK RESEND CONFIGURATION
    # -----------------------------------------------------

    if not RESEND_API_KEY:
        print("ERROR: RESEND_API_KEY is missing")

        raise HTTPException(
            status_code=500,
            detail="Email service is not configured"
        )

    if not EMAIL_TO:
        print("ERROR: EMAIL_TO is missing")

        raise HTTPException(
            status_code=500,
            detail="Email recipient is not configured"
        )

    # -----------------------------------------------------
    # SET RESEND API KEY
    # -----------------------------------------------------

    resend.api_key = RESEND_API_KEY

    # -----------------------------------------------------
    # ESCAPE USER INPUT FOR HTML EMAIL
    # -----------------------------------------------------

    safe_name = html.escape(contact.name)
    safe_email = html.escape(str(contact.email))
    safe_message = html.escape(contact.message)

    # -----------------------------------------------------
    # CREATE EMAIL
    # -----------------------------------------------------

    params: resend.Emails.SendParams = {
        "from": EMAIL_FROM,
        "to": [EMAIL_TO],
        "reply_to": [str(contact.email)],
        "subject": f"Portfolio Contact: {contact.name}",
        "html": f"""
        <html>
            <body>
                <h2>New Portfolio Contact Message</h2>

                <p>
                    <strong>Name:</strong>
                    {safe_name}
                </p>

                <p>
                    <strong>Email:</strong>
                    {safe_email}
                </p>

                <p>
                    <strong>Message:</strong>
                </p>

                <p>
                    {safe_message.replace(chr(10), "<br>")}
                </p>

                <hr>

                <p>
                    This message was sent from your portfolio contact form.
                </p>
            </body>
        </html>
        """
    }

    # -----------------------------------------------------
    # SEND EMAIL USING RESEND
    # -----------------------------------------------------

    try:

        print("Attempting to send email through Resend...")
        print("Email From:", EMAIL_FROM)
        print("Email To:", EMAIL_TO)

        email = await resend.Emails.send_async(params)

        print("Email sent successfully!")
        print("Resend response:", email)

    except Exception as error:

         print("====================================")
         print("RESEND EMAIL ERROR:")
         print(repr(error))
         print("====================================")

    raise HTTPException(
        status_code=500,
        detail=f"Resend error: {str(error)}"
    )

    # -----------------------------------------------------
    # SUCCESS RESPONSE
    # -----------------------------------------------------

    return {
        "message": "Your message has been sent successfully!"
    }