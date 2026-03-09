"""Automate contacting estate agents on Pararius using Selenium.

Provides two actions:
  - send_message_to_agent(): submit the agent contact form.
  - set_viewing(): submit the viewing request form (also selects all available days).
"""

import time
from random import uniform

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from fake_useragent import UserAgent


# -- Shared helpers -----------------------------------------------------------

def _create_driver():
    """Create a Firefox WebDriver with a randomised user-agent string."""
    options = Options()
    user_agent = UserAgent().random
    options.add_argument(f"--user-agent={user_agent}")
    return webdriver.Firefox(options=options)


def _dismiss_cookie_banner(driver):
    """Reject the OneTrust cookie popup if it appears."""
    try:
        driver.find_element(By.ID, "onetrust-reject-all-handler").click()
    except Exception:
        pass  # banner not present — nothing to do


def _fill_contact_form(driver, firstname, lastname, email, phone, message):
    """Locate and fill the standard Pararius contact form fields.

    Adds small random delays between inputs to mimic human typing.
    """
    fields = {
        "listing_contact_agent_form[first_name]": firstname,
        "listing_contact_agent_form[last_name]": lastname,
        "listing_contact_agent_form[email]": email,
        "listing_contact_agent_form[phone]": phone,
        "listing_contact_agent_form[message]": message,
    }

    for field_name, value in fields.items():
        driver.find_element(By.NAME, field_name).send_keys(value)
        time.sleep(uniform(1, 2))


def _submit_form(driver):
    """Click the form submit button and wait for the response."""
    driver.find_element(By.CSS_SELECTOR, ".form .form__button--submit").click()
    time.sleep(5)


# -- Public API ---------------------------------------------------------------

def send_message_to_agent(listing_url, firstname, lastname, email, phone, message):
    """Fill and submit the agent contact form for a listing.

    Args:
        listing_url: Full URL to the Pararius contact-agent page.
        firstname, lastname, email, phone: User contact details.
        message: Body text to send to the agent.

    Returns:
        True if the form was submitted successfully, False otherwise.
    """
    driver = _create_driver()
    try:
        driver.get(listing_url)
        time.sleep(5)

        _dismiss_cookie_banner(driver)
        _fill_contact_form(driver, firstname, lastname, email, phone, message)
        _submit_form(driver)

        print("Message sent successfully!")
        return True
    except Exception as exc:
        print(f"Failed to send message: {exc}")
        return False
    finally:
        driver.quit()


def set_viewing(listing_url, firstname, lastname, email, phone, message):
    """Fill and submit the viewing request form for a listing.

    Same as send_message_to_agent but also selects all available
    day-of-week checkboxes before submitting.

    Args:
        listing_url: Full URL to the Pararius viewing-request page.
        firstname, lastname, email, phone: User contact details.
        message: Body text to send to the agent.

    Returns:
        True if the form was submitted successfully, False otherwise.
    """
    driver = _create_driver()
    try:
        driver.get(listing_url)
        time.sleep(5)

        _dismiss_cookie_banner(driver)
        _fill_contact_form(driver, firstname, lastname, email, phone, message)

        # Select all available day-of-week checkboxes
        checkboxes = driver.find_elements(By.CLASS_NAME, "checkbox-control__label")
        for checkbox in checkboxes:
            checkbox.click()
            time.sleep(uniform(1, 2))

        _submit_form(driver)

        print("Viewing request sent successfully!")
        return True
    except Exception as exc:
        print(f"Failed to request viewing: {exc}")
        return False
    finally:
        driver.quit()
