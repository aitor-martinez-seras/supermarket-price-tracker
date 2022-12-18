import pandas as pd
import numpy as np
from utils import scrape_html_of_url, load_excel, EROSKI_RET, BM_RET
from constants import URLS_EXCEL
from time import perf_counter
from datetime import datetime
from multiprocessing import Pool


# TODO: En un futuro igual quiero coger mas info de una consulta, la manera de implementar será que el metodo get
#  del Retriever devuelto en los argumentos devuelva mas datos aparte del precio
def retrieve_one_price(args) -> float:
    # Performance analysis
    t1 = perf_counter()

    # Exrtract the URL and the retriever, that is the .get method of the Retriever class
    product_url, (retriever, has_js) = args

    # Product name must be a string. If it is float it means it is Nan, so skip to next iteration
    if isinstance(product_url, str):
        price = retriever(scrape_html_of_url(product_url, has_js))
    else:
        price = 0
    t2 = perf_counter()
    print(f'El precio es: {price} euros.\t Ha tardado {t2 - t1:.5f}')
    return price


# TODO: Implementar logging para poder debuggear cuando este corriendo en RPi
def main():
    df_urls = load_excel(URLS_EXCEL)

    # Create the dataframe to store prices
    df_prices = df_urls[['ID', 'PRODUCTOS ']]

    print('Comenzar recogida de datos de los supermercados')
    with Pool(4) as pool:

        print('Recogiendo datos de Eroski')
        t1 = perf_counter()
        #prices_eroski = pool.map(retrieve_one_price, zip(df_urls['URL Eroski'], EROSKI_RET))
        t2 = perf_counter()
        print(f'Tiempo en eroski: {t2 - t1}')

        print('Recogiendo datos de BM')
        prices_bm = pool.map(retrieve_one_price, zip(df_urls['URL BM'], BM_RET), chunksize=4)
        t3 = perf_counter()
        print(f'Tiempo en BM: {t3 - t2}')

        # print('Recogiendo datos de Mercadona')
        # prices_mercadona = pool.map(retrieve_one_price_bm, df_urls['URL BM'])
        # t4 = perf_counter()
        # print(f'Tiempo en Mercadona: {t4 - t3}')

        # print('Recogiendo datos de ALDI')
        # prices_aldi = pool.map(retrieve_one_price_bm, df_urls['URL BM'])
        # print(f'Tiempo en ALDI: {perf_counter() - t4}')

    print('Tiempo en recuperar precios', perf_counter() - t1)

    #prices_eroski = np.asarray(prices_eroski, dtype=np.float16)
    prices_bm = np.asarray(prices_bm, dtype=np.float16)

    # TODO: Add functionality to repeat the products where a 0 was the price, in case now it retrieves it.
    #   implement a for loop over the values where prices == 0 (np.where(prices==0))...

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

