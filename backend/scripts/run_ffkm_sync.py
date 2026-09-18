#!/usr/bin/env python3
import asyncio
from app.services.ffkm_tournament_sync import run_ffkm_sync_locked

async def main():
    stats = await run_ffkm_sync_locked()
    print(stats.as_dict() if stats is not None else {"skipped": True, "reason": "already running"})

asyncio.run(main())
