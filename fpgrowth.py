from __future__ import annotations
from typing import TypeVar, List, Dict, FrozenSet, Set, Optional, Union


# Define some type.
itemset = TypeVar(int)
itemsetSet = TypeVar(FrozenSet[itemset])
itemsetSets = TypeVar(List[itemsetSet])


class Tree:
    def __init__(self,
                 tag: Union[str, int],
                 count: Optional[int] = 1,
                 parent: Optional[Tree] = None):
        self.tag = tag
        self.count = count
        self.next_node = None
        self.parent = parent
        self.children = dict()

    def __getitem__(self, key):
        return self.children.get(key, None)

    def __setitem__(self, key, value):
        self.children[key] = value

    def inc(self, count):
        self.count += count


def append_node(first_node, target):
    r"""Append node target into first_node's node list tail."""
    # Get the last node.
    while first_node.next_node:
        first_node = first_node.next_node
    # Insert target into next node.
    first_node.next_node = target


def update_fp_tree(items, parent, header_tab, count):
    r"""Update the FP-Tree."""
    first, other = items[0], items[1:]
    first_node = parent[first]

    # In parent's children dict.
    if first_node:
        first_node.inc(count)
    # First insert first node into children.
    else:
        first_node = parent[first] = Tree(first, count, parent)

        # Update header table for first node.
        if header_tab[first][1]:
            append_node(header_tab[first][1], first_node)
        else:
            header_tab[first][1] = first_node

    # Recurrsively update FP-Tree.
    if len(items) > 1:
        update_fp_tree(other, parent[first], header_tab, count)


def build_fp_tree(transactions, min_sup=1):
    r"""Build the FP-Tree and header table."""
    header_tab = dict()

    # Create header table.
    for trans in transactions:
        for item in trans:
            header_tab[item] = header_tab.get(item, 0) + transactions[trans]

    # Filter out the node, whos count less than min_sup.
    for k in list(header_tab.keys()):
        if header_tab[k] < min_sup:
            del(header_tab[k])

    # Get the freq_itemset from header table.
    freq_itemsets = set(header_tab.keys())

    # Without any freq_itemsets
    if not freq_itemsets:
        return None, None

    # Format the header table [count: count].
    for k in header_tab:
        header_tab[k] = [header_tab[k], None]

    result = Tree('Null', 1, None)

    for trans, count in transactions.items():
        tmp_dict = dict()

        # Filter out node's count value less than min_sup
        for item in trans:
            if item in freq_itemsets:
                tmp_dict[item] = header_tab[item][0]

        if tmp_dict:
            # Sort the tmp_dict by count value.
            ordered = [v[0] for v in sorted(
                tmp_dict.items(), key=lambda p: (p[1], int(p[0])), reverse=True)]

            # Update the FP-Tree.
            update_fp_tree(ordered, result, header_tab, count)

    return result, header_tab


def trace_back(target, prefix_path):
    r"""Tracing back and append the target."""
    if target.parent:
        # Append target.
        prefix_path.append(target.tag)
        trace_back(target.parent, prefix_path)


def get_prefix_paths(bases_ptn, sub_header_tab):
    r"""Get the prefix paths."""
    subtree = sub_header_tab[bases_ptn][1]
    result = dict()

    # Sequencially insert the mapping of next_node to count.
    while subtree:
        prefix_path = list()
        trace_back(subtree, prefix_path)

        # Insert the leaf node's count.
        if len(prefix_path) > 1:
            result[frozenset(prefix_path[1:])] = subtree.count

        # Next node.
        subtree = subtree.next_node
    return result


def mining(parent, header_tab, min_sup, prefix_path, freq_itemsets):
    r"""The mining algorithm."""
    # Sort the base patterns.
    bases_ptns = [v[0]
                  for v in sorted(header_tab.items(), key=lambda p: p[1][0])]

    # Sequencially deal up with the base patterns.
    for base_ptn in bases_ptns:  # 对每个频繁项
        new_itemset = prefix_path.copy()
        new_itemset.add(base_ptn)
        freq_itemsets.append(new_itemset)

        # Get the conditional pattern bases.
        cond_pat_basess = get_prefix_paths(base_ptn, header_tab)

        # Build the subtree.
        cond_tree, sub_header_tab = build_fp_tree(cond_pat_basess, min_sup)

        # Recussive mining.
        if sub_header_tab:
            mining(cond_tree, sub_header_tab, min_sup,
                   new_itemset, freq_itemsets)


def format_trans(transactions: List[itemsetSets]):
    r"""Format the original transactions into **mapping of itemset to count values**."""
    result = dict()
    for trans in transactions:
        trans = frozenset(trans)
        result[trans] = result.get(trans, 0) + 1

    return result
