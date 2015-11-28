import time
import signal

from preprocessing import PrepPersister
from preprocessing import preprocess
from persistence import EsSearcher

from utils import timeit
from utils import Logger


logger = Logger(__name__).getLogger()

@timeit
def preprocess_articles(from_date, to_date):
  signal.signal(signal.SIGALRM, timeout_handler)

  to_process = []
  for a in fetch_articles(from_date, to_date):
    if not a.preprocessed:
      to_process.append( a )

  print("Total articles: {}".format(len(to_process)))

  prep_persister = PrepPersister()

  unprocessed = []
  for a in to_process:

    preprocessor = None
    try:
      signal.alarm(10)
      preprocessor = preprocess( a, tokenizer=None )
    except Exception as e:
      logger.error("{} - {}".format(str(e), str(a)))
      unprocessed.append( str(a) )
    signal.alarm(0)

    if preprocessor and prep_persister.save(preprocessor):
      try:
        a.preprocessed = True
        a.save()
      except Exception as e:
        logger.error("article could not be updated: {} - {}".format(str(e), str(a)))
  
  print("Could not preprocess:")
  for uri in unprocessed:
    print("  ", uri)
  print("Finished Job!")


def fetch_articles(from_date, to_date):
  searcher = EsSearcher()
  if from_date and not to_date:
    return searcher.articles_for_date(from_date)
  elif from_date and to_date:
    return searcher.articles_from_to(from_date, to_date)
  else:
    return searcher.all_articles()

def timeout_handler(signum, frame):
  print("Timeout: could not preprocess article")
  raise Exception("Timeout: article is not processable!")

if __name__ == "__main__":
  preprocess_articles("20150712", None)
  