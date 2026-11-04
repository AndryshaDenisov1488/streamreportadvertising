import pytest
from pydantic import ValidationError

from app.schemas.platform import AcceptInviteIn, InviteCreate
from app.services.invite_service import split_full_name


def test_split_full_name_keeps_patronymic_with_given_name() -> None:
    first_name, last_name = split_full_name("Иванов Иван Иванович")
    assert last_name == "Иванов"
    assert first_name == "Иван Иванович"


def test_split_full_name_requires_two_words() -> None:
    with pytest.raises(Exception) as exc:
        split_full_name("Иванов")
    assert getattr(exc.value, "status_code", None) == 400


def test_invite_create_rejects_single_word_name() -> None:
    with pytest.raises(ValidationError):
        InviteCreate(email="op@example.com", role="OPERATOR", full_name="Иванов")


def test_accept_invite_requires_matching_passwords() -> None:
    with pytest.raises(ValidationError):
        AcceptInviteIn(token="a" * 20, password="long-enough", password_confirm="other-pass")


def test_accept_invite_url_uses_public_base(monkeypatch: pytest.MonkeyPatch) -> None:
    from app.core.config import get_settings
    from app.services.invite_email_service import accept_invite_url

    settings = get_settings()
    monkeypatch.setattr(settings, "app_public_base_url", "https://streaming.mainstreamfs.ru/")
    monkeypatch.setattr(settings, "smtp_host", "smtp.example.com")
    url = accept_invite_url("abc+def/token")
    assert url == "https://streaming.mainstreamfs.ru/accept-invite?token=abc%2Bdef%2Ftoken"
