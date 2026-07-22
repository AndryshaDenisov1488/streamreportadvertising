"""Pytest bootstrap: require a non-placeholder JWT_SECRET before app imports."""

from __future__ import annotations

import os

# Must run before test modules import app.main / get_settings (SEC-AUTH-004)
os.environ.setdefault(
    "JWT_SECRET",
    "unit-test-only-jwt-secret-value-32chars-min",
)
os.environ.setdefault("ENVIRONMENT", "test")
