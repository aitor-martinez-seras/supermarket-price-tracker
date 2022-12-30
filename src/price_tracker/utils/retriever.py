import re
from bs4 import BeautifulSoup
from typing import Tuple, List, Dict


class Retriever:
    """
        Class defining how data should be scrapped from plain text html.

        Attributes:
            keys(Dict[List[Tuple]]): Ordered keys that allow retrieving the price
            has_js(bool): True if the html contains JS that must be rendered
    """
    def __init__(self, keys: Dict[str, List[Tuple[str, str]]], has_js: bool):
        self.keys = keys
        self.has_js = has_js

    def get(self, product_units: Tuple[str], html: BeautifulSoup) -> float:
        # A 0 will arrive in case there has been a bad response from the server (<404> for example)
        if isinstance(html, int):
            return 0

        # Price (a string with the price inside it, but not alone)
        price_str = self.retrieve_text_from_html(html, "price")

        # If unitary price does not exits, we need to check description
        if price_str == '':

            description = self.retrieve_text_from_html(html, "description")
            # If "" is returned it means we cannot find the info we are looking for so
            # we raise AssertionError to be catch by the retrieve_one_price() function in main
            if description == '':
                raise AssertionError("HTML page is not correct")

            else:
                correct_units = self.check_units_in_split_str(product_units, description.split())
                if correct_units:
                    price_str = self.retrieve_text_from_html(html, "price-secondary")
                    if price_str == '':
                        raise AssertionError("No secondary price found")
                else:
                    raise AssertionError("The number of units cannot be retrieved from description")

        else:  # Price exits, check if has searched units
            correct_units = self.check_units_in_split_str(product_units, price_str.split())

            if not correct_units:  # The price is in the units we look for
                # I have to go for secondary price
                price_str = self.retrieve_text_from_html(html, "price-secondary")
                if price_str == '':
                    raise AssertionError("Secondary price not found")

        price = self.retrieve_float(price_str)

        return price

    def retrieve_text_from_html(self, html: BeautifulSoup, key: str) -> str:
        for k in self.keys[key]:
            text = html.find(attrs={k[0]: k[1]})
            # If price is None we will assume that there is no price per unit, but that we are in
            # the correct html
            if text is None:
                return ''
        return text.text

    def check_units_in_split_str(self, prod_units: Tuple[str], split_str: List[str]) -> bool:
        for unit in prod_units:
            for word in split_str:
                if unit.lower() == word.lower():
                    return True
        print('----------')
        for p in prod_units:
            print(p.lower(), end=' / ')
        print()
        for p in split_str:
            print(p.lower(), end=' / ')
        print()
        print('Encountered incompatibilty between units')
        print('----------')
        return False

    def retrieve_float(self, price: str) -> float:
        """
        Retrieves a float number from a string if the float is in the form XX,XX inside the string.
        Only works in Spanish webpages, as numbers are separated by commas and not dots.
        """
        try:
            return round(float(re.findall(r"\d+\,\d+", price)[0].replace(',', '.')), 2)
        except IndexError:
            raise AssertionError('The price float could not be found in the price string')

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
