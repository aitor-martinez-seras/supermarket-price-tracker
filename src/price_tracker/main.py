import sys
from time import perf_counter
from datetime import datetime
from multiprocessing import Pool
import argparse
import logging
from logging.handlers import SMTPHandler
from pathlib import Path

import pandas as pd
import numpy as np

from constants import URLS_EXCEL_PATH, UNITS, MONTHS, OUTPUTS_PATH, LOGS_PATH
from utils import EROSKI_RET, BM_RET
from utils.io_utils import scrape_html_of_url, load_excel, write_dataframe_to_excel
from utils.prints import print_msg, custom_exception_info_msg
from smtp import send_logs_via_email


# TODO: Tengo que implementar que se vaya acumulando en un logger el status de cada consulta, si es OK o no
def retrieve_one_product(args) -> float:
    # Performance analysis
    t1 = perf_counter()

    # Extract the URL and the retriever, that is the .get method of the Retriever class
    product_id, product_unit, product_url, (retriever, has_js) = args

    # In case the price is not found, it should be 0.
    price = 0

    # Product name must be a string. If it is float it means it is NaN, so skip to next iteration
    if isinstance(product_url, str):
        try:
            units = UNITS[product_unit]
            price = retriever(units, scrape_html_of_url(product_url, has_js))
            t2 = perf_counter()
            logger.info(f'{product_id}. El precio es: {price} euros.\t Ha tardado {t2 - t1:.5f}')
        except AssertionError as e:
            print_msg(custom_exception_info_msg(product_id, e.args[0]), logger=logger, log_lvl=30)

    else:
        print_msg(f'{product_id}. URL del producto no es un string valido', logger=logger, log_lvl=30)

    return price


# TODO: Implementar logging para poder debuggear cuando este corriendo en RPi
def main():
    # --------------------
    # Retrieve prices
    # --------------------
    logger.info('Inicio de programa')
    logger.warning('Ojito')
    logger.error('De error na')
    logger.debug('Debugeando')
    logger.info('Fin')
    return
    df_urls = load_excel(URLS_EXCEL_PATH)

    # Create the dataframe to store prices
    df_prices = df_urls[['ID', 'PRODUCTOS', 'UNIDADES']]

    # TODO: Parece que funciona el multiprocessing tanto en RPi como en Windows, aunque en RPI muestra error raro
    #   el

    print('Comenzar recogida de datos de los supermercados')
    with Pool(4) as pool:

        print('Recogiendo datos de Eroski')
        t1 = perf_counter()
        prices_eroski = pool.map(
            retrieve_one_product,
            zip(df_urls['ID'], df_urls['UNIDADES'], df_urls['URL Eroski'], EROSKI_RET)
        )
        t2 = perf_counter()
        print(f'Tiempo en eroski: {(t2 - t1)/60:.2f} minutos')

        print('Recogiendo datos de BM')
        prices_bm = pool.map(
            retrieve_one_product,
            zip(df_urls['ID'], df_urls['UNIDADES'], df_urls['URL BM'], BM_RET),
            chunksize=4
        )
        t3 = perf_counter()
        print(f'Tiempo en BM: {(t3 - t2)/60:.2f} minutos')

        # print('Recogiendo datos de Mercadona')
        # prices_mercadona = pool.map(retrieve_one_price_bm, df_urls['URL BM'])
        # t4 = perf_counter()
        # print(f'Tiempo en Mercadona: {t4 - t3}')

        # print('Recogiendo datos de ALDI')
        # prices_aldi = pool.map(retrieve_one_price_bm, df_urls['URL BM'])
        # print(f'Tiempo en ALDI: {perf_counter() - t4}')

    print(f'Tiempo total en recuperar los precios de todos los supermercados: {(perf_counter() - t1)/60:.2f} minutos')

    prices_eroski = np.asarray(prices_eroski, dtype='float')
    prices_bm = np.asarray(prices_bm, dtype='float')

    # TODO: Add functionality to repeat the products where a 0 was the price, in case now it retrieves it.
    #   implement a for loop over the values where prices == 0 (np.where(prices==0))...

    # Add the different colums to the dataframe
    df_prices['Eroski'] = pd.Series(prices_eroski, dtype='float')
    df_prices['BM'] = pd.Series(prices_bm, dtype='float')

    # ----------------------
    # Save csv and excel
    # ----------------------
    month_number = str(today_datetime.month).zfill(2)
    month_name = MONTHS[month_number]

    # Save csv
    csv_path = OUTPUTS_PATH / f'{today}_precios.csv'
    df_prices.to_csv(csv_path, index=False)

    # Save excel
    excel_path = OUTPUTS_PATH / f'{month_number}_listado_precios_{month_name}.xlsx'
    if excel_path.is_file():
        try:
            # It is crucial that the mode is 'a' (append), otherwise it overwrites whole document
            with pd.ExcelWriter(excel_path, mode="a", engine='openpyxl') as writer:
                write_dataframe_to_excel(df=df_prices, writer=writer, sheet_name=today)
        except ValueError as e:
            print(f'Not saving into the {excel_path} the sheet {today} as this error ocurred: {e}')
    else:
        df_prices.to_excel(excel_path, sheet_name=today, index=False)
    print("Programa finalizado con exito!")

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
    t_start_program = perf_counter()
    # parser = argparse.ArgumentParser(description='Supermarket-price-tracker main script')
    # args = parser.parse_args()
    # --------------------
    # Define loggers
    # --------------------
    # SMTP_CFG = load_smtp_settings(SMTP_CFG_PATH)
    logger = logging.getLogger('price_tracker')
    logger.setLevel(logging.DEBUG)  # Set minimum level to enable the handlers

    today_datetime = datetime.now().date()
    today = today_datetime.isoformat().replace("-", "_")

    # Create Handlers
    file_handler_info = logging.FileHandler(LOGS_PATH / f'{today}_info.log', mode='w')
    file_handler_debug = logging.FileHandler(LOGS_PATH / f'{today}_debug.log', mode='w')
    stream_handler = logging.StreamHandler(sys.stdout)
    # smtp_handler = SMTPHandler(
    #     mailhost=(SMTP_CFG['smtp_server'], int(SMTP_CFG['port'])),
    #     fromaddr=SMTP_CFG['sender_email'],
    #     toaddrs=[SMTP_CFG['receiver_email']],
    #     subject=f'Informe dia {today}',
    #     credentials=(SMTP_CFG['sender_email'], SMTP_CFG['password']),
    #     secure=()
    # )

    # Set handler levels
    file_handler_info.setLevel(logging.INFO)
    file_handler_debug.setLevel(logging.DEBUG)
    stream_handler.setLevel(logging.DEBUG)
    # smtp_handler.setLevel(logging.INFO)

    # Create the formatter and assign to the handlers
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler_info.setFormatter(formatter)
    file_handler_debug.setFormatter(formatter)
    stream_handler.setFormatter(formatter)
    # smtp_handler.setFormatter(formatter)

    # Add Handlers to logger
    logger.addHandler(file_handler_info)
    logger.addHandler(file_handler_debug)
    logger.addHandler(stream_handler)
    # logger.addHandler(smtp_handler)

    # Run main
    main()
    send_logs_via_email(today, LOGS_PATH / f'{today}_debug.log')
    print(f'Tiempo transcurrido: {(perf_counter() - t_start_program)/60:.2f} minutos')
