"""Scrape an individual Pararius listing page for contact links.

Given a listing URL, this module finds the appropriate contact link
(either a direct agent contact form or a viewing request form).
"""

import requests
from bs4 import BeautifulSoup


def house_details_scraper(url):
    """Extract the contact or viewing-request link from a listing page.

    Args:
        url: Full URL of a Pararius listing page.

    Returns:
        A tuple of (contact_type, full_url) where contact_type is either
        "agent" or "viewing". Returns None if the page can't be fetched.
    """
    response = requests.get(url, timeout=30)

    if response.status_code != 200:
        print(f"Failed to retrieve {url} — status {response.status_code}")
        return None

    soup = BeautifulSoup(response.content, "html.parser")

    sidebar_sections = soup.find_all("section", class_="page__sidebar")

    agent_link = ""
    viewing_link = ""

    for section in sidebar_sections:
        # Try to find the direct agent contact link
        try:
            agent_link = section.find("a", class_="agent-summary__agent-contact-request")["href"]
        except (TypeError, KeyError):
            print(f"No agent contact link found for {url}")

        # Try to find the viewing request link
        try:
            viewing_class = (
                "agent-summary__agent-viewing-request "
                "agent-summary__agent-viewing-request--ghost"
            )
            viewing_link = section.find("a", class_=viewing_class)["href"]
        except (TypeError, KeyError):
            print(f"No viewing link found for {url}")
            viewing_link = ""

    # Prefer the viewing link when available, fall back to agent contact
    if viewing_link:
        return ("viewing", "https://www.pararius.com" + viewing_link)
    return ("agent", "https://www.pararius.com" + agent_link)
