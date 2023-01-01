def print_msg(msg: str):
    print(f'''------------------------------------------
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
        msg += 'EXCEPTION IS NOT COMTEMPLATED, REVIEW CODE '
    return msg
