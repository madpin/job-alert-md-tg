# job_monitor/app/main.py
"""Main application logic module."""

# Add future imports here if needed
from __future__ import annotations

# Set encode as utf-8
# -*- coding: utf-8 -*-

import os

from core.config import Settings
from core.database import SessionLocal
from core.utils import generate_md5_hash
from data_models import Website
from notifiers.telegram_notifier import TelegramNotifier
from scrapers.base_scraper import BaseScraper
from scrapers.occupop_scraper import OccupopScraper
from scrapers.rezoomo_scraper import RezoomoScraper


def get_scraper(scraper_type: str) -> BaseScraper:
    """Returns the appropriate scraper based on the website type.

    Args:
        scraper_type: The type of scraper.

    Returns:
        The scraper instance.

    Raises:
        ValueError: If an invalid scraper type is provided.
    """
    # Error handling approach:
    # - Raises ValueError for unknown scraper types.
    if scraper_type == "rezoomo":
        return RezoomoScraper()
    elif scraper_type == "occupop":
        return OccupopScraper()
    else:
        raise ValueError(f"Invalid scraper type: {scraper_type}")


def monitor_website(website: Website, notifier: TelegramNotifier) -> None:
    """Monitors a single website for changes.

    Args:
        website: The Website object to monitor.
        notifier: The TelegramNotifier instance.
    """
    scraper = get_scraper(website.scraper_type)
    scraped_content = scraper.scrape(website.url)

    if not scraped_content:
        print(f"Failed to scrape content from {website.url}")
        return

    new_content_hash = generate_md5_hash(scraped_content)

    # Ensure the screenshots directory exists
    screenshots_dir = "screenshots"
    os.makedirs(screenshots_dir, exist_ok=True)

    # Define screenshot path
    screenshot_filename = f"{website.url.split('//')[1].replace('/', '_')}.png"
    screenshot_path = os.path.join(screenshots_dir, screenshot_filename)

    # Check if the content has changed
    if website.last_content_hash != new_content_hash:
        print(f"Change detected for {website.url}")
        # Take a screenshot
        scraper.take_screenshot(website.url, screenshot_path)
        # Send notification
        notifier.send_alert(
            f"Change detected for {website.url}",
            files=[screenshot_path],
        )

        # Update the last_content_hash in the database
        db = SessionLocal()
        try:
            db_website = db.query(Website).filter(Website.url == website.url).first()
            if db_website:
                db_website.last_content_hash = new_content_hash
                db.commit()
        except Exception as e:
            db.rollback()
            print(f"Error updating database: {e}")
        finally:
            db.close()
    else:
        print(f"NO change detected for {website.url}")
        # Take a screenshot
        scraper.take_screenshot(website.url, screenshot_path)
        # Send notification
        notifier.send_message(
            f"No change detected for {website.url}",
            files=[screenshot_path],
        )


def run_monitoring() -> None:
    """Runs the monitoring process for all websites."""
    settings = Settings()

    db = SessionLocal()
    try:
        websites = db.query(Website).all()
        for website in websites:
            monitor_website(
                website,
                TelegramNotifier(
                    settings.TELEGRAM_BOT_TOKEN, settings.TELEGRAM_CHAT_ID
                ),
            )
    except Exception as e:
        print(f"Error during monitoring: {e}")
    finally:
        db.close()
    TelegramNotifier(
        settings.TELEGRAM_BOT_TOKEN, settings.TELEGRAM_CHAT_ID
    ).send_message("Monitoring completed.")


# Performance characteristics:
# - Main logic, performance depends on the individual components used.
# Resource usage details:
# - Memory usage depends on the number of websites and the size of scraped content.
# Threading considerations:
# - Can be parallelized to monitor multiple websites concurrently.
# Error handling approach:
# - Handles database, scraper, and notification errors gracefully.
