# job_monitor/app/scrapers/rezoomo_scraper.py
"""Rezoomo scraper module."""

# Add future imports here if needed
from __future__ import annotations

# Set encode as utf-8
# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup

from core.utils import take_screenshot
from scrapers.base_scraper import BaseScraper


class RezoomoScraper(BaseScraper):
    """Scraper for Rezoomo websites."""

    def scrape(self, url: str) -> str:
        """Scrapes the given Rezoomo URL.
        Use requests to download the webpage and Beautifulsoup to parse the page HTML.
        Args:
            url: The URL to scrape.

        Returns:
            The scraped content.
        """
        # Error handling approach:
        # - Uses try-except block to handle request and parsing errors.
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()  # Raise an exception for bad status codes

            soup = BeautifulSoup(response.content, "html.parser")

            # Extract all text content from the job listing
            job_listing_content = []

            # Extract job details from window.initData
            script_tag = soup.find(
                "script", string=lambda text: text and "window.initData" in text
            )
            if script_tag:
                # Extract relevant job information from the script
                # This would need parsing of the JavaScript object
                job_info = "Job information from script"
                job_listing_content.append(job_info)
            else:
                # Fallback to searching for job-block elements
                job_blocks = soup.find_all(
                    "div",
                    class_="job-block",
                )

                for job_block in job_blocks:
                    # Extract job details
                    date = job_block.find("div", class_="date-field").get_text(
                        strip=True
                    )
                    title = job_block.find("p", class_="jobTitle").get_text(strip=True)
                    location = job_block.find(
                        "i", class_="fa-map-marker-alt"
                    ).parent.get_text(strip=True)
                    job_type = job_block.find("i", class_="fa-clock").parent.get_text(
                        strip=True
                    )

                    # Combine job details
                    job_info = f"{date} | {title} | {location} | {job_type}"
                    job_listing_content.append(job_info)

            return " ".join(job_listing_content)

        except requests.exceptions.RequestException as e:
            print(f"Error during request: {e}")
            return ""
        except Exception as e:
            print(f"Error parsing content: {e}")
            return ""

    def take_screenshot(self, url: str, screenshot_path: str) -> None:
        """Takes a screenshot of the given URL.


        Args:
            url: The URL to take a screenshot of.
            screenshot_path: The file path to save the screenshot to.
        """
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, "html.parser")

            # Find the h2 element by its text content
            job_listing_h2 = soup.find("h2", string="Job listing")
            if job_listing_h2:
                # Get the parent div
                parent_div = job_listing_h2.find_parent("div")

                if parent_div:
                    # Get the div selector by combining class names or other attributes
                    div_selector = f"div.{' '.join(parent_div.get('class', []))}"
                    take_screenshot(url, screenshot_path, div_selector)
                else:
                    print(
                        f"Could not find parent div for job listing h2 element at URL: {url}"
                    )
                    take_screenshot(url, screenshot_path)
            else:
                print(
                    f"Could not find h2 element with text 'Job listing' at URL: {url}"
                )
                take_screenshot(url, screenshot_path)
        except requests.exceptions.RequestException as e:
            print(f"Network error while accessing {url}: {str(e)}")
        except Exception as e:
            print(
                f"Unexpected error while processing {url} for screenshot at {screenshot_path}: {str(e)}"
            )
            print(f"Error type: {type(e).__name__}")


# Performance characteristics:
# - Depends on the network speed and the complexity of the webpage.
# - BeautifulSoup parsing can be optimized further for specific HTML structures.
# Resource usage details:
# - Memory usage depends on the size of the webpage.
# Threading considerations:
# - requests is thread-safe. BeautifulSoup can be used in separate threads.
