import threading
import queue

from utils import timeit
from scraper import Scraper
from newspaper_scraper import Source
from newspaper_scraper import Download
from router import newspaper_conf, app_conf


def download_papers_from_sources():
  pool, q = [], queue.Queue()

  conf = newspaper_conf()
  for name, data in conf.items():
    memoize = data["memoize"]
    for url in data["urls"]:
      thr = threading.Thread(
        target=download_paper_from_source, 
        args=(name, url, memoize, q), 
        kwargs={}
      )
      thr.start()
      pool.append(thr)

  [t.join() for t in pool]
  print_queue_count(q)

def download_paper_from_source(name, url, memoize, q):
  print("paper: ", name, " with: ", url)

  source = Source(name, url, memoize)
  source.build()

  download = Download(source)
  actual = persist_articles(source.name, download)

  count_queue(q, source.size, actual)

@timeit
def persist_articles(source_name, download):
  conf = app_conf()
  persister = Scraper(source_name, conf["elasticsearch"])
  actual = 0
  for data in download.start():
    data.newspaper = source_name
    saved = persister.save(data)
    if saved: 
      actual += 1
  return actual

def count_queue(q, total, actual):
  h = {"total" : 0, "actual" : 0}
  if not q.empty():
    h = q.get()
  h["total"] += total
  h["actual"] += actual
  q.put(h)

def print_queue_count(q):
  if not q.empty():
    h = q.get()
    print("total:",h["total"],"actual:",h["actual"])
  else:
    print("No count! W00t?!")


if __name__ == "__main__":
  pass