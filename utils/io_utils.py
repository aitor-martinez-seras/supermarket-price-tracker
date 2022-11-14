from pandas import read_excel
import random
import requests
from constants import *
from bs4 import BeautifulSoup
import re

#########################################################

# This file contains the code to handle the operations
# of loading and creating excel files, together with
# retrieving information from the internet

#########################################################


def scrape_html_of_url(product_url: str):
    """
    Retrieves the hmtl of the URL
    :param product_url: string with the URL
    :return: html parsed
    """
    page = requests.get(
        product_url,
        headers={'User-Agent': random.choice(USER_AGENTS)})
    soup = BeautifulSoup(page.text, 'html.parser')
    return soup


def load_excel():
    return read_excel(URLS_EXCEL, )


# TODO: Code from below is the class implementation version
'''
from time import perf_counter
from multiprocessing import Pool


class Supermarket():

    def __init__(self, urls):
        self.urls = urls

    @staticmethod
    def obtain_html(url):
        page = requests.get(
            url,
            headers={'User-Agent': random.choice(USER_AGENTS)})
        soup = BeautifulSoup(page.text, 'html.parser')
        return soup

    # To be overridden by the child
    def price_retriever(self, html):
        pass

    def retrieve_one_price(self, url):
        # Performance analysis
        t1 = perf_counter()
        # Product name must be a string. If it is float it means it is Nan, so skip to next iteration
        if isinstance(url, str):
            price = self.price_retriever(self.obtain_html(url))
        else:
            price = 0
        t2 = perf_counter()
        print(f'El precio es: {price} euros.\t Ha tardado {t2 - t1:.5f}')

    def retrieve_all_prices(self):
        print('Creating the pool and running it')
        with Pool() as pool:
            print(f'Recogiendo datos de: {self.__class__}')
            prices = pool.map(self.retrieve_one_price, self.urls)
        return prices


class Eroski(Supermarket):

    def __init__(self, urls):
        super(Eroski, self).__init__(urls)

    def price_retriever(self, html_page: BeautifulSoup) -> float:
        """
        Parses the html of Eroski supermarket and retrieves the price
        :param html_page: BeautifulSoup html object
        """
        # Locate the tag with the price and extract the whole text
        price = html_page.find(attrs={"class": "price-now"}).find(attrs={"itemprop": "price"}).text
        # Use the package regex (re) to find numbers separated by a comma.
        # Then replace the comma for a dot and turn it to a float
        # TODO: We have to handle the exception that the product shows as "No disponible", what causes that the price
        #  is not available
        try:
            price = float(re.findall(r"\d+\,\d+", price)[0].replace(',', '.'))
        except IndexError as e:
            prince = None
        return price


class BM(Supermarket):

    def __init__(self, urls):
        super(BM, self).__init__(urls)

    def price_retriever(self):
        pass

'''