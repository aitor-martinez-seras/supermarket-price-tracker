from datetime import datetime
import argparse

import pandas as pd

from constants import MONTHS, OUTPUTS_PATH
from utils.io_utils import write_dataframe_to_excel


def main(args):

    print('Loading data from csv to xlsx')

    # Load csv
    if args.day_from == 'today':
        today_datetime = datetime.now().date()
        day_from = today_datetime.isoformat().replace("-", "_")
    else:
        raise NotImplementedError('Still in development')
    csv_path = OUTPUTS_PATH / f'{day_from}_precios.csv'
    df_prices = pd.read_csv(csv_path)



    # Save excel
    if args.day_to == 'today':
        day_to = day_from
        month_number = str(today_datetime.month).zfill(2)

    else:
        raise NotImplementedError('Still in development')

    month_name = MONTHS[month_number]
    excel_path = OUTPUTS_PATH / f'{month_number}_listado_precios_{month_name}.xlsx'
    if excel_path.is_file():
        try:
            with pd.ExcelWriter(excel_path, mode='a', engine='openpyxl') as writer:
                write_dataframe_to_excel(df=df_prices, writer=writer, sheet_name=day_to)
                print('Info saved to a new sheet!')
        except ValueError as e:
            print(f'Not saving into the {excel_path} the sheet {day_to} as this error ocurred: {e}')
    else:
        df_prices.to_excel(excel_path, sheet_name=day_to, index=False)
        print('New workbook created and saved the a sheet into it')

    print('Finished!')


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Take the .csv file's info to .xslx", add_help=True)
    parser.add_argument("--day-from", default='today', dest='day_from', type=str)
    parser.add_argument("--day-to", default='today', dest='day_to', type=str)
    args = parser.parse_args()
    main(args)
