from elasticsearch_dsl.connections import connections
from elasticsearch_dsl import Search
from elastic import Elastic
from article import Article
from article import article_from_hash
from utils import date_range

MAX_SIZE = 1000

class EsSearcher():

  def __init__(self, config=None):
    host, port = "localhost", 9200
    if config:
      host, port = config["host"], config["port"]
    connections.create_connection(hosts=['localhost:9200'])
    self.es = Elastic(host, port)

  def all_articles(self, paper=None):
    query = self._query_scope(paper)
    for source in self.es.all_documents("article", query):
      yield article_from_hash( source )

  def articles_for_date(self, index, paper=None):
    query = self._query_scope(paper)
    for source in self.es.all_docs_by_index(index, "article", query):
      yield article_from_hash( source )

  def articles_from_to(self, from_date, to_date, paper=None):
    for d in date_range(from_date, to_date):
      for a in self.articles_for_date(d, paper):
        yield a

  def _query_scope(self, paper=None):
    if not paper:
      return {"query" : {"match_all" : {}}}
    return {"query" : {"match" : { "newspaper" : paper}}}


if __name__ == "__main__":
  from_date, to_date = "20150601", "20150715"
  single_date = "20150704"
  paper = "theguardian"

  from_to = es.articles_from_to(from_date, to_date, paper)
  for idx, a in enumerate(from_to):
    print(idx + 1, "->", a.url) 

  paper = "theguardian"
  single = es.articles_for_date(single_date, paper)
  res = ", ".join([str(idx) for idx, _ in enumerate(single)])
  print(res)
