import threading
import queue

from utils import timeit
from scraping import ArticlePersister
from scraping import Source
from scraping import get_sources
from scraping import Download


def download_and_persist_sources( sources=None ):
  if not sources:
    sources = get_sources()

  running_threads = []
  dispatch_queue = queue.Queue()

  for source in sources:
    thr = threading.Thread(
      target=download_and_persist_source, 
      args=(source, dispatch_queue), 
      kwargs={}
    )
    thr.start()
    running_threads.append(thr)

  [t.join() for t in running_threads]

  print("Finished job!")


def download_and_persist_source(source, dispatch_queue):
  print("paper: ", source.name, " with: ", source.url)

  source.build()

  download = Download(source)
  actual = persist_articles(source, download)

  if not actual:
    print("did not download any articles")

  else:
    print("total:", source.size, "actual:", actual)

@timeit
def persist_articles(source, download):
  persister = ArticlePersister( source.name )

  actual = 0
  for data in download.start():

    if not data.is_valid(source.whitelist):
      print("data invalid:", data.normalized_title)
      continue

    data.newspaper = source.name
    if persister.save(data): 
      actual += 1

  return actual


if __name__ == "__main__":
  download_and_persist_sources()

