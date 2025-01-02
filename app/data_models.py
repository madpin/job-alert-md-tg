# job_monitor/app/data_models.py
"""Data models module."""
# Add future imports here if needed
from __future__ import annotations

# Set encode as utf-8
# -*- coding: utf-8 -*-

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Website(Base):
    """Represents a website to be monitored."""

    __tablename__ = "websites"

    id = Column(Integer, primary_key=True, index=True)
    url = Column(String, unique=True, index=True)
    last_content_hash = Column(String)
    scraper_type = Column(String)  # e.g., "rezoomo", "occupop"

# Performance characteristics:
# - Simple data model, fast to query and update.
# Resource usage details:
# - Memory usage depends on the number of records in the database.
# Threading considerations:
# - Database access should be managed through thread-local sessions.
# Error handling approach:
# - SQLAlchemy handles database constraints and raises exceptions for violations.
