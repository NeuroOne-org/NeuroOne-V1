"""Tests for the OTP generation/verification helpers behind login-2FA and
password reset."""

import logging
from unittest.mock import MagicMock

from app.services import otp_service


def teardown_function() -> None:
    otp_service._otp_store.clear()


def _stub_smtp(monkeypatch) -> MagicMock:
    # The test suite defaults OTP_DELIVERY to "console" (see conftest.py) so
    # 2FA tests don't need Gmail credentials; these tests are specifically
    # about the email path, so they opt back into it.
    monkeypatch.setattr(otp_service.settings, "OTP_DELIVERY", "email")
    smtp_instance = MagicMock()
    smtp_instance.__enter__.return_value = smtp_instance
    smtp_cls = MagicMock(return_value=smtp_instance)
    monkeypatch.setattr(otp_service.smtplib, "SMTP", smtp_cls)
    return smtp_instance


def _entry(identity: str, purpose: otp_service.OtpPurpose):
    return otp_service._otp_store[otp_service._store_key(identity, purpose)]


def test_generated_code_is_six_digits_and_emailed(monkeypatch) -> None:
    smtp = _stub_smtp(monkeypatch)

    otp_service.generate_and_send_otp(
        "user@example.com", "user@example.com", purpose="password_reset"
    )

    entry = _entry("user@example.com", "password_reset")
    assert len(entry.code) == 6
    assert entry.code.isdigit()
    smtp.starttls.assert_called_once()
    smtp.login.assert_called_once()
    smtp.send_message.assert_called_once()


def test_correct_code_verifies_and_is_consumed(monkeypatch) -> None:
    _stub_smtp(monkeypatch)
    otp_service.generate_and_send_otp(
        "user@example.com", "user@example.com", purpose="password_reset"
    )
    code = _entry("user@example.com", "password_reset").code

    assert otp_service.verify_otp("user@example.com", code, purpose="password_reset") is True
    assert otp_service._store_key("user@example.com", "password_reset") not in otp_service._otp_store
    # Re-submitting the now-consumed code fails.
    assert otp_service.verify_otp("user@example.com", code, purpose="password_reset") is False


def test_unknown_identity_fails_without_raising() -> None:
    assert (
        otp_service.verify_otp("never-requested@example.com", "000000", purpose="login")
        is False
    )


def test_expired_code_fails_and_is_removed(monkeypatch) -> None:
    _stub_smtp(monkeypatch)
    otp_service.generate_and_send_otp(
        "user@example.com", "user@example.com", purpose="password_reset"
    )
    _entry("user@example.com", "password_reset").expires_at -= (
        otp_service.OTP_TTL_SECONDS + 1
    )

    assert otp_service.verify_otp("user@example.com", "000000", purpose="password_reset") is False
    assert otp_service._store_key("user@example.com", "password_reset") not in otp_service._otp_store


def test_wrong_guess_does_not_burn_a_still_valid_code(monkeypatch) -> None:
    _stub_smtp(monkeypatch)
    otp_service.generate_and_send_otp(
        "user@example.com", "user@example.com", purpose="password_reset"
    )
    code = _entry("user@example.com", "password_reset").code
    wrong = "000000" if code != "000000" else "111111"

    assert otp_service.verify_otp("user@example.com", wrong, purpose="password_reset") is False
    assert otp_service.verify_otp("user@example.com", code, purpose="password_reset") is True


def test_code_is_burned_after_max_attempts(monkeypatch) -> None:
    _stub_smtp(monkeypatch)
    otp_service.generate_and_send_otp(
        "user@example.com", "user@example.com", purpose="password_reset"
    )
    code = _entry("user@example.com", "password_reset").code
    wrong = "000000" if code != "000000" else "111111"

    for _ in range(otp_service.MAX_VERIFY_ATTEMPTS):
        assert otp_service.verify_otp("user@example.com", wrong, purpose="password_reset") is False

    # Even the correct code no longer works — the entry was burned.
    assert otp_service._store_key("user@example.com", "password_reset") not in otp_service._otp_store
    assert otp_service.verify_otp("user@example.com", code, purpose="password_reset") is False


def test_login_and_password_reset_codes_do_not_share_a_slot(monkeypatch) -> None:
    """Requesting one purpose's code must not overwrite, or be usable to
    satisfy, the other purpose -- the historical bug this store used to
    have when both were keyed by bare email."""

    _stub_smtp(monkeypatch)
    otp_service.generate_and_send_otp(
        "user@example.com", "user@example.com", purpose="login"
    )
    login_code = _entry("user@example.com", "login").code

    otp_service.generate_and_send_otp(
        "user@example.com", "user@example.com", purpose="password_reset"
    )
    reset_code = _entry("user@example.com", "password_reset").code

    # Requesting the reset code did not clobber the still-valid login code.
    assert otp_service.verify_otp("user@example.com", login_code, purpose="login") is True
    # The login code is not accepted for the password_reset purpose.
    assert (
        otp_service.verify_otp("user@example.com", reset_code, purpose="login") is False
    )
    assert (
        otp_service.verify_otp("user@example.com", reset_code, purpose="password_reset")
        is True
    )


def test_console_delivery_logs_instead_of_emailing(monkeypatch, caplog) -> None:
    smtp_cls = MagicMock()
    monkeypatch.setattr(otp_service.smtplib, "SMTP", smtp_cls)
    monkeypatch.setattr(otp_service.settings, "OTP_DELIVERY", "console")

    with caplog.at_level(logging.INFO, logger=otp_service.logger.name):
        otp_service.generate_and_send_otp(
            "user@example.com", "user@example.com", purpose="login"
        )

    code = _entry("user@example.com", "login").code
    smtp_cls.assert_not_called()
    assert any(code in message for message in caplog.messages)


def test_send_otp_background_delivers_successfully(monkeypatch) -> None:
    _stub_smtp(monkeypatch)

    otp_service.send_otp_background(
        "user@example.com", "user@example.com", purpose="login"
    )

    assert _entry("user@example.com", "login").code is not None
