import re
from bs4 import BeautifulSoup


class Retriever:
    """
        Class defining how data should be scrapped from plain text html.

        Attributes:
            keys(List[Tuple]): Ordered keys that allow retrieving the price
    """
    def __init__(self, keys, has_js):
        self.keys = keys
        self.has_js = has_js

    def get(self, html: BeautifulSoup or int) -> float:
        # TODO: Better debug this
        # A 0 will arrive in case there has been a bad response from the server (<404> for example)
        if html == 0:
            return 0

        for k in self.keys:
            try:
                html = html.find(attrs={k[0]: k[1]})
            # If the page is received but the content we look for is not available, raising an AttributeError,
            # we raise AssertionError to be catch by the retrieve_one_price() function in main
            except AttributeError:
                raise AssertionError

        # Handle the exception where the render fails to generate the HTML correctly
        try:
            result = self.check_float(html.text)
        except AttributeError:
            result = 0
        return result

    def check_float(self, price):
        try:
            return round(float(re.findall(r"\d+\,\d+", price)[0].replace(',', '.')), 2)
        except IndexError as e:
            return None

    def __iter__(self):
        """
        This defines what is returned when called the iter method. In this case we
        want to return the Retriever object itself, as it contains the info about the
        steps to retrieve the info out of the HTML
        """
        return self

    def __next__(self):
        """
        When next() method is called internally by the pool, this is the method
        that is called
        """
        return self.get, self.has_js


if __name__ == '__main__':
    pass
