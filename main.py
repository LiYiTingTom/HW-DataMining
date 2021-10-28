import fpgrowth
from utils import get_data
from config import DATA

'''simple data'''
_, transactions, _ = get_data(DATA.ibm_test)
initSet = fpgrowth.createInitSet(transactions)
myFPtree, myHeaderTab = fpgrowth.createFPtree(initSet, 3)

freqItems = []
fpgrowth.mineFPtree(myFPtree, myHeaderTab, 3, set([]), freqItems)
for x in freqItems:
    print(x)
