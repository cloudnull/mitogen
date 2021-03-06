"""
Measure latency of IPC between two local threads.
"""

import threading
import time

import mitogen
import mitogen.utils

mitogen.utils.setup_gil()

X = 20000

def flip_flop(ready, inp, out):
    ready.put(None)
    for x in xrange(X):
        inp.get()
        out.put(None)


ready = mitogen.core.Latch()
l1 = mitogen.core.Latch()
l2 = mitogen.core.Latch()

t1 = threading.Thread(target=flip_flop, args=(ready, l1, l2))
t2 = threading.Thread(target=flip_flop, args=(ready, l2, l1))
t1.start()
t2.start()

ready.get()
ready.get()

t0 = time.time()
l1.put(None)
t1.join()
t2.join()
print('++', int(1e6 * ((time.time() - t0) / (1.0+X))), 'usec')
