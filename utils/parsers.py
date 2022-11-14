from bs4 import BeautifulSoup
import re


# TODO: Upgrade parsers to return different things as product descriptions, to fill the
#  excel file containing the price with more data about the product
def parse_eroski_price(html_page: BeautifulSoup) -> float:
    """
    Parses the html of Eroski supermarket and retrieves the price
    :param html_page: BeautifulSoup html object
    """
    # Locate the tag with the price and extract the whole text
    price = html_page.find(attrs={"class": "price-now"}).find(attrs={"itemprop": "price"}).text
    # Use the package regex (re) to find numbers separated by a comma. Then replace the comma for a dot and turn it to
    # a float
    # TODO: We have to handle the exception that the product shows as "No disponible", what causes that the price
    #  is not available
    try:
        price = float(re.findall(r"\d+\,\d+", price)[0].replace(',', '.'))
    except IndexError as e:
        prince = None
    return price


def parse_bm_price(html_page):
    """
    Parses the html of BM supermarket and retrieves the price
    :param html_page: BeautifulSoup html object
    :return:
    """
    # Locate the tag with the price and extract the whole text
    price = html_page.find()
    # Use the package regex (re) to find numbers separated by a comma. Then replace the comma for a dot and turn it to
    # a float
    # TODO: if this last line is going to be repeated, turn it to a function
    price = float(re.findall(r"\d+\,\d+", price)[0].replace(',', '.'))
    print(f"El precio del producto es: {price} euros")
    return price
