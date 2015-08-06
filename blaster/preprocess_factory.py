import os
import time

from preppersister import PrepPersister
from essearcher import EsSearcher
from preprocessor import prep_from_chunk

from utils import timeit
from logger import Logger


logger = Logger(__name__).getLogger()


@timeit
def preprocess_articles(from_date, to_date):
  chunks = []
  for a in fetch_articles(from_date, to_date):
    if not a.preprocessed:
      chunks.append( Chunk(a) )

  preper = PrepPersister()

  print("total articles:",len(chunks))
  for chunk in chunks:
    preprocess_and_persist( preper, chunk )
  print("all done!")


def preprocess_and_persist(prepper, chunk):
  prep = prep_from_chunk( chunk, tokenizer=None )
  if preper.save(chunk):
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


if __name__ == "__main__":
  preprocess_articles("20150712", None)
  