import logging


def print_msg(msg: str, logger: logging.Logger, log_lvl: int):
    logger.log(log_lvl, f'''------------------------------------------
{msg}
------------------------------------------'''
    )


def custom_exception_info_msg(product_id: int, error_code: str) -> str:
    msg = f'{product_id}. '
    if error_code == 'no-html':
        msg += 'Mala respuesta del servidor, revisar URL'
    elif error_code == 'incorrect-html':
        msg += 'HTML page is not correct'
    elif error_code == 'no-secondary-price':
        msg += 'No secondary price found'
    elif error_code == 'no-units-in-description':
        msg += 'No units appear in the description'
    else:
        msg += 'EXCEPTION IS NOT CONTEMPLATED, REVIEW CODE'
    return msg
