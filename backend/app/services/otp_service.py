# app/services/otp_service.py
#
# Generates one-time passcodes and delivers them either via Gmail SMTP or,
# with OTP_DELIVERY=console, the backend log -- then verifies them. Used by
# the login-2FA and forgot/reset-password flows (app/services/auth_service.py).
#
# SETUP REQUIRED for OTP_DELIVERY=email (you must do this yourself — I
# cannot access your Gmail):
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
#   Settings refuses to start with OTP_DELIVERY=email and no credentials; if
#   they are cleared at runtime anyway, sending raises ExternalServiceError
#   instead of attempting an SMTP login.
#
# NOTE on storage: this uses a simple in-memory dict for OTP codes, which is
# fine for local dev/demo but resets whenever the server restarts and won't
# work if you ever run multiple server processes. For production, move this
# to Redis or a database table with a real expiry column.

import logging
import secrets
import smtplib
import time
from dataclasses import dataclass
from email.mime.text import MIMEText
from typing import Literal

from app.core.config import settings
from app.utils.exceptions import ExternalServiceError

logger = logging.getLogger(__name__)

OTP_TTL_SECONDS = 300  # 5 minutes
MAX_VERIFY_ATTEMPTS = 5  # wrong guesses allowed before the code is burned

# A code is only ever valid for the purpose it was issued under: a sign-in
# code can't be replayed to reset a password, and requesting one purpose's
# code doesn't clobber the other's (see _store_key).
OtpPurpose = Literal["login", "password_reset"]


@dataclass
class _OtpEntry:
    code: str
    expires_at: float
    attempts_remaining: int = MAX_VERIFY_ATTEMPTS


# { "{purpose}:{identity}" (e.g. "login:jane@example.com"): _OtpEntry }
_otp_store: dict[str, _OtpEntry] = {}


def _store_key(identity: str, purpose: OtpPurpose) -> str:
    return f"{purpose}:{identity}"


def generate_and_send_otp(identity: str, to_email: str, purpose: OtpPurpose) -> None:
    """Generates a 6-digit OTP scoped to `purpose`, stores it, and delivers
    it via Gmail SMTP, or logs it when OTP_DELIVERY=console."""

    # Checked before storing a code: a code the user can never receive would
    # only sit in the store until it expired. Console delivery needs no Gmail.
    if settings.OTP_DELIVERY == "email" and not (
        settings.GMAIL_ADDRESS and settings.GMAIL_APP_PASSWORD
    ):
        raise ExternalServiceError(
            "Email delivery is not configured. Set GMAIL_ADDRESS and "
            "GMAIL_APP_PASSWORD to send verification codes."
        )

    code = f"{secrets.randbelow(1_000_000):06d}"
    _otp_store[_store_key(identity, purpose)] = _OtpEntry(
        code=code, expires_at=time.time() + OTP_TTL_SECONDS
    )

    if settings.OTP_DELIVERY == "console":
        logger.info("[dev] %s OTP for %s: %s", purpose, to_email, code)
        return

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


def send_otp_background(identity: str, to_email: str, purpose: OtpPurpose) -> None:
    """Fire-and-forget wrapper meant for BackgroundTasks.add_task.

    Swallows delivery failures instead of letting them propagate, so a
    dead SMTP server can't turn into a 500 that only real accounts get --
    the caller (forgot-password, request-otp) has already sent its generic
    response by the time this runs.
    """

    try:
        generate_and_send_otp(identity=identity, to_email=to_email, purpose=purpose)
    except Exception:
        logger.exception("Failed to deliver OTP (purpose=%s)", purpose)


def verify_otp(identity: str, submitted_code: str, purpose: OtpPurpose) -> bool:
    """
    Checks a submitted OTP against the one stored for this identity and
    purpose. The code is only consumed (deleted) when it's correct, expired,
    or has run out of attempts — a wrong guess costs an attempt but does not
    otherwise burn a still-valid code, so the user can retry up to
    MAX_VERIFY_ATTEMPTS times before having to request a new code.
    """
    key = _store_key(identity, purpose)
    entry = _otp_store.get(key)

    if entry is None:
        return False

    if time.time() > entry.expires_at:
        del _otp_store[key]
        return False

    # Constant-time comparison so response timing doesn't leak how many
    # leading digits were right. Bytes, because compare_digest rejects
    # non-ASCII str and the submitted code is untrusted input.
    if not secrets.compare_digest(submitted_code.encode(), entry.code.encode()):
        entry.attempts_remaining -= 1
        if entry.attempts_remaining <= 0:
            del _otp_store[key]
        return False

    del _otp_store[key]
    return True
