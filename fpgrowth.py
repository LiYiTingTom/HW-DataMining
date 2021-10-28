from typing import TypeVar, List, Dict, FrozenSet, Set, Optional


# Define some type.
Item = TypeVar(int)
ItemSet = TypeVar(FrozenSet[Item])
ItemSets = TypeVar(List[ItemSet])


class Tree:
    def __init__(self, tag, count, parent):
        self.name = tag
        self.count = count
        self.nodeLink = None
        self.parent = parent
        self.children = dict()

    def inc(self, count):
        self.count += count

    def disp(self, ind=1):
        print('  '*ind, self.name, ' ', self.count)
        for child in list(self.children.values()):
            child.disp(ind+1)


def updateHeader(nodeToTest, targetNode):
    while nodeToTest.nodeLink != None:
        nodeToTest = nodeToTest.nodeLink
    nodeToTest.nodeLink = targetNode


def updateFPtree(items, inTree, header_tab, count):
    first, other = items[0], items[1:]
    if first in inTree.children:
        # 判断items的第一个结点是否已作为子结点
        inTree.children[first].inc(count)
    else:
        # 创建新的分支
        inTree.children[first] = Tree(first, count, inTree)
        if header_tab[first][1] == None:
            header_tab[first][1] = inTree.children[first]
        else:
            updateHeader(header_tab[first][1], inTree.children[first])
    # 递归
    if len(items) > 1:
        updateFPtree(other, inTree.children[first], header_tab, count)


def build_fp_tree(dataSet, min_sup=1):
    header_tab = {}
    for trans in dataSet:
        for item in trans:
            header_tab[item] = header_tab.get(item, 0) + dataSet[trans]
    for k in list(header_tab.keys()):
        if header_tab[k] < min_sup:
            del(header_tab[k])  # 删除不满足最小支持度的元素
    freqItemSet = set(header_tab.keys())  # 满足最小支持度的频繁项集
    if len(freqItemSet) == 0:
        return None, None
    for k in header_tab:
        header_tab[k] = [header_tab[k], None]  # element: [count, node]

    retTree = Tree('Null Set', 1, None)
    for tranSet, count in list(dataSet.items()):
        # dataSet：[element, count]
        localD = {}
        for item in tranSet:
            if item in freqItemSet:  # 过滤，只取该样本中满足最小支持度的频繁项
                localD[item] = header_tab[item][0]  # element : count
        if len(localD) > 0:
            # 根据全局频数从大到小对单样本排序
            # orderedItem = [v[0] for v in sorted(localD.iteritems(), key=lambda p:(p[1], -ord(p[0])), reverse=True)]
            orderedItem = [v[0] for v in sorted(
                iter(localD.items()), key=lambda p:(p[1], int(p[0])), reverse=True)]
            # 用过滤且排序后的样本更新树
            updateFPtree(orderedItem, retTree, header_tab, count)
    return retTree, header_tab

# 回溯


def ascendFPtree(leafNode, prefix_path):
    if leafNode.parent != None:
        prefix_path.append(leafNode.name)
        ascendFPtree(leafNode.parent, prefix_path)
# 条件模式基


def get_prefix_path(base_ptn, sub_header_taberTab):
    Tree = sub_header_taberTab[base_ptn][1]  # base_ptn在FP树中的第一个结点
    condPats = {}
    while Tree:
        prefix_path = []
        ascendFPtree(Tree, prefix_path)  # prefix_path是倒过来的，从Tree开始到根
        if len(prefix_path) > 1:
            # 关联Tree的计数
            condPats[frozenset(prefix_path[1:])] = Tree.count
        Tree = Tree.nodeLink  # 下一个base_ptn结点
    return condPats


def mining(inTree, header_tab, min_sup, prefix_path, freq_itemsets):
    # 最开始的频繁项集是header_tab中的各元素
    base_ptns = [v[0] for v in sorted(
        header_tab.items(), key=lambda p: p[1][0])]  # 根据频繁项的总频次排序
    for base_ptn in base_ptns:  # 对每个频繁项
        new_itemset = prefix_path.copy()
        new_itemset.add(base_ptn)
        freq_itemsets.append(new_itemset)
        cond_pat_bases = get_prefix_path(base_ptn, header_tab)  # 当前频繁项集的条件模式基
        cond_tree, sub_header_tab = build_fp_tree(
            cond_pat_bases, min_sup)  # 构造当前频繁项的条件FP树
        if sub_header_tab:
            mining(cond_tree, sub_header_tab, min_sup,
                   new_itemset, freq_itemsets)  # 递归挖掘条件FP树


def format_trans(transactions: List[ItemSets]):
    r"""Format the original transactions into **mapping of itemset to count values**.

    Example
    =======
    >>> trans = [[1, 2, 3], [1, 2, 3], [2, 3]
    >>> Formater(trans)
    {
        frozenset({1, 2, 3}): 2,
        frozenset({2, 3}): 1
    }

    Return
    ======
    counter: Dict[FrozenSet, int]
        The mapping of each itemset to it's count.
    """
    result = dict()
    for trans in transactions:
        trans = frozenset(trans)
        result[trans] = result.get(trans, 0) + 1
    return result


def calSuppData(header_tab, freq_itemsets, total):
    suppData = {}
    for Item in freq_itemsets:
        # 找到最底下的结点
        Item = sorted(Item, key=lambda x: header_tab[x][0])
        base = get_prefix_path(Item[0], header_tab)
        # 计算支持度
        support = 0
        for B in base:
            if frozenset(Item[1:]).issubset(set(B)):
                support += base[B]
        # 对于根的儿子，没有条件模式基
        if len(base) == 0 and len(Item) == 1:
            support = header_tab[Item[0]][0]

        suppData[frozenset(Item)] = support/float(total)
    return suppData


def aprioriGen(Lk, k):
    retList = []
    lenLk = len(Lk)
    for i in range(lenLk):
        for j in range(i+1, lenLk):
            L1 = list(Lk[i])[:k-2]
            L2 = list(Lk[j])[:k-2]
            L1.sort()
            L2.sort()
            if L1 == L2:
                retList.append(Lk[i] | Lk[j])
    return retList


def calcConf(freqSet, H, supportData, br1, minConf=0.7):
    prunedH = []
    for conseq in H:
        conf = supportData[freqSet] / supportData[freqSet - conseq]
        if conf >= minConf:
            print("{0} --> {1} conf:{2}".format(freqSet - conseq, conseq, conf))
            br1.append((freqSet - conseq, conseq, conf))
            prunedH.append(conseq)
    return prunedH


def rulesFromConseq(freqSet, H, supportData, br1, minConf=0.7):
    m = len(H[0])
    if len(freqSet) > m+1:
        Hmp1 = aprioriGen(H, m+1)
        Hmp1 = calcConf(freqSet, Hmp1, supportData, br1, minConf)
        if len(Hmp1) > 1:
            rulesFromConseq(freqSet, Hmp1, supportData, br1, minConf)


def generateRules(freq_itemsets, supportData, minConf=0.7):
    bigRuleList = []
    for freqSet in freq_itemsets:
        H1 = [frozenset([item]) for item in freqSet]
        if len(freqSet) > 1:
            rulesFromConseq(freqSet, H1, supportData, bigRuleList, minConf)
        else:
            calcConf(freqSet, H1, supportData, bigRuleList, minConf)
    return bigRuleList
