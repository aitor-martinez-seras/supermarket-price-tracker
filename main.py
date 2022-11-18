import pandas as pd
from utils import scrape_html_of_url, parse_eroski_price, parse_bm_price, load_excel
from time import perf_counter
from datetime import datetime
from multiprocessing import Pool


# TODO: Encapsulate each supermarket in an object -> Es necesario o util??, pensar en futuras funcionalidades.
#  Puede encapsularse muy elegantemente en clases, pero no se porque exactamente da error al usarse.
#  Preguntar a Aritz para ver como manejo el tema de clases y multiprocessing
def retrieve_one_price_eroski(product_url: str or float) -> float:
    # Performance analysis
    t1 = perf_counter()
    # Product name must be a string. If it is float it means it is Nan, so skip to next iteration
    if isinstance(product_url, str):
        price = parse_eroski_price(scrape_html_of_url(product_url))
    else:
        price = 0
    t2 = perf_counter()
    print(f'El precio es: {price} euros.\t Ha tardado {t2-t1:.5f}')
    return price


def retrieve_one_price_bm(product_url: str or float) -> float:
    # Performance analysis
    t1 = perf_counter()
    # Product name must be a string. If it is float it means it is Nan, so skip to next iteration
    if isinstance(product_url, str):
        price = parse_bm_price(scrape_html_of_url(product_url))
    else:
        price = 0
    t2 = perf_counter()
    print(f'El precio es: {price} euros.\t Ha tardado {t2-t1:.5f}')
    return price


# TODO: Implementar logging para poder debuggear cuando este corriendo en RPi

def main():
    df_urls = load_excel()
    dict_list = []

    # Create the dataframe to store prices
    df_prices = df_urls[['ID', 'PRODUCTOS ']]

    # Retrieve URLs
    urls_mercadona = df_urls['URL Mercadona']
    urls_aldi = df_urls['URL ALDI']

    print('Creating the pool and running it')
    with Pool() as pool:
        print('Recogiendo datos de Eroski')
        prices_eroski = pool.map(retrieve_one_price_eroski, df_urls['URL Eroski'])
        print('Recogiendo datos de BM')
        #prices_bm = pool.map(retrieve_one_price_bm, df_urls['URL BM'])
    prices_bm = prices_eroski.copy()
    # Add the different colums to the dataframe
    df_prices['Eroski'] = prices_eroski
    df_prices['BM'] = prices_bm

    # Create the excel
    # TODO: Especificar que la primera columna es la de los indices
    df_prices.to_csv('precios.csv', index=False)
    df_prices.to_excel('precios.xlsx', sheet_name=datetime.now().date().isoformat(), index=False)
    print()

# TODO: Futuras funcionalidades
#   1:  Crear un csv en vez de un excel por cada día
#       1.1: Que cada día se coja el excel con todos los datos y se actualice con los datos del nuevo día,
#       añadiendo simplemente una nueva hoja.
#   2:  Implementar una funcion que coja los .csvs, los lea, y cree un excel gordo con el precio de cada día
#       en una hoja distinta
#   3:  Implementar la posibilidad de un grafico interactivo con matplotlib donde poder visualizar diferentes datos
#       3.1: la evolución de un precio en un periodo concreto de tiempo, pudiendo seleccionar varios a la vez
#   4:  En caso de generar las clases, usando un ORM generar la base de datos.
#       4.1: meter base de datos en el servidor QNAP o en RPi
#   5:  Implementar el grafico interactivo como un servicio web
#   6:  Hacer data mining para averiguar el supermercado mas barato para cada tipo de producto


if __name__ == '__main__':
    t1 = perf_counter()
    main()
    t2 = perf_counter()
    print(f'Tiempo transcurrido: {t2-t1:.3f}')

