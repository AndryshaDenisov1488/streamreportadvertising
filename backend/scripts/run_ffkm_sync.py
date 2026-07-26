#!/usr/bin/env python3
import asyncio
from app.db.session import AsyncSessionLocal
from app.services.ffkm_tournament_sync import sync_tournaments_from_ffkm_admin

async def main():
    async with AsyncSessionLocal() as session:
        stats = await sync_tournaments_from_ffkm_admin(session)
        print(stats.as_dict())

asyncio.run(main())
