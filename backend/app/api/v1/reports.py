from datetime import date
from uuid import UUID

from fastapi import APIRouter, Depends, Query
from fastapi.responses import Response
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import ManagerOrAdmin
from app.db.session import get_db
from app.schemas.report import ReportMentionsOut
from app.services.report_service import (
    export_mentions_csv,
    export_mentions_docx,
    export_mentions_xlsx,
    get_mentions_report,
)

router = APIRouter(prefix="/reports", tags=["reports"])


@router.get("/mentions", response_model=ReportMentionsOut)
async def report_mentions(
    _: ManagerOrAdmin,
    session: AsyncSession = Depends(get_db),
    stream_id: UUID | None = Query(default=None),
    date_from: date | None = Query(default=None),
    date_to: date | None = Query(default=None),
) -> ReportMentionsOut:
    return await get_mentions_report(
        session,
        stream_event_id=stream_id,
        date_from=date_from,
        date_to=date_to,
    )


@router.get("/export.docx")
async def export_docx(
    _: ManagerOrAdmin,
    session: AsyncSession = Depends(get_db),
    stream_id: UUID | None = Query(default=None),
    date_from: date | None = Query(default=None),
    date_to: date | None = Query(default=None),
) -> Response:
    data = await export_mentions_docx(
        session,
        stream_event_id=stream_id,
        date_from=date_from,
        date_to=date_to,
    )
    return Response(
        content=data,
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        headers={"Content-Disposition": 'attachment; filename="mentions_report.docx"'},
    )


@router.get("/export.csv")
async def export_csv(
    _: ManagerOrAdmin,
    session: AsyncSession = Depends(get_db),
    stream_id: UUID | None = Query(default=None),
    date_from: date | None = Query(default=None),
    date_to: date | None = Query(default=None),
) -> Response:
    data = await export_mentions_csv(
        session,
        stream_event_id=stream_id,
        date_from=date_from,
        date_to=date_to,
    )
    return Response(
        content=data,
        media_type="text/csv; charset=utf-8",
        headers={"Content-Disposition": 'attachment; filename="mentions_report.csv"'},
    )


@router.get("/export.xlsx")
async def export_xlsx(
    _: ManagerOrAdmin,
    session: AsyncSession = Depends(get_db),
    stream_id: UUID | None = Query(default=None),
    date_from: date | None = Query(default=None),
    date_to: date | None = Query(default=None),
) -> Response:
    data = await export_mentions_xlsx(
        session,
        stream_event_id=stream_id,
        date_from=date_from,
        date_to=date_to,
    )
    return Response(
        content=data,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": 'attachment; filename="mentions_report.xlsx"'},
    )
