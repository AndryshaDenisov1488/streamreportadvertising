from fastapi import APIRouter, Depends, Request, Response
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import get_settings
from app.core.deps import AnyAuthenticated
from app.core.limiter import limiter
from app.db.session import get_db
from app.schemas.auth import LoginRequest, MeOut, RefreshRequest, TokenResponse
from app.schemas.platform import AcceptInviteIn
from app.schemas.user import UserOut
from app.services import auth_service, invite_service

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/accept-invite", response_model=TokenResponse)
async def accept_invite_route(
    request: Request,
    response: Response,
    body: AcceptInviteIn,
    session: AsyncSession = Depends(get_db),
) -> TokenResponse:
    user = await invite_service.accept_invite(session, body)
    client_host = request.client.host if request.client else None
    access, refresh, _exp = await auth_service.create_fresh_session(
        session,
        user=user,
        request_ip=client_host,
    )
    settings = get_settings()
    max_age = settings.jwt_refresh_expire_days * 24 * 60 * 60
    response.set_cookie(
        key=settings.refresh_cookie_name,
        value=refresh,
        httponly=True,
        secure=settings.refresh_cookie_secure,
        samesite=settings.refresh_cookie_samesite,
        max_age=max_age,
        path="/",
    )
    return TokenResponse(access_token=access, user=UserOut.model_validate(user))


@router.post("/login", response_model=TokenResponse)
@limiter.limit("30/minute")
async def login(
    request: Request,
    response: Response,
    body: LoginRequest,
    session: AsyncSession = Depends(get_db),
) -> TokenResponse:
    settings = get_settings()
    client_host = request.client.host if request.client else None
    user, access, refresh, _exp = await auth_service.login_user(
        session,
        email=body.email,
        password=body.password,
        request_ip=client_host,
    )
    max_age = settings.jwt_refresh_expire_days * 24 * 60 * 60
    response.set_cookie(
        key=settings.refresh_cookie_name,
        value=refresh,
        httponly=True,
        secure=settings.refresh_cookie_secure,
        samesite=settings.refresh_cookie_samesite,
        max_age=max_age,
        path="/",
    )
    return TokenResponse(access_token=access, user=UserOut.model_validate(user))


@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(
    request: Request,
    response: Response,
    session: AsyncSession = Depends(get_db),
    body: RefreshRequest | None = None,
) -> TokenResponse:
    settings = get_settings()
    token = request.cookies.get(settings.refresh_cookie_name)
    if body and body.refresh_token:
        token = body.refresh_token
    if not token:
        from fastapi import HTTPException, status

        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Нет refresh токена")
    user, access = await auth_service.refresh_access_token(session, token)
    return TokenResponse(access_token=access, user=UserOut.model_validate(user))


@router.post("/logout", status_code=204)
async def logout(
    request: Request,
    response: Response,
    user: AnyAuthenticated,
    session: AsyncSession = Depends(get_db),
    body: RefreshRequest | None = None,
) -> None:
    settings = get_settings()
    token = request.cookies.get(settings.refresh_cookie_name)
    if body and body.refresh_token:
        token = body.refresh_token
    await auth_service.logout_user(session, user_id=user.id, refresh_token=token)
    response.delete_cookie(settings.refresh_cookie_name, path="/")


@router.get("/me", response_model=MeOut)
async def me(user: AnyAuthenticated) -> MeOut:
    return MeOut(user=UserOut.model_validate(user))
