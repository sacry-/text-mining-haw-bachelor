import threading
import queue
import time


def do_stuff(q):
  time.sleep(0.5)
  arg = q.get()
  time.sleep(0.5)
  print( arg + 10 )

q = queue.Queue(maxsize=3)
pool = []
for var in [1,2,3,4,5,6,7,8,9,10]:
  q.put( var )
  thr = threading.Thread(
    target=do_stuff, 
    args=(q,), 
    kwargs={}
  )
  thr.start()
