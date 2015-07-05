import os
import multiprocessing
import time

from preprocessor import preprocess
from essearcher import EsSearcher
from utils import timeit


START_TS = time.time() # HACK!
def threaded_preprocess(t):
  mid, text = t
  prep = preprocess( text )
  prep.pos_tags()
  prep.ner_extract()
  print("Done: {}, {:2.2f}".format(mid, time.time() - START_TS))
  return prep

@timeit
def preprocess_articles(from_date, to_date):
  fetched = fetch_articles(from_date, to_date)
  articles = map(lambda a: (a.meta.id, a.text), list(fetched))

  cpu_count = max(2, os.cpu_count() - 1)
  with multiprocessing.Pool(cpu_count) as p:
    p.map(threaded_preprocess, articles)

  print("All Done!")


def fetch_articles(from_date, to_date):
  searcher = EsSearcher()

  articles = []
  if from_date and not to_date:
    if from_date == "all":
      articles = searcher.all_articles()
    else:
      articles = searcher.articles_for_date(from_date)
  elif from_date and to_date:
    articles = searcher.articles_from_to(from_date, to_date)

  return articles
