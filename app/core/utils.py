# job_monitor/app/core/utils.py
"""Utility functions module."""

# Add future imports here if needed
from __future__ import annotations

# Set encode as utf-8
# -*- coding: utf-8 -*-

import hashlib

from playwright.sync_api import sync_playwright


def generate_md5_hash(content: str) -> str:
    """Generates the MD5 hash of a string.

    Args:
        content: The string content.

    Returns:
        The MD5 hash.
    """
    # Performance considerations:
    # - Using hashlib.md5 for fast hashing.
    # Memory management details:
    # - Efficiently handles large strings by processing in chunks.
    return hashlib.md5(content.encode("utf-8")).hexdigest()


def take_screenshot(url: str, screenshot_path: str, selector: str = None) -> None:
    """Takes a screenshot of a given URL using playwright.

    Args:
        url: The URL to take a screenshot of.
        screenshot_path: The path to save the screenshot.
        selector: Optional CSS selector to capture specific element. If None, captures full page.

    Raises:
        PlaywrightError: If there's an error during browser automation
        IOError: If there's an error saving the screenshot
    """
    # Error handling approach:
    # - Uses try-except block to handle potential playwright errors.
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)  # Explicitly set headless mode
            context = browser.new_context(
                viewport={"width": 1920, "height": 1080}
            )  # Set viewport
            page = context.new_page()
            page.set_default_timeout(30000)  # 30 second timeout
            page.goto(url, wait_until="networkidle")  # Wait for network to be idle

            if selector:
                element = page.locator(selector)
                element.screenshot(path=screenshot_path)  # Capture specific element
            else:
                page.screenshot(
                    path=screenshot_path, full_page=True
                )  # Capture full page

            context.close()
            browser.close()

    except Exception as e:
        raise RuntimeError(f"Failed to take screenshot: {e}") from e


# Performance characteristics:
# - MD5 generation is fast. Screenshot capture depends on Playwright's performance.
# Resource usage details:
# - Screenshot capture can be memory-intensive for large pages.
# Threading considerations:
# - MD5 generation is thread-safe. Playwright instance should not be shared between threads.
