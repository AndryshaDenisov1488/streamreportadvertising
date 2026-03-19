"""Сид начальных пользователей и демо-события. Запуск: python -m scripts.seed (из каталога backend, PYTHONPATH=.).

Почты и пароль задаются через переменные окружения (удобно для прода):
  SEED_ADMIN_EMAIL, SEED_MANAGER_EMAIL, SEED_OPERATOR_EMAIL, SEED_PASSWORD
Значения по умолчанию — как в демо (example.com).

Чистый прод (только суперадмин, без демо-мероприятия и без менеджера/оператора):
  SEED_ONLY_SUPERADMIN=1
"""

import asyncio
import os
import uuid
from datetime import date
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import select

load_dotenv(Path(__file__).resolve().parent.parent / ".env")

from app.core.security import hash_password
from app.db.session import AsyncSessionLocal
from app.models.enums import UserRole
from app.models.stream import StreamDay, StreamEvent
from app.models.user import User


def _seed_env() -> tuple[str, str, str, str]:
    admin = os.getenv("SEED_ADMIN_EMAIL", "admin@example.com").strip()
    manager = os.getenv("SEED_MANAGER_EMAIL", "manager@example.com").strip()
    operator = os.getenv("SEED_OPERATOR_EMAIL", "operator@example.com").strip()
    password = os.getenv("SEED_PASSWORD", "ChangeMe123!")
    return admin, manager, operator, password


async def main() -> None:
    admin_email, manager_email, operator_email, seed_password = _seed_env()
    only_superadmin = os.getenv("SEED_ONLY_SUPERADMIN", "").strip().lower() in ("1", "true", "yes", "on")

    async with AsyncSessionLocal() as session:
        res = await session.execute(select(User.id).where(User.email == admin_email))
        if res.scalar_one_or_none():
            print(f"Сид уже выполнен (найден {admin_email}).")
            return

        pwd_hash = hash_password(seed_password)
        if only_superadmin:
            users = [
                User(
                    id=uuid.uuid4(),
                    email=admin_email,
                    first_name="Администратор",
                    last_name="Системный",
                    password_hash=pwd_hash,
                    role=UserRole.SUPERADMIN,
                    is_active=True,
                    suggest_password_change=False,
                    onboarding_completed=True,
                ),
            ]
            for u in users:
                session.add(u)
            await session.commit()
            print(f"Сид (только суперадмин): {admin_email} / пароль из SEED_PASSWORD")
            return

        users = [
            User(
                id=uuid.uuid4(),
                email=admin_email,
                first_name="Администратор",
                last_name="Системный",
                password_hash=pwd_hash,
                role=UserRole.SUPERADMIN,
                is_active=True,
                suggest_password_change=False,
                onboarding_completed=True,
            ),
            User(
                id=uuid.uuid4(),
                email=manager_email,
                first_name="Михаил",
                last_name="Петров",
                password_hash=pwd_hash,
                role=UserRole.STREAM_MANAGER,
                is_active=True,
                suggest_password_change=False,
                onboarding_completed=True,
            ),
            User(
                id=uuid.uuid4(),
                email=operator_email,
                first_name="Алексей",
                last_name="Сидоров",
                password_hash=pwd_hash,
                role=UserRole.OPERATOR,
                is_active=True,
                suggest_password_change=False,
                onboarding_completed=True,
            ),
        ]
        for u in users:
            session.add(u)
        await session.flush()

        mgr_id = next(u.id for u in users if u.role == UserRole.STREAM_MANAGER)
        ev = StreamEvent(
            title="Демо: чемпионат",
            start_date=date.today(),
            duration_days=3,
            created_by_id=mgr_id,
        )
        session.add(ev)
        await session.flush()
        for i in range(1, 4):
            session.add(
                StreamDay(
                    stream_event_id=ev.id,
                    day_index=i,
                    stream_url=f"rtmp://demo.example/live/day{i}",
                    server_url="https://demo-cdn.example",
                    stream_key=f"key-day-{i}",
                )
            )

        await session.commit()
        print(
            f"Сид выполнен: {admin_email}, {manager_email}, {operator_email} / пароль из SEED_PASSWORD "
            f"(по умолчанию ChangeMe123!)"
        )


if __name__ == "__main__":
    asyncio.run(main())
