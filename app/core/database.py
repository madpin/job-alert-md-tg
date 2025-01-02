# job_monitor/app/core/database.py
"""Database setup module."""

# Add future imports here if needed
from __future__ import annotations

# Set encode as utf-8
# -*- coding: utf-8 -*-

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from core.config import Settings

settings = Settings()

# Using a persistent file-based SQLite database for simplicity.
engine = create_engine(
    settings.DATABASE_URL,
    connect_args={"check_same_thread": False},  # Only for SQLite
)

# echo=True enables logging of SQL statements, useful for debugging.
# engine = create_engine(settings.DATABASE_URL, echo=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Performance characteristics:
# - Engine creation is relatively expensive, but only happens once.
# - Session creation is lightweight.
# Resource usage details:
# - Connection pooling can be configured on the engine for resource efficiency.
# Threading considerations:
# - Engine is thread-safe. SessionLocal should be used in a thread-local context.
# Error handling approach:
# - SQLAlchemy raises exceptions for database errors, which should be handled
#   in the application logic.
