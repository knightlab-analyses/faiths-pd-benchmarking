from unifrac import stacked_faith
import time
import sys

print('Running-stacked_faith')
args = sys.argv
t0 = time.time()
obs = stacked_faith(args[1], args[2])
obs.to_csv('/home/garmstro/faith_pd/large-data/redbiom-fetch/redbiom-fetch-faith-pd.txt')
t1 = time.time()
print('Python time-{}'.format(t1-t0))
