import random
import time
import platform

import pandas as pd
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

from price_tracker.constants import USER_AGENTS

#########################################################

# This file contains the code to handle the operations
# of loading and creating excel files, together with
# retrieving information from the internet

#########################################################


def scrape_html_of_url(product_url: str, has_js: bool):
    if has_js:
        # Define options and service for selenium
        options = Options()
        options.headless = True
        if platform.system() == 'Linux':
            service = Service(executable_path="/usr/bin/chromedriver")
        options.add_argument("--enable-javascript")
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')

        # Initializing webdriver for Chrome with our options
        driver = webdriver.Chrome(service=service, options=options)
        driver.get(product_url)
        time.sleep(10)  # To enable the correct loading of the page

        html_content = driver.page_source
        driver.close()

        # else:
        #     page = requests.get(
        #         product_url,
        #         headers={'User-Agent': random.choice(USER_AGENTS)})
        #     if page.status_code != 200:
        #         print(f'Bad response {page.status_code}', end='\t')
        #         raise AssertionError('no-html')
        #     time.sleep(3)
        #     page = page.text

    else:
        page = requests.get(
            product_url,
            headers={'User-Agent': random.choice(USER_AGENTS)}
        )
        if page.status_code != 200:
            print(f'Bad response {page.status_code}', end='\t')
            raise AssertionError('no-html')
        time.sleep(5)  # To enable the correct loading of the page
        html_content = page.text

    soup = BeautifulSoup(html_content, 'html.parser')
    return soup


def load_excel(xlxs_path):
    return pd.read_excel(xlxs_path)


def write_dataframe_to_excel(df: pd.DataFrame, writer: pd.ExcelWriter, sheet_name: str):
    df.to_excel(writer, sheet_name=sheet_name, index=False, float_format="%.2f")


if __name__ == '__main__':
    from src.price_tracker.utils import EROSKI_RET, BM_RET
    df_urls = load_excel(r"C:\Users\110414\PycharmProjects\Seguidor-de-precios\Lista_de_productos.xlsx.xlsx")
    df_prices = df_urls[['ID', 'PRODUCTOS ']]
    from src.price_tracker.main import retrieve_one_product
    get_mth, has_js = EROSKI_RET.get, EROSKI_RET.has_js
    retrieve_one_product((df_urls['URL Eroski'][80], (get_mth, has_js)))
    get_mth, has_js = BM_RET.get, BM_RET.has_js
    retrieve_one_product((df_urls['URL BM'][0], (get_mth, has_js)))
