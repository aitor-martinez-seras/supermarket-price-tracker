from typing import Tuple, List


def return_prices_and_log_msgs(prs_and_msgs: List[Tuple[float, str, int]], logger, supermarket: str) -> List:
    prices = []
    for price, msg, log_lvl in prs_and_msgs:
        prices.append(price)
        logger.log(log_lvl, supermarket + ': ' + msg)
    return prices
