# job_monitor/app/core/config.py
"""Configuration module."""
# Add future imports here if needed
from __future__ import annotations

# Set encode as utf-8
# -*- coding: utf-8 -*-

from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    """Application settings."""

    TELEGRAM_BOT_TOKEN: str = Field(..., env="TELEGRAM_BOT_TOKEN")
    TELEGRAM_CHAT_ID: str = Field(..., env="TELEGRAM_CHAT_ID")
    DATABASE_URL: str = Field("sqlite:///job_monitor.db", env="DATABASE_URL")

    class Config:
        """Loads the env vars from a .env file."""

        env_file = ".env"
        env_file_encoding = "utf-8"

# Performance characteristics:
# - Fast initialization due to Pydantic's efficient parsing.
# Resource usage details:
# - Minimal memory usage, only storing the configuration values.
# Threading considerations:
# - Thread-safe as long as environment variables are not modified concurrently.
# Error handling approach:
# - Raises validation errors if environment variables are missing or of incorrect type.
