from skbio import TreeNode
from skbio.diversity import alpha_diversity
from biom import load_table
import numpy as np
import time
import sys

print('Running-faith_pd')
args = sys.argv
table = load_table(args[1])
otu_ids = table.ids('observation')
counts = np.asarray([table.data(i) for i in table.ids()])
tree = TreeNode.read(args[2])

t0 = time.time()
actual = alpha_diversity('faith_pd', counts, tree=tree, otu_ids=otu_ids)
t1 = time.time()
print('Python time-{}'.format(t1-t0))
