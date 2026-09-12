# app/services/otp_service.py
#
# Generates and emails one-time passcodes via Gmail SMTP, and verifies them.
# Used by the forgot/reset-password flow (app/services/auth_service.py).
#
# SETUP REQUIRED (you must do this yourself — I cannot access your Gmail):
#   1. Go to https://myaccount.google.com/security
#   2. Turn on 2-Step Verification if it isn't already on (required for App Passwords)
#   3. Go to https://myaccount.google.com/apppasswords
#   4. Create an App Password (name it e.g. "NeuroOne backend")
#   5. Google gives you a 16-character password — copy it
#   6. Add these two lines to backend/.env:
#        GMAIL_ADDRESS=youraddress@gmail.com
#        GMAIL_APP_PASSWORD=the16charpassword
#      (use the App Password, NOT your real Gmail login password — Gmail
#      blocks plain-password SMTP login for security)
#   Both are optional for booting the API; without them, requesting an OTP
#   raises ExternalServiceError instead of attempting an SMTP login.
#
# NOTE on storage: this uses a simple in-memory dict for OTP codes, which is
# fine for local dev/demo but resets whenever the server restarts and won't
# work if you ever run multiple server processes. For production, move this
# to Redis or a database table with a real expiry column.

import secrets
import smtplib
import time
from dataclasses import dataclass
from email.mime.text import MIMEText

from app.core.config import settings
from app.utils.exceptions import ExternalServiceError

OTP_TTL_SECONDS = 300  # 5 minutes
MAX_VERIFY_ATTEMPTS = 5  # wrong guesses allowed before the code is burned


@dataclass
class _OtpEntry:
    code: str
    expires_at: float
    attempts_remaining: int = MAX_VERIFY_ATTEMPTS


# { identity (e.g. email): _OtpEntry }
_otp_store: dict[str, _OtpEntry] = {}


def generate_and_send_otp(identity: str, to_email: str) -> None:
    """Generates a 6-digit OTP, stores it, and emails it via Gmail SMTP."""

    # Checked before storing a code: a code the user can never receive would
    # only sit in the store until it expired.
    if not settings.GMAIL_ADDRESS or not settings.GMAIL_APP_PASSWORD:
        raise ExternalServiceError(
            "Email delivery is not configured. Set GMAIL_ADDRESS and "
            "GMAIL_APP_PASSWORD to send verification codes."
        )

    code = f"{secrets.randbelow(1_000_000):06d}"
    _otp_store[identity] = _OtpEntry(code=code, expires_at=time.time() + OTP_TTL_SECONDS)

    message = MIMEText(
        f"Your NeuroOne verification code is: {code}\n\n"
        f"This code expires in 5 minutes. If you didn't request this, "
        f"you can safely ignore this email."
    )
    message["Subject"] = "Your NeuroOne verification code"
    message["From"] = settings.GMAIL_ADDRESS
    message["To"] = to_email

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(settings.GMAIL_ADDRESS, settings.GMAIL_APP_PASSWORD)
        server.send_message(message)


def verify_otp(identity: str, submitted_code: str) -> bool:
    """
    Checks a submitted OTP against the stored one. The code is only
    consumed (deleted) when it's correct, expired, or has run out of
    attempts — a wrong guess costs an attempt but does not otherwise
    burn a still-valid code, so the user can retry up to
    MAX_VERIFY_ATTEMPTS times before having to request a new code.
    """
    entry = _otp_store.get(identity)

    if entry is None:
        return False

    if time.time() > entry.expires_at:
        del _otp_store[identity]
        return False

    if submitted_code != entry.code:
        entry.attempts_remaining -= 1
        if entry.attempts_remaining <= 0:
            del _otp_store[identity]
        return False

    del _otp_store[identity]
    return True
