from elasticsearch_dsl.connections import connections
from elasticsearch_dsl import Search
from elastic import Elastic
from article import Article


class EsSearcher():

  def __init__(self, config=None):
    host, port = "localhost", 9200
    if config:
      host, port = config["host"], config["port"]
    connections.create_connection(hosts=['localhost:9200'])
    self.es = Elastic(host, port)

  def articles_by_newspaper(self, index, doc_type, paper):
    count = self.es.count(index, doc_type)
    s = Article.search()
    s = s[1:count]
    s = s.query('match', newspaper=paper)
    for a in s.execute():
      yield a

  def all_articles(self, index, doc_type):
    count = self.es.count(index, doc_type)
    print(count)
    s = Article.search()
    s = s[1:count]
    s = s.query('match_all')
    for a in s.execute():
      yield a

if __name__ == "__main__":
  pass



