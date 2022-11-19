from .io_utils import *
from .parsers import *
from .retriever import *


# TODO: Uncomment retrievers when we get the URLs
EROSKI_RET = Retriever([('class','price-now'),('itemprop','price')])
BM_RET = Retriever([('class','price-now'),('itemprop','price')])
# ALDI_RET  = Retriever([('class','price-now'),('itemprop','price')])
# MERCADONA = Retriever([('class','price-now'),('itemprop','price')])  #TODO: Check mercadona's keys
ALL_RETS = {'eroski': EROSKI_RET,
            'bm': BM_RET,
            # 'mercadona': MERCADONA,
            # 'aldi': ALDI_RET
}
