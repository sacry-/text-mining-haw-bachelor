import random

from scraping.article import article_from_hash

from persistence.esconnect import EsConnect
from persistence.elastic import Elastic
from persistence.helpers import date_range

from collections import Counter

# curl -XDELETE '127.0.0.1:9200/20150712/article/_query?q=newspaper:vice'
# curl -XDELETE '127.0.0.1:9200/20150712/article/restaurant_report_konyvbar_in_budapest

# curl '127.0.0.1:9200/_cat/indices?v' | sort -rnk2
# curl '127.0.0.1:9200/_cat/indices?v' | sort -rnk2 | grep "2015[067891]{2}.*"

# curl '127.0.0.1:9200/_cat/indices?v' | sort -rnk2 | grep "20150[78]{2}.*"
# curl '127.0.0.1:9200/_cat/indices?v' | sort -rnk2 | grep "201511.*"

# curl '127.0.0.1:9200/_nodes/settings?pretty=true'
# curl '127.0.0.1:9200/_count'
# curl '127.0.0.1:9200/20150712/article/_search?q=newspaper:theguardian&size=1000'
class EsSearcher():

  def __init__(self, connector=None):
    if not connector:
      connector = EsConnect()
    self.es = Elastic( connector )

  def all_articles(self, paper=None):
    query = self._query_scope(paper)
    for source in self.es.all_documents("article", query):
      yield article_from_hash( source )

  def articles_for_date(self, index, paper=None):
    query = self._query_scope(paper)
    for source in self.es.all_docs_by_index(index, "article", query):
      yield article_from_hash( source )

  def articles_from_to(self, from_date, to_date, paper=None):
    possible_indices = self.es.all_indices()
    for index in date_range(from_date, to_date):
      if index in possible_indices:
        for a in self.articles_for_date(index, paper):
          yield a

  def article_at(self, a_date, doc, title):
    return article_from_hash( self.es.get(a_date, doc, title) )

  def choose_k(self, indices, paper=None):
    articles = []
    for (index, count) in Counter(indices).items():
      intermediate = []
      for a in self.articles_for_date(index, paper):
        intermediate.append( a )
      articles += random.sample(intermediate, count)
    return articles

  def prep_for_index(self, _index, _id):
    try:
      source = self.es.get(_index, "prep", _id)
      return source
    except:
      return {}

  def prep_for_date(self, index, paper=None):
    query = self._query_scope(paper)
    for source in self.es.all_docs_by_index(index, "prep", query):
      yield source

  def prep_from_to(self, from_date, to_date, paper=None):
    possible_indices = self.es.all_indices()
    for index in date_range(from_date, to_date):
      if index in possible_indices:
        for source in self.prep_for_date(index, paper):
          yield source

  def count_all(self, doc_type, matching={"match_all" : {}}):
    total = 0
    for index in self.indices():
      total += self.es.count(index, doc_type, {"query" : matching})
    return total

  def indices(self):
    return self.es.all_indices()

  def count_index(self, index, doc_type):
    return self.es.count(index, doc_type, self._query_scope())

  def _query_scope(self, paper=None):
    if not paper:
      return {"query" : {"match_all" : {}}}
    return {"query" : {"match" : { "newspaper" : paper}}}

  def ping(self):
    return self.es.ping()

  def ids_for_index(self, _index, doc_type):
    query = {
      "query": {"match_all": {}}, 
      "size": 1000, 
      "fields": ["_id"]
    }
    res = self.es.search(_index, doc_type, query)
    return [d['_id'] for d in res['hits']['hits']]

  def possible_indices(self, from_date, to_date):
    possible_indices = self.es.all_indices()
    for index in date_range(from_date, to_date):
      if index in possible_indices:
        yield index

if __name__ == "__main__":
  es = EsSearcher()
  
  article_count = es.count_all("article")
  preped_article_count = es.count_all("article", {"match" : { "preprocessed" : True}})
  print("article count:",article_count)
  print("preped article count:",preped_article_count)
  print("article_count - preped_articles =", article_count - preped_article_count)

  if False:
    from_date, to_date = "20010129", "20151207"
    missing = []
    for a in es.articles_from_to(from_date, to_date):
      try:
        elastic.article_at(a._index, "prep", a.meta.id)
      except:
        missing.append( [a._index, a.meta.id] )
    print(missing)

