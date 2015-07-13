import os
import multiprocessing
import time

from preprocessor import preprocess
from essearcher import EsSearcher
from utils import timeit


class Chunk():

  def __init__(self, a):
    self.id = a.meta.id
    self.title = a.title
    self.text = a.text
    self.article_html = a.article_html

def persist(prep):
  print("persistence magic here")

def threaded_preprocess(chunk):
  prep = preprocess( chunk, tokenizer=None )
  persist(prep)

@timeit
def preprocess_articles(from_date, to_date):
  chunks = []
  for a in fetch_articles(from_date, to_date):
    if not a.preprocessed:
      chunks.append( Chunk(a) )
  print("total articles:",len(chunks))

  cpu_count = max(2, os.cpu_count() - 1)
  with multiprocessing.Pool(cpu_count) as p:
    p.map(threaded_preprocess, chunks)

  print("all done!")

def fetch_articles(from_date, to_date):
  articles = []
  if from_date and not to_date:
    if from_date == "all":
      articles = EsSearcher().all_articles()
    else:
      articles = EsSearcher().articles_for_date(from_date)
  elif from_date and to_date:
    articles = EsSearcher().articles_from_to(from_date, to_date)

  return articles

if __name__ == "__main__":
  preprocess_articles("20150712", None)
  