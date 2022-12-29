from .io_utils import *
from .parsers import *
from .retriever import *


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

#EROSKI_RET = Retriever([('itemprop', 'price'), ('class', 'price-product')], has_js=False)
BM_RET = Retriever(
    {
        "description": [('class', 'u-title-3 d-inline')],
        "price": [('id', 'infoproduct-content--unitprice')],
        "price-secondary": [('id', 'infoproduct-content--price')]
    },
    has_js=True
)
# ALDI_RET  =
# MERCADONA =
ALL_RETS = {'Eroski': EROSKI_RET,
            'BM': BM_RET,
            # 'mercadona': MERCADONA,
            # 'aldi': ALDI_RET
}
