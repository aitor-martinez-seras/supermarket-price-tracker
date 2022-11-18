import re
import random
import requests
from time import perf_counter
from constants import *
from bs4 import BeautifulSoup
from abc import ABCMeta, abstractmethod
from pandas import read_excel
import ray


#########################################################

# This file contains the code to handle the operations
# of loading and creating excel files, together with
# retrieving information from the internet

#########################################################


def scrape_html_of_url(product_url: str) -> BeautifulSoup:
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


@ray.remote
class Supermarket():

    def __init__(self, retriever):
        self.retriever = retriever
    
    def retrieve_one_price(self, url):
        price = 0
        
        # Product name must be a string. If it is float it means it is Nan, so skip to next iteration
        if isinstance(url, str):
            headers={'User-Agent': random.choice(USER_AGENTS)}
            html = BeautifulSoup(requests.get(url, headers=headers).text, 'html.parser')
            price = self.retriever.get(html)
        return price
    
    def retrieve_all_prices(self, urls):
        return [self.retrieve_one_price(url) for url in urls]
