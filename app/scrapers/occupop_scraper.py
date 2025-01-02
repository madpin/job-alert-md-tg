# job_monitor/app/scrapers/occupop_scraper.py
"""
Occupop scraper module.

This module provides a scraper for Occupop websites, extracting job listings and other relevant information.

Features:
- Scrapes job listings from Occupop career pages.
- Handles request and parsing errors gracefully.
- Provides a method to take screenshots of web pages (using an external utility).

Required packages:
- requests
- beautifulsoup4

Usage:
- Create an instance of OccupopScraper.
- Call the `scrape` method with the URL of the Occupop career page to extract job listings.
- Optionally, use the `take_screenshot` method to capture a screenshot of the page.

Author: tpinto
"""

from __future__ import annotations

import requests
from bs4 import BeautifulSoup

from core.utils import take_screenshot
from scrapers.base_scraper import BaseScraper


class OccupopScraper(BaseScraper):
    """Scraper for Occupop websites."""

    def scrape(self, url: str) -> str:
        """
        Scrapes the given Occupop URL, finds the parent div for "Job listing" text.

        Uses requests to download the webpage and BeautifulSoup to parse the page HTML.

        Args:
            url: The URL to scrape.

        Returns:
            The scraped content of the parent div containing "Job listing", or an empty string if not found or an error occurs.
        """
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)

            soup = BeautifulSoup(response.content, "html.parser")

            # Find the div containing "Job listing" using a more efficient method
            job_listing_section = soup.find(
                "h2", class_=lambda x: x and "css" in x, string="Job listing"
            )

            if job_listing_section:
                # Find the parent div of the h2 element
                parent_div = job_listing_section.find_parent("div")

                if parent_div:
                    return parent_div.get_text(separator=" ", strip=True)
                else:
                    print("Could not find the parent div of 'Job listing' section.")
            else:
                print("Could not find 'Job listing' section.")

        except requests.exceptions.RequestException as e:
            print(f"Error during request: {e}")
        except Exception as e:
            print(f"Error parsing content: {e}")

        return ""

    def take_screenshot(self, url: str, screenshot_path: str) -> None:
        """
        Takes a screenshot of the given URL.

        Args:
            url: The URL to take a screenshot of.
            screenshot_path: The file path to save the screenshot to.
        """
        take_screenshot(url, screenshot_path)
