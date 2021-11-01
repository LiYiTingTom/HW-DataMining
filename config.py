from pathlib import Path
from dataclasses import dataclass


@dataclass
class DATA:
    ibm: Path = Path('./data/ibm/ibm-5000.txt')
    ibm_test_xs: Path = Path('./data/ibm/ibm-xs.txt')
    ibm_2021: Path = Path('./data/ibm/ibm-2021.txt')
    kaggle: Path = Path(
        './data/market_sells_orders/order_products__prior.csv.zip')
    # order: Path = Path('data/market_sells_orders/input/orders.csv.zip')
    # aisles: Path = Path('data/market_sells_orders/input/aisles.csv.zip')
    # departments: Path = Path('data/market_sells_orders/input/departments.csv.zip')
    # products: Path = Path('data/market_sells_orders/input/products.csv.zip')


@dataclass
class PARAMS:
    min_sup:  float = .02
    min_conf: float = .05


DISPLAY: bool = False
WRITE_FILE: bool = False
KAG_LIMIT: int = 10000
OUTPUT_DIR: Path = Path('./outputs/')
