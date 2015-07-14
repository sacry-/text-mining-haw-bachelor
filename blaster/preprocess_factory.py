import os
import time

from preprocessor import prep_from_chunk
from preprocessor import Prep
from utils import timeit

from logger import Logger
from essearcher import EsSearcher
from esconnect import EsConnect


logger = Logger(__name__).getLogger()

class Chunk():

  def __init__(self, a):
    self.a = a
    self.index = a._index
    self.id = a.meta.id
    self.title = a.title
    self.text = a.text
    self.article_html = a.article_html

  def update_article(self):
    self.a.preprocessed = True
    self.a.save()

def preprocess_and_persist(chunk):
  try:
    prep = prep_from_chunk( chunk, tokenizer=None )
    prep.save()
    chunk.update_article()
    logger.info("preprocessed: {}/prep/{}".format(chunk.index, chunk.id))
  except Exception as e:
    logger.error("prep could not be created: " + e)

@timeit
def preprocess_articles(from_date, to_date):
  chunks = []
  for a in fetch_articles(from_date, to_date):
    if not a.preprocessed:
      chunks.append( Chunk(a) )
  print("total articles:",len(chunks))

  EsConnect().createConnection()
  Prep.init()

  for chunk in chunks:
    preprocess_and_persist( chunk )

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
  