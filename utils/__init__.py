from .io_utils import *
from .parsers import *
from .retriever import *


EROSKI_RET = Retriever([('class','price-now'),('itemprop','price')])
MERCADONA = Retriever([('class','price-now'),('itemprop','price')])  #TODO: Check mercadona's keys
ALL_RETS = {'eroski': EROSKI_RET, 'mercadona': MERCADONA}
