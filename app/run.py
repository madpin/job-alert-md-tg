# job_monitor/app/run.py
"""Run module."""

# Add future imports here if needed
from __future__ import annotations

# Set encode as utf-8
# -*- coding: utf-8 -*-

from core.database import engine
from data_models import Base, Website
from main import run_monitoring
from core.database import SessionLocal


def create_tables():
    """Creates database tables based on the defined data models."""
    Base.metadata.create_all(bind=engine)


def populate_initial_data():
    """Populates the database with initial data."""

    db = SessionLocal()
    try:
        # Check if the websites already exist
        if (
            not db.query(Website)
            .filter(
                Website.url
                == "https://www.rezoomo.com/company/the-national-maternity-hospital/jobs/?source=iframe"
            )
            .first()
        ):
            website1 = Website(
                url="https://www.rezoomo.com/company/the-national-maternity-hospital/jobs/?source=iframe",
                scraper_type="rezoomo",
            )
            db.add(website1)

        if (
            not db.query(Website)
            .filter(
                Website.url
                == "https://www.rezoomo.com/company/coombe-hospital/jobs/?source=iframe"
            )
            .first()
        ):
            website2 = Website(
                url="https://www.rezoomo.com/company/coombe-hospital/jobs/?source=iframe",
                scraper_type="rezoomo",
            )
            db.add(website2)

        if (
            not db.query(Website)
            .filter(Website.url == "https://therotundahospital.occupop-careers.com/")
            .first()
        ):
            website3 = Website(
                url="https://therotundahospital.occupop-careers.com/",
                scraper_type="occupop",
            )
            db.add(website3)
        db.commit()
        print("Initial data populated successfully.")
    except Exception as e:
        db.rollback()
        print(f"Error populating initial  {e}")
    finally:
        db.close()


def main():
    """Main entry point for the application."""
    create_tables()
    populate_initial_data()
    run_monitoring()


if __name__ == "__main__":
    main()

# Performance characteristics:
# - Table creation is a one-time operation.
# - Monitoring depends on the main application logic.
# Resource usage details:
# - Minimal resource usage for table creation.
# Threading considerations:
# - No threading concerns in this module.
# Error handling approach:
# - Handles database errors during table creation.
