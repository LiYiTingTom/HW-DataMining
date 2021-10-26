from pathlib import Path
from dataclasses import dataclass


@dataclass
class DATA:
    ibm_test: Path = Path('./data/ibm/ibm-5000.txt')
    ibm_test_sm: Path = Path('./data/ibm/ibm-sm.txt')
    ibm_test_xs: Path = Path('./data/ibm/ibm-xs.txt')
    kag_order_products__prior: Path = Path('./data/market_sells_orders/order_products__prior.csv.zip')
    # order: Path = Path('data/market_sells_orders/input/orders.csv')
    # aisles: Path = Path('data/market_sells_orders/input/aisles.csv')
    # departments: Path = Path('data/market_sells_orders/input/departments.csv')
    # products: Path = Path('data/market_sells_orders/input/products.csv')

MIN_SUP = .2
MIN_CONF = .5