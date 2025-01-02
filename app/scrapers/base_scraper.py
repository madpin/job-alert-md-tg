# job_monitor/app/scrapers/base_scraper.py
"""Base scraper module."""

# Add future imports here if needed
from __future__ import annotations

# Set encode as utf-8
# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod


class BaseScraper(ABC):
    """Abstract base class for web scrapers."""

    @abstractmethod
    def scrape(self, url: str) -> str:
        """Scrapes the given URL and returns the relevant content.

        Args:
            url: The URL to scrape.

        Returns:
            The scraped content.
        """
        ...

    @abstractmethod
    def take_screenshot(self, url: str, screenshot_path: str) -> None:
        """Takes a screenshot of the given URL.

        Args:
            url: The URL to take a screenshot of.
            screenshot_path: The file path to save the screenshot to.
        """
        ...


# Performance characteristics:
# - Abstract class, no performance overhead.
# Resource usage details:
# - Depends on the implementation of the derived scraper classes.
# Threading considerations:
# - Depends on the implementation of the derived scraper classes.
# Error handling approach:
# - Depends on the implementation of the derived scraper classes.
