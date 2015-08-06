from esconnect import EsConnect
from elastic import Elastic

from article import article_from_hash
from utils import date_range


# curl -XDELETE '127.0.0.1:9200/20150712/article/_query?q=newspaper:vice'
# curl -XDELETE '127.0.0.1:9200/20150712/article/restaurant_report_konyvbar_in_budapest

# curl '127.0.0.1:9200/_cat/indices?v' | sort -rnk2
# curl '127.0.0.1:9200/_cat/indices?v' | sort -rnk2 | grep "20150[678].*"

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

  def count_all(self, doc_type, matching={"match_all" : {}}):
    total = 0
    for index in self.es.all_indices():
      total += self.es.count(index, doc_type, {"query" : matching})
    return total

  def count_index(self, index, doc_type):
    return self.es.count(index, doc_type, self._query_scope())

  def _query_scope(self, paper=None):
    if not paper:
      return {"query" : {"match_all" : {}}}
    return {"query" : {"match" : { "newspaper" : paper}}}


if __name__ == "__main__":
  es = EsSearcher()

  article_count = es.count_all("article")
  preped_article_count = es.count_all("article", {"match" : { "preprocessed" : True}})
  prep_count = es.count_all("prep")
  print("article count:",article_count)
  print("preped article count:",preped_article_count)
  print("prep count:",prep_count)
  print("missing:",article_count - prep_count)

  from_date, to_date = "20150701", "20150716"
  total = 0
  for index in date_range(from_date, to_date):
    c = es.count_index(index, "article")
    print(index, c)
    total += c
  print("total", total)

