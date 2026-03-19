from app.models.user import User


def user_display_name(user: User) -> str:
    s = f"{user.last_name} {user.first_name}".strip()
    return s if s else user.email
