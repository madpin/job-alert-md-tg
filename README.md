# Job Posting Monitor

[![Build Status](https://img.shields.io/badge/build-passing-brightgreen)](https://github.com/yourusername/job_monitor) <!-- Replace with your build status badge if you have CI/CD -->
[![Code Style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

**Job Posting Monitor** is a Python-based web scraping and notification system that keeps you updated on the latest job postings from your favorite career sites. Never miss a new opportunity again! This tool automatically monitors job listings, takes screenshots of the pages, and sends you instant Telegram alerts whenever changes are detected.

## Features

-   **Monitors Multiple Job Sites:** Currently supports:
    -   [The National Maternity Hospital (Rezoomo)](https://www.rezoomo.com/company/the-national-maternity-hospital/jobs/?source=iframe)
    -   [Coombe Women & Infants University Hospital (Rezoomo)](https://www.rezoomo.com/company/coombe-hospital/jobs/?source=iframe)
    -   [The Rotunda Hospital (Occupop)](https://therotundahospital.occupop-careers.com/) (specifically the "Job listing" section)
-   **Change Detection:** Intelligently detects changes in job postings using MD5 hash comparisons.
-   **Automated Screenshots:** Captures screenshots of job listing pages for visual reference.
-   **Telegram Notifications:** Sends instant updates to your Telegram account.
-   **Alerts for Changes:** Sends a special alert (`@madpin`) when new job postings are detected or existing ones are modified.
-   **Customizable Scheduling:** Runs every 8 hours (configurable) or on-demand.
-   **Extensible Architecture:** Easily add new job sites and notification methods with a modular design.
-   **Dockerized Deployment:** Simple deployment using Docker Compose.
-   **Database Integration:** Uses SQLite and SQLAlchemy for persistent storage of website data.

## Why Use Job Posting Monitor?

-   **Stay Ahead of the Curve:** Be the first to know about new job openings.
-   **Save Time:** No more manually checking multiple websites every day.
-   **Never Miss an Opportunity:** Get instant alerts so you can apply immediately.
-   **Easy to Use:** Simple setup and configuration.

## Getting Started

### Prerequisites

-   [Docker](https://www.docker.com/products/docker-desktop)
-   [Docker Compose](https://docs.docker.com/compose/install/)
-   Python 3.10+ (if running locally without Docker)
-   Telegram Account and Bot (see below)

### Setting up a Telegram Bot

1. **Create a Bot:**
    -   Open Telegram and search for the **BotFather**.
    -   Start a chat with BotFather and follow the instructions to create a new bot (use the `/newbot` command).
    -   **Save your bot's API token**.
2. **Get Your Chat ID:**
    -   Start a chat with your newly created bot.
    -   Send a message to the bot.
    -   To find your chat ID, you can use a bot like `@chatIDrobot` or go to `https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getUpdates` (replace `<YOUR_BOT_TOKEN>` with your bot's token) in your browser and look for the `"chat": {"id": ...}` field in the JSON response.
    -   **Save your chat ID**.

### Installation

1. **Clone the repository:**

    ```bash
    git clone https://github.com/madpin/job-alert-md-tg.git # Replace with your repo URL
    cd job_monitor
    ```

2. **Set up environment variables:**

    -   Create a `.env` file in the root directory of the project.
    -   Add the following environment variables to your `.env` file, replacing the placeholder values:

    ```
    TELEGRAM_BOT_TOKEN=your_telegram_bot_token
    TELEGRAM_CHAT_ID=your_telegram_chat_id
    DATABASE_URL=sqlite:///job_monitor.db
    ```

3. **Build and run with Docker Compose:**

    ```bash
    docker-compose up --build -d
    ```

    This will build the Docker image and start the container in detached mode. The application will automatically run the monitoring job every 8 hours.

### Running on Demand

To trigger the monitoring job manually, you can run:

```bash
docker-compose exec job-monitor python app/run.py
```

### Running Locally (Without Docker)

1. **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

2. **Run the application:**

    ```bash
    python app/run.py
    ```

## Configuration

-   **Scheduling:** The monitoring job is scheduled to run every 8 hours by default. You can customize this using a cron job inside the Docker container or an external scheduler.
-   **Adding New Websites:** To monitor new job sites, you'll need to:
    1. Create a new scraper class in the `app/scrapers` directory that inherits from `BaseScraper`.
    2. Implement the `scrape()` and `take_screenshot()` methods to extract the relevant content and capture a screenshot.
    3. Add the new website's URL and scraper type to the database (using the `Website` model).
    4. Update the `get_scraper()` function in `main.py` to return an instance of your new scraper class.

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues to suggest improvements or new features.

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Make your changes and write tests.
4. Submit a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

-   [Playwright](https://playwright.dev/)
-   [Python Telegram Bot](https://python-telegram-bot.org/)
-   [SQLAlchemy](https://www.sqlalchemy.org/)
-   [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
-   [Requests](https://requests.readthedocs.io/en/master/)

---

**Disclaimer:** Web scraping should be done ethically and responsibly. Always check the website's terms of service and robots.txt before scraping. Be mindful of the website's server load and avoid overloading it with requests. This tool is intended for personal use and should not be used for any malicious or unethical purposes.
