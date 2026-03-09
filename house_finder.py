"""Scrape Pararius apartment listings and auto-contact estate agents.

This is the main entry point. It scrapes each configured city/price
combination, stores new listings in a CSV tracker, and contacts agents
for any listing that hasn't been contacted yet.
"""

import os
import requests
from bs4 import BeautifulSoup
import pandas as pd
from house import House
from contact_estate_agent import ContactDetails
import house_detail
import contact_estate_agent

BASE_URL = "https://www.pararius.com/apartments"

# --- Configuration -----------------------------------------------------------

# Cities to search — just add or remove names from this list.
# Names must match the Pararius URL slug (e.g. "den-haag", "alphen-aan-den-rijn").
CITIES = [
    "utrecht",
    "gouda",
    "leiden",
    "den-haag",
    "alphen-aan-den-rijn",
    "nieuwegein",
    "houten",
    "bunnik",
    "odijk",
    "zeist",
    "de-bilt",
    "bilthoven",
    "baarn",
    "hilversum",
    "amersfoort",
]

# Price range (EUR per month)
MIN_PRICE = 0
MAX_PRICE = 1200

# Fill in your own details before running.
FIRST_NAME = "YOUR_FIRST_NAME"
LAST_NAME = "YOUR_LAST_NAME"
EMAIL = "YOUR_EMAIL"
PHONE = "YOUR_PHONE"
MESSAGE = "YOUR_MESSAGE"

DATA_FILE = "data.csv"
# -----------------------------------------------------------------------------


def build_search_urls(cities, min_price, max_price):
    """Build Pararius search URLs from the city list and price range."""
    return [f"{BASE_URL}/{city}/{min_price}-{max_price}" for city in cities]


def scrape_pararius(dataframe, url):
    """Scrape a single Pararius search page and append new listings to *dataframe*.

    Args:
        dataframe: pandas DataFrame that tracks all known listings.
        url: Pararius search URL to scrape.

    Returns:
        The updated DataFrame (rows are added in-place as well).
    """
    response = requests.get(url, timeout=30)

    if response.status_code != 200:
        print(f"Failed to retrieve {url} — status {response.status_code}")
        return dataframe

    soup = BeautifulSoup(response.content, "html.parser")
    listings = soup.find_all("section", class_="listing-search-item")

    for listing in listings:
        title = listing.find("a", class_="listing-search-item__link--title").text.strip()
        location = listing.find("div", class_="listing-search-item__sub-title").text.strip()
        price = listing.find("div", class_="listing-search-item__price").text.strip()
        surface_area = listing.find(
            "li",
            class_="illustrated-features__item illustrated-features__item--surface-area",
        ).text.strip()
        link = listing.find("a", class_="listing-search-item__link")["href"]

        house = House(title, location, price, surface_area, "https://www.pararius.com" + link)

        # Only add the listing if it isn't already tracked
        if not dataframe["Link"].str.contains(house.link, regex=False).any():
            dataframe.loc[len(dataframe)] = house.to_list()

    return dataframe


# --- Main execution ----------------------------------------------------------

if __name__ == "__main__":
    # Load existing data or create a fresh DataFrame
    if os.path.exists(DATA_FILE):
        df = pd.read_csv(DATA_FILE)
    else:
        df = pd.DataFrame(
            columns=["Title", "Location", "Price", "Surface Area", "Link", "Contacted"]
        )

    # Scrape every configured search page
    for search_url in build_search_urls(CITIES, MIN_PRICE, MAX_PRICE):
        scrape_pararius(df, search_url)

    # Contact agents for listings we haven't reached out to yet
    contact = ContactDetails(FIRST_NAME, LAST_NAME, EMAIL, PHONE, MESSAGE)
    for idx, row in df[~df["Contacted"].astype(bool)].iterrows():
        contact_link = house_detail.house_details_scraper(row["Link"])
        print(contact_link)

        if contact_link[0] == "agent":
            sent = contact_estate_agent.send_message_to_agent(
                contact_link[1], contact,
            )
        else:
            sent = contact_estate_agent.set_viewing(
                contact_link[1], contact,
            )

        if sent:
            df.at[idx, "Contacted"] = True

    # Persist updated data
    df.to_csv(DATA_FILE, index=False)
