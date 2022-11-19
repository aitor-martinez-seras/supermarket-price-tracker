from .io_utils import *
from .parsers import *
from .retriever import *


# TODO: Uncomment retrievers when we get the URLs
EROSKI_RET = Retriever([('class', 'price-now'), ('itemprop', 'price')], has_js=False)
BM_RET = Retriever([('id', 'infoproduct-content--unitprice')], has_js=True)
# ALDI_RET  = Retriever([('class','price-now'),('itemprop','price')])
# MERCADONA = Retriever([('class','price-now'),('itemprop','price')])  #TODO: Check mercadona's keys
ALL_RETS = {'Eroski': EROSKI_RET,
            'BM': BM_RET,
            # 'mercadona': MERCADONA,
            # 'aldi': ALDI_RET
}
