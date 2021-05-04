from unifrac import faith_pd
import time
import sys

print('Running-stacked_faith')
args = sys.argv
t0 = time.time()
obs = faith_pd(args[1], args[2])
t1 = time.time()
print('Python time-{}'.format(t1-t0))
