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

    def get(self, html: BeautifulSoup) -> float:
        for k in self.keys:
            html = html.find(attrs={k[0]: k[1]})
        return self.check_float(html.text)

    def check_float(self, price):
        try:
            return float(re.findall(r"\d+\,\d+", price)[0].replace(',', '.'))
        except IndexError as e:
            return None

    def __iter__(self):
        return self

    # When iterating in the Pool, we want the method get in each iteration
    def __next__(self):
        return self.get, self.has_js


if __name__ == '__main__':
    pass
