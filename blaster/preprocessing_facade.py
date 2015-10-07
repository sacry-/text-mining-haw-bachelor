import time

from preprocessing import PrepPersister
from preprocessing import Chunk
from preprocessing import preprocessor_from_chunk
from es import EsSearcher

from utils import timeit
from utils import Logger


logger = Logger(__name__).getLogger()

@timeit
def preprocess_articles(from_date, to_date):
  chunks = []
  for a in fetch_articles(from_date, to_date):

    if not a.preprocessed:
      chunks.append( Chunk(a) )

  preper = PrepPersister()

  print("Total articles:",len(chunks))
  for chunk in chunks:
    preprocess_and_persist( preper, chunk )
  print("Finished Job!")


def preprocess_and_persist(preper, chunk):
  prep = preprocessor_from_chunk( chunk, tokenizer=None )
  if preper.save(prep):
    try:
      chunk.update_article()
    except Exception as e:
      logger.error("article for chunk could not be updated: " + e)

def fetch_articles(from_date, to_date):
  searcher = EsSearcher()
  if from_date and not to_date:
    return searcher.articles_for_date(from_date)
  elif from_date and to_date:
    return searcher.articles_from_to(from_date, to_date)
  else:
    return searcher.all_articles()


if __name__ == "__main__":
  preprocess_articles("20150712", None)
  