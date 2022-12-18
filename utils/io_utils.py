from pandas import read_excel
import random
import requests
from constants import *
from bs4 import BeautifulSoup
import re
from abc import ABCMeta, abstractmethod
from constants import USER_AGENTS
from requests_html import HTMLSession, AsyncHTMLSession
from time import sleep

#########################################################

# This file contains the code to handle the operations
# of loading and creating excel files, together with
# retrieving information from the internet

#########################################################


def scrape_html_of_url(product_url: str, has_js: bool):
    if has_js:
        # TODO: Does not work with multiprocessing. https://github.com/psf/requests-html/issues/155
        #  I think AsyncHTMLSession() could be the solution
        #  https://stackoverflow.com/questions/53696855/multithreading-with-requests-html
        #  https://github.com/psf/requests-html/issues/500
        session = HTMLSession()
        r = session.get(
            product_url,
            #headers={'User-Agent': random.choice(USER_AGENTS)}
        )
        r.html.render(retries=10, wait=5, timeout=60, sleep=1)
        soup = BeautifulSoup(r.html.html, 'html.parser')
    else:
        page = requests.get(
            product_url,
            headers={'User-Agent': random.choice(USER_AGENTS)})
        soup = BeautifulSoup(page.text, 'html.parser')
    return soup


def load_excel(xlxs_path):
    return read_excel(xlxs_path, )



if __name__ == '__main__':
    from utils import scrape_html_of_url, EROSKI_RET, BM_RET
    df_urls = load_excel(r"C:\Users\110414\PycharmProjects\Seguidor-de-precios\LIBRO-BASE-PRODUCTOS_ok.xlsx")
    df_prices = df_urls[['ID', 'PRODUCTOS ']]
    from main import retrieve_one_price
    get_mth, has_js = BM_RET.get, BM_RET.has_js
    retrieve_one_price((df_urls['URL BM'][0], (get_mth, has_js)))
