from .retriever import Retriever
from .common import return_prices_and_log_msgs


EROSKI_RET = Retriever(
    {
        "description": [('itemprop', 'description')],
        "price": [('itemprop', 'price')],
        "price-secondary": [('itemprop', 'price'), ('class', 'offer-now')]
    },
    has_js=False
)
BM_RET = Retriever(
    {
        "description": [('class', 'u-title-3 d-inline')],
        "price": [('id', 'infoproduct-content--unitprice')],
        "price-secondary": [('id', 'infoproduct-content--price')]
    },
    has_js=True
)
# MERCADONA =
