import re
from time import time
from pathlib import Path
from copy import deepcopy
from functools import wraps
from typing import TypeVar, Dict, FrozenSet, Optional, List, Set, Any
from collections import defaultdict
from zipfile import ZipFile
import pandas as pd
from config import KAG_LIMIT

# Define some type.
TID = TypeVar(int)
Item = TypeVar(int)
ItemSet = TypeVar(Set[Item])
ItemSets = TypeVar(List[ItemSet])


def timing(f):
    @wraps(f)
    def wrap(*args, **kw):
        ts = time()
        result = f(*args, **kw)
        te = time()
        step = ''
        if f.__name__ == 'apriori':
            step = f'set_size: {args[2]-1}'
        print(f'[{f.__name__}] ({step}) took: {te-ts:2.4f} sec')
        return result
    return wrap


def write_file(file_name: str, data: Any, header: Optional[str]):
    with open(file_name, 'w') as fout:
        if header:
            fout.write(header)
        fout.write('\n'.join(data))
    print(f"file: '{file_name}' writen.")


def get_data(path: Path):
    if path.parent.name == 'ibm':
        return get_ibm_data(path)
    else:
        return get_kag_data(path)


@timing
def get_kag_data(path: Path):
    r"""Get data.

    PARAMS
    =========
    path: Path
        The path to data file.

    Returns
    =======
    ori_itemsets: ItemSets
        The original itemsets.
    transactions: List[ItemSet]
        The transactions.
    item_counter: Dict[ItemSet, int]
        Mapping of itemset to it's occur times.
    """
    # Data read in.
    zip_file = ZipFile(path)
    file = str(path.name).split(path.suffix)[0]
    orders = pd.read_csv(zip_file.open(file), nrows=KAG_LIMIT)

    # check status
    print(f'extracted sales: {orders.shape[0]}')
    print(f'unique orders count: {len(orders.order_id.unique())}')
    print(f'unique products count: {len(orders.product_id.unique())}')

    # Dropout 'add_to_cart_order' and 'reordered' columns.
    orders = orders.drop(
        columns=['add_to_cart_order', 'reordered'], errors='ignore')

    # Extract data.
    t_dict: Dict[TID, ItemSets] = defaultdict(list)
    ori_itemsets: ItemSets = set()
    item_counter: Dict[ItemSet, int] = dict()

    for tid, item in zip(orders.order_id.to_list(), orders.product_id.to_list()):
        t_dict[tid].append(item)
        ori_itemsets.add(item)
        item_counter[item] = item_counter.get(item, 0) + 1

    return ori_itemsets, t_dict.values(), item_counter


def get_ibm_data(path: Path):
    r"""Get data.

    PARAMS
    =========
    path: Path
        The path to data file.

    Returns
    =======
    ori_itemsets: ItemSets
        The original itemsets.
    transactions: List[ItemSet]
        The transactions.
    item_counter: Dict[ItemSet, int]
        Mapping of itemset to it's occur times.
    """
    ori_itemsets: ItemSets = set()
    t_dict: Dict[TID, ItemSets] = defaultdict(list)
    item_counter: Dict[ItemSet, int] = dict()

    # Formated data.
    for line in open(path):
        _, _, tid, item, _ = re.split('[ \t\n]+', line)
        t_dict[tid].append(item)
        item_counter[item] = item_counter.get(item, 0) + 1
        item = frozenset({item})
        ori_itemsets.add(item)
    return ori_itemsets, t_dict.values(), item_counter
