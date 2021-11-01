from time import time
from pathlib import Path
from copy import deepcopy
from functools import wraps
from itertools import combinations
from typing import TypeVar, Dict, FrozenSet, Optional, List, Set, Any
from collections import defaultdict
from zipfile import ZipFile
import pandas as pd
from config import KAG_LIMIT, OUTPUT_DIR

# Define some type.
TID = TypeVar(int)
Item = TypeVar(int)
ItemSet = TypeVar(Set[Item])
ItemSets = TypeVar(List[ItemSet])


def timing(f):
    def wrap(*args, **kwargs):
        ts = time()
        result = f(*args, **kwargs)
        te = time()
        print(f'[{f.__name__}] took: {te-ts:2.4f} sec')
        return result
    return wrap


def write_file(file_name: str, data: Any, header: Optional[str]):
    if not OUTPUT_DIR.exists():
        OUTPUT_DIR.mkdir()
    file_name = OUTPUT_DIR / Path(file_name)

    with open(file_name, 'w') as fout:
        if header:
            fout.write(header)
        fout.write('\n'.join(data))
    print(f"file: '{file_name.absolute()}' writen.")


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

    for tid, item in zip(orders.order_id.to_list(), orders.product_id.to_list()):
        t_dict[tid].append(item)
        item = frozenset({item})
        ori_itemsets.add(item)

    return ori_itemsets, t_dict.values()


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
    """
    ori_itemsets: ItemSets = set()
    t_dict: Dict[TID, ItemSets] = defaultdict(list)

    # Formated data.
    for line in open(path):
        _, tid, item = line.split()
        t_dict[tid].append(item)
        item = frozenset({item})
        ori_itemsets.add(item)

    return ori_itemsets, t_dict.values()


def rules_from_item(itemset: ItemSet):
    r"""Generate associations.

    PARAMS
    =========
    itemset: ItemSet
        The target itemset.

    Return
    ======
    List[Tuple[ItemSet]]
        The associations.
    """
    left = list()
    for i in range(1, len(itemset)):
        left.extend(combinations(itemset, i))
    return [(frozenset(l), frozenset(itemset.difference(l))) for l in left]


def get_association_rules(itemsets: ItemSets, min_conf: float, min_sup: float):
    r"""Get all association rules for itemsets.

    PARAMSs
    ==========
    itemsets: ItemSets
        The traget itemsets.
    min_conf: float
        The minimum confidence threshole.

    Return
    ======
    rules: List
        All the association rules.
    """
    rules = list()

    for itemset in itemsets:
        if len(itemset) > 1:
            rules.extend(rules_from_item(itemset))

    result = list()
    for left, right in rules:
        sup = itemsets[left | right]
        conf = sup / itemsets[left]
        lift = conf / itemsets[right]
        if conf >= min_conf and sup >= min_sup:
            result.append(
                f"\"{str(set(left))}' -> '{str(set(right))}\", {sup:.6f}, {conf:.6f}, {lift:.6f}")
    return result


def compute_supports(itemsets: ItemSets, transactions: List[ItemSet]):
    r"""Compute the itemset's support value in transactions.

    PARAMSs
    ==========
    itemsets: ItemSets
        The target itemsets.
    transactions: List[ItemSet]
        The transaction lists.

    Return
    ======
    Dict[ItemSet, float]
        A dict of itemsets map to there support value.
    """
    def support(itemset: FrozenSet[Item], transactions: List[FrozenSet[Item]]):
        r"""Compute the target itemset's support value.

        PARAMSs
        ==========
        itemset: ItemSet
            The target itemset.
        transactions: List[ItemSet]
            The transaction lists.

        Return
        ======
        float
            The support value.
        """
        count = 0
        for transaction in transactions:
            if set(itemset).issubset(transaction):
                count += 1
        return count / len(transactions)

    t_size = len(transactions)
    return {itemset: support(itemset, transactions) for itemset in itemsets}
