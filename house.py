"""Data class representing a single apartment listing from Pararius."""


class House:
    """Stores details about a rental listing scraped from Pararius.

    Attributes:
        title: The listing title (e.g. "Apartment for rent").
        location: Neighborhood or street name.
        price: Monthly rent as displayed on the page.
        surface_area: Living area in square meters.
        link: Full URL to the listing on pararius.com.
    """

    def __init__(self, title, location, price, surface_area, link):
        self.title = title
        self.location = location
        self.price = price
        self.surface_area = surface_area
        self.link = link

    def to_list(self):
        """Return listing data as a list matching the DataFrame column order."""
        return [self.title, self.location, self.price, self.surface_area, self.link, False]

    def __repr__(self):
        return f"House('{self.title}', '{self.location}', '{self.price}')"
