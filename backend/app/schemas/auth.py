from pydantic import BaseModel, EmailStr, Field, model_validator

from app.schemas.user import UserOut


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class ForgotPasswordIn(BaseModel):
    email: EmailStr


class ForgotPasswordOut(BaseModel):
    message: str = (
        "Если указанный адрес зарегистрирован в системе, мы отправили на него ссылку для сброса пароля."
    )


class PasswordResetValidateOut(BaseModel):
    ok: bool


class ResetPasswordIn(BaseModel):
    token: str = Field(min_length=20, max_length=512)
    new_password: str = Field(min_length=8, max_length=128)
    new_password_confirm: str = Field(min_length=8, max_length=128)

    @model_validator(mode="after")
    def passwords_match(self) -> "ResetPasswordIn":
        if self.new_password != self.new_password_confirm:
            raise ValueError("Пароли должны совпадать")
        return self


class RefreshRequest(BaseModel):
    refresh_token: str | None = None


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserOut


class MeOut(BaseModel):
    user: UserOut
