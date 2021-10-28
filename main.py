import fpgrowth
from utils import get_data
from config import DATA

# Get data.
_, transactions, _ = get_data(DATA.ibm_test)

# Format data.
initSet = fpgrowth.format_trans(transactions)

# Build FP-Tree
fp_tree, header_table = fpgrowth.build_fp_tree(initSet, 3)

freqItems = []
fpgrowth.mining(fp_tree, header_table, 3, set([]), freqItems)
for x in freqItems:
    print(x)

# Get data.
_, transactions, _ = get_data(DATA.kag_order_products__prior)

# Format data.
initSet = fpgrowth.format_trans(transactions)

# Build FP-Tree
fp_tree, header_table = fpgrowth.build_fp_tree(initSet, 3)

freqItems = []
fpgrowth.mining(fp_tree, header_table, 3, set([]), freqItems)
for x in freqItems:
    print(x)
