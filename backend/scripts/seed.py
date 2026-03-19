"""Сид начальных пользователей и демо-события. Запуск: python -m scripts.seed (из каталога backend, PYTHONPATH=.)."""

import asyncio
import uuid
from datetime import date

from sqlalchemy import select

from app.core.security import hash_password
from app.db.session import AsyncSessionLocal
from app.models.enums import UserRole
from app.models.stream import StreamDay, StreamEvent
from app.models.user import User


async def main() -> None:
    async with AsyncSessionLocal() as session:
        res = await session.execute(select(User.id).where(User.email == "admin@example.com"))
        if res.scalar_one_or_none():
            print("Сид уже выполнен (найден admin@example.com).")
            return

        users = [
            User(
                id=uuid.uuid4(),
                email="admin@example.com",
                password_hash=hash_password("ChangeMe123!"),
                role=UserRole.SUPERADMIN,
                is_active=True,
            ),
            User(
                id=uuid.uuid4(),
                email="manager@example.com",
                password_hash=hash_password("ChangeMe123!"),
                role=UserRole.STREAM_MANAGER,
                is_active=True,
            ),
            User(
                id=uuid.uuid4(),
                email="operator@example.com",
                password_hash=hash_password("ChangeMe123!"),
                role=UserRole.OPERATOR,
                is_active=True,
            ),
        ]
        for u in users:
            session.add(u)
        await session.flush()

        mgr_id = next(u.id for u in users if u.role == UserRole.STREAM_MANAGER)
        ev = StreamEvent(
            title="Демо: чемпионат (Москва)",
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
        print("Сид выполнен: admin@example.com, manager@example.com, operator@example.com / ChangeMe123!")


if __name__ == "__main__":
    asyncio.run(main())
