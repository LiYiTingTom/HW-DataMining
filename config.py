from pathlib import Path
from dataclasses import dataclass


@dataclass
class DATA:
    ibm_test: Path = Path('./data/ibm/ibm-5000.txt')
    ibm_test_sm: Path = Path('./data/ibm/ibm-sm.txt')
    ibm_test_xs: Path = Path('./data/ibm/ibm-xs.txt')
    kag_order_products__prior: Path = Path(
        './data/market_sells_orders/order_products__prior.csv.zip')
    # order: Path = Path('data/market_sells_orders/input/orders.csv.zip')
    # aisles: Path = Path('data/market_sells_orders/input/aisles.csv.zip')
    # departments: Path = Path('data/market_sells_orders/input/departments.csv.zip')
    # products: Path = Path('data/market_sells_orders/input/products.csv.zip')


@dataclass
class PARAMS:
    min_sup:  float = .4
    min_conf: float = .4
    min_freq: int = 3


WRITE_FILE = True
DISPLAY = True
DATASET = DATA.ibm_test
KAG_LIMIT = 1000
