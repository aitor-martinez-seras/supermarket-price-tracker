import re
from bs4 import BeautifulSoup
from typing import Tuple, List
from constants import UNITS

class Retriever:
    """
        Class defining how data should be scrapped from plain text html.

        Attributes:
            keys(Dict[List[Tuple]]): Ordered keys that allow retrieving the price
    """
    def __init__(self, keys, has_js):
        self.keys = keys
        self.has_js = has_js

    def get(self, product_units: Tuple, html: BeautifulSoup or int) -> float:
        # A 0 will arrive in case there has been a bad response from the server (<404> for example)
        if html == 0:
            return 0

        # Price
        price = self.retrieve_text_from_html(html, "price")

        if price == '':  # Unitary price does not exits, we need to check description

            description = self.retrieve_text_from_html(html, "description")
            # If "" is returned it means we cannot find the info we are looking for so
            # we raise AssertionError to be catch by the retrieve_one_price() function in main
            if description == '':
                raise AssertionError("HTML page is not correct")

            else:
                correct_units = self.check_units_in_split_str(product_units, description.split())
                if correct_units:
                    price = self.retrieve_text_from_html(html, "price-secondary")
                    if price == '':
                        raise AssertionError("No secondary price found")
                    price = self.retrieve_float(price)

                else:
                    raise AssertionError("The number of units cannot be retrieved from description")

        else:  # Price exits, check if has searched units
            correct_units = self.check_units_in_split_str(product_units, price.split())

            if correct_units:  # The price is in the units we look for
                price = self.retrieve_float(price)
            else:
                # I have to go for secondary price
                price = self.retrieve_text_from_html(html, "price-secondary")
                if price == '':
                    raise AssertionError("Secondary price not found")

        return price

    def retrieve_text_from_html(self, html: BeautifulSoup, key: str):
        for k in self.keys[key]:
            text = html.find(attrs={k[0]: k[1]})
            # If price is None we will assume that there is no price per unit, but that we are in
            # the correct html
            if text is None:
                return ''
        return text.text

    def check_units_in_split_str(self, prod_units: Tuple[str], split_str: List[str]) -> bool:
        for unit in prod_units:
            for i, word in enumerate(split_str):
                if unit.lower() == word.lower():
                    return split_str[i-1]
        return True

    def retrieve_description_from_html(self, html: BeautifulSoup) -> str:
        for k in self.keys["description"]:
            desc = html.find(attrs={k[0]: k[1]})
            if desc is None:
                return ""
        return desc.text


    def retrieve_float(self, price):
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
