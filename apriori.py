from __future__ import annotations
import re
from time import time
from dataclasses import dataclass, field
from itertools import combinations
from collections import Counter
from typing import TypeVar, Dict, FrozenSet, Optional
from copy import deepcopy
from config import DATA, MIN_SUP

# Define some type.
Item = TypeVar(int)
ItemList = TypeVar(list)
TID = TypeVar(int)
t_dict: Dict[TID, ItemList] = dict()
original_iset: Set[Item] = set()


# Formated data.
for line in open(DATA.test):
    _, _, tid, item, _ = re.split('[ \t\n]+', line)
    if tid in t_dict:
        t_dict[tid].add(item)
    else:
        t_dict[tid] = set(item)
    original_iset.add(frozenset({item}))
transactions = t_dict.values()

def count(itemset: FrozenSet[Item], transactions: List[FrozenSet[Item]]):
    count = 0
    for transaction in transactions:
        if itemset.issubset(transaction): count += 1
    return count

def Counter(itemsets: FrozenSet[Item], transactions: List[FrozenSet[Item]]):
    r"""Count how many times the itemset occur in any transactions."""
    return {itemset: count(itemset, transactions) for itemset in itemsets}


def apriori(itemsets: Set[Item],  transactions: List[Set[Item]], k: int):
    r"""Apriori Algorithm.

    Returns
    =======
    L_1: filter
        The itemset occur in transctions times mapping.
    I_2: map
        The combinations of next itemsets.
    """
    # Count itemset occur in all transaction times.
    C = Counter(itemsets, transactions)                         # (Itemset, count)
    # Filter out less than MIN_SUP.
    L = filter(lambda x: x[1] >= MIN_SUP, C.items())            # (Itemset, count)

    try:
        L_union = frozenset(frozenset.union(*dict(deepcopy(L)).keys()))
    except TypeError as e:
        L_union = set()
    # Generate combinations in forzenset type.
    I = map(frozenset, combinations(L_union, k))                # Itemsets
    return L, I

def support(itemset: FrozenSet, transactions):
    if not isinstance(itemset, FrozenSet): itemset = frozenset(itemset)
    return count(itemset, transactions) / len(transactions)

def confidence(x, y, transactions):
    return support(x | y, transactions) / support(x, transactions)

def lift(x, y, transactions):
    return confidence(x, y, transactions) / support(y, transactions)

def main():
    print(f"MIN_SUP: {MIN_SUP} {'='*100}")
    for k in range(2, 1000):
        start = time()
        I = original_iset if k == 2 else I
        L, I = apriori(I, transactions, k)
        # print(f"[{k-1}]: {dict(deepcopy(L))}")
        print(f"|{k}| {len(list(deepcopy(L)))} | {time() - start: 6f} |")
        if 0 == len(list(L)) <= 1:
            break
main()
