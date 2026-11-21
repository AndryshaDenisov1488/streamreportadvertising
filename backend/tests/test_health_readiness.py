import asyncio
from unittest.mock import AsyncMock, Mock

import pytest
from fastapi import HTTPException

from app.api.health import health_ready, migration_heads


@pytest.mark.parametrize("schema", ["current", "old", "empty", "unreadable", "offline"])
def test_readiness_requires_current_schema(schema):
    rows = Mock()
    rows.scalars.return_value.all.return_value = {
        "current": list(migration_heads()), "old": ["old"], "empty": [],
    }.get(schema, [])
    database = AsyncMock()
    error = RuntimeError("internal connection details")
    database.execute.side_effect = (
        [error] if schema == "offline" else [Mock(), error if schema == "unreadable" else rows]
    )
    if schema == "current":
        assert asyncio.run(health_ready(database))["status"] == "ready"
    else:
        with pytest.raises(HTTPException) as caught:
            asyncio.run(health_ready(database))
        assert caught.value.status_code == 503
        assert str(error) not in str(caught.value.detail)
