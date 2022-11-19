import re


class Retriever:
    """
        Class defining how data should be scrapped from plain text html.

        Attributes:
            keys(List[Tuple]): Ordered keys that allow retriving the price
    """
    def __init__(self, keys):
        self.keys = keys

    def get(self, html: str) -> float:
        for k in self.keys:
            html = html.find(attrs={k[0]: k[1]})
        return self.check_float(html.text)

    def check_float(self, price):
        try:
            return float(re.findall(r"\d+\,\d+", price)[0].replace(',', '.'))
        except IndexError as e:
            return None

