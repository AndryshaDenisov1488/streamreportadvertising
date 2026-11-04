from types import SimpleNamespace

from app.services.auth_service import pick_user_for_login


def test_login_prefers_username_over_another_users_email() -> None:
    by_name = SimpleNamespace(username="Andrysha", email="admin@mainstreamfs.ru")
    by_mail = SimpleNamespace(username=None, email="andrysha")
    picked = pick_user_for_login([by_mail, by_name], "andrysha")
    assert picked is by_name


def test_login_matches_email_when_there_is_no_such_username() -> None:
    user = SimpleNamespace(username="operator", email="op@example.com")
    picked = pick_user_for_login([user], "OP@example.com")
    assert picked is user
