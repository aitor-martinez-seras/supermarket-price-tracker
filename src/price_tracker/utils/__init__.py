from .io_utils import *
from .retriever import Retriever


# TODO: Uncomment retrievers when we get the URLs
# EROSKI_RET = Retriever([('class', 'price-now'), ('itemprop', 'price')], has_js=False)
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
