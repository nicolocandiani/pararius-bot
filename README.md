# Pararius Bot

A bot that scrapes [Pararius](https://www.pararius.com) apartment listings and automatically contacts real estate agents. It tracks which listings have already been contacted so it never messages the same agent twice.

Uses **Selenium** to drive a real browser session for form submission.

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Make sure you have [Firefox](https://www.mozilla.org/firefox/) installed (or switch the WebDriver in `contact_estate_agent.py` to Chrome).

3. Open `house_finder.py` and fill in the configuration section at the top:
   - `SEARCH_URLS` — the Pararius search pages you want to monitor.
   - `FIRST_NAME`, `LAST_NAME`, `EMAIL`, `PHONE`, `MESSAGE` — your contact details and the message to send.

4. Run the bot:
   ```bash
   python house_finder.py
   ```

5. (Optional) Schedule the script to run every 30–60 minutes using cron or Task Scheduler.

## Project structure

| File | Description |
|---|---|
| `house_finder.py` | Main entry point — scrapes listings and triggers contact |
| `house.py` | `House` data class for a single listing |
| `house_detail.py` | Scrapes a listing page for agent/viewing contact links |
| `contact_estate_agent.py` | Selenium automation to fill and submit contact forms |
| `message.txt` | Template message (currently placeholder text) |
| `data.csv` | Auto-generated at runtime to track contacted listings |

## TO-DO

- [ ] Adapt message to each listing using an LLM
- [ ] Headless browser configuration
- [ ] Investigate CAPTCHA solving
