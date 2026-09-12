"""Tests for the OTP generation/verification helpers behind password reset."""

from unittest.mock import MagicMock

import pytest

from app.services import otp_service
from app.utils.exceptions import ExternalServiceError


def teardown_function() -> None:
    otp_service._otp_store.clear()


def _stub_smtp(monkeypatch) -> MagicMock:
    smtp_instance = MagicMock()
    smtp_instance.__enter__.return_value = smtp_instance
    smtp_cls = MagicMock(return_value=smtp_instance)
    monkeypatch.setattr(otp_service.smtplib, "SMTP", smtp_cls)
    return smtp_instance


def test_generated_code_is_six_digits_and_emailed(monkeypatch) -> None:
    smtp = _stub_smtp(monkeypatch)

    otp_service.generate_and_send_otp("user@example.com", "user@example.com")

    entry = otp_service._otp_store["user@example.com"]
    assert len(entry.code) == 6
    assert entry.code.isdigit()
    smtp.starttls.assert_called_once()
    smtp.login.assert_called_once()
    smtp.send_message.assert_called_once()


def test_correct_code_verifies_and_is_consumed(monkeypatch) -> None:
    _stub_smtp(monkeypatch)
    otp_service.generate_and_send_otp("user@example.com", "user@example.com")
    code = otp_service._otp_store["user@example.com"].code

    assert otp_service.verify_otp("user@example.com", code) is True
    assert "user@example.com" not in otp_service._otp_store
    # Re-submitting the now-consumed code fails.
    assert otp_service.verify_otp("user@example.com", code) is False


@pytest.mark.parametrize("unset", [None, ""])
@pytest.mark.parametrize("field", ["GMAIL_ADDRESS", "GMAIL_APP_PASSWORD"])
def test_unconfigured_email_raises_without_sending_or_storing(
    monkeypatch, field: str, unset: str | None
) -> None:
    # "" is what docker-compose's ${GMAIL_ADDRESS:-} yields when unset.
    smtp = _stub_smtp(monkeypatch)
    monkeypatch.setattr(otp_service.settings, field, unset)

    with pytest.raises(ExternalServiceError):
        otp_service.generate_and_send_otp("user@example.com", "user@example.com")

    otp_service.smtplib.SMTP.assert_not_called()
    smtp.login.assert_not_called()
    assert "user@example.com" not in otp_service._otp_store


def test_unknown_identity_fails_without_raising() -> None:
    assert otp_service.verify_otp("never-requested@example.com", "000000") is False


def test_expired_code_fails_and_is_removed(monkeypatch) -> None:
    _stub_smtp(monkeypatch)
    otp_service.generate_and_send_otp("user@example.com", "user@example.com")
    otp_service._otp_store["user@example.com"].expires_at -= otp_service.OTP_TTL_SECONDS + 1

    assert otp_service.verify_otp("user@example.com", "000000") is False
    assert "user@example.com" not in otp_service._otp_store


def test_wrong_guess_does_not_burn_a_still_valid_code(monkeypatch) -> None:
    _stub_smtp(monkeypatch)
    otp_service.generate_and_send_otp("user@example.com", "user@example.com")
    code = otp_service._otp_store["user@example.com"].code
    wrong = "000000" if code != "000000" else "111111"

    assert otp_service.verify_otp("user@example.com", wrong) is False
    assert otp_service.verify_otp("user@example.com", code) is True


def test_code_is_burned_after_max_attempts(monkeypatch) -> None:
    _stub_smtp(monkeypatch)
    otp_service.generate_and_send_otp("user@example.com", "user@example.com")
    code = otp_service._otp_store["user@example.com"].code
    wrong = "000000" if code != "000000" else "111111"

    for _ in range(otp_service.MAX_VERIFY_ATTEMPTS):
        assert otp_service.verify_otp("user@example.com", wrong) is False

    # Even the correct code no longer works — the entry was burned.
    assert "user@example.com" not in otp_service._otp_store
    assert otp_service.verify_otp("user@example.com", code) is False
