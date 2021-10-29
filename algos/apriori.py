from datetime import datetime
from itertools import combinations
from typing import TypeVar, Dict, FrozenSet, Optional, List, Set
from utils import timing, write_file, get_data


# Define some type.
TID = TypeVar(int)
Item = TypeVar(int)
ItemSet = TypeVar(Set[Item])
ItemSets = TypeVar(List[ItemSet])


def support(itemset: FrozenSet[Item], transactions: List[FrozenSet[Item]]):
    r"""Compute the target itemset's support value.

    Parameters
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


def compute_supports(itemsets: ItemSets, transactions: List[ItemSet]):
    r"""Compute the itemset's support value in transactions.

    Parameters
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
    t_size = len(transactions)
    return {itemset: support(itemset, transactions) for itemset in itemsets}


def apriori(itemsets: Set[Item],  transactions: List[Set[Item]], k: int, min_sup: float):
    r"""Apriori Algorithm.

    Parameters
    ==========
    itemsets: ItemSets
        The target itemsets.
    transactions: List[ItemSet]
        The transaction lists.

    Returns
    =======
    L_1: dict
        The itemset occur in transctions times mapping.
    I_2: map
        The combinations of next itemsets.
    """
    t_size = len(transactions)
    # Count itemset occur in all transaction times.
    C = compute_supports(itemsets, transactions)
    # Filter out less than min_sup.
    L = dict(filter(lambda x: x[1] >= min_sup, C.items()))
    # Union all itemsets.
    if not L:
        return L, None
    L_union = frozenset.union(*L.keys())
    # Generate combinations in forzenset type.
    I = map(frozenset, combinations(L_union, k))
    return L, I


def get_freq_itemsets(ori_itemsets: ItemSet, transactions: List[ItemSet], min_sup: float):
    r"""Get all itemsets.

    Parameters
    ==========
    ori_itemsets: ItemSet
        The original itemset.
    transactions: List[ItemSet]
        The transaction lists.

    Returns
    =======
    result: Dict[ItemSet, float]
        A dict of all itemsets mapping to there support value.
    """
    result = dict()
    for k in range(2, 100):
        I = ori_itemsets if k == 2 else I
        L, I = apriori(I, transactions, k, min_sup)
        result.update(L)
        if 0 <= len(list(L)) <= 1 and I is None:
            return result
    return result


def rules_from_item(itemset: ItemSet):
    r"""Generate associations.

    Parameter
    =========
    itemset: ItemSet
        The target itemset.

    Return
    ======
    List[Tuple[ItemSet]]
        The associations.
    """
    left = []
    for i in range(1, len(itemset)):
        left.extend(combinations(itemset, i))
    return [(frozenset(l), frozenset(itemset.difference(l))) for l in left]


def get_association_rules(itemsets: ItemSets, min_conf: float):
    r"""Get all association rules for itemsets.

    Parameters
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
    rules = []
    for itemset in itemsets:
        if len(itemset) > 1:
            rules.extend(rules_from_item(itemset))

    result = []
    for left, right in rules:
        sup = itemsets[left | right]
        conf = sup / itemsets[left]
        lift = conf / itemsets[right]
        if conf >= min_conf:
            result.append(
                f"\"{str(set(left))}' -> '{str(set(right))}\", {sup:.6f}, {conf:.6f}, {lift:.6f}")
    return result
