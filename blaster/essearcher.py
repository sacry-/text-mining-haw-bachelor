import datetime
import re

from elasticsearch_dsl.connections import connections
from elasticsearch_dsl import Search
from elastic import Elastic
from article import Article

  
DATE_PATTERN = re.compile("([0-9]{4})([0-9]{2})([0-9]{2})")

class EsSearcher():

  def __init__(self, config=None):
    host, port = "localhost", 9200
    if config:
      host, port = config["host"], config["port"]
    connections.create_connection(hosts=['localhost:9200'])
    self.es = Elastic(host, port)
    self.default_doc_type = "article"

  def all_articles(self, paper=None):
    for index in self.es.all_indices():
      for a in self.articles_for_date(index, paper):
        yield a

  def articles_for_date(self, index, paper=None):
    count = self.es.count(index, self.default_doc_type)
    s = Article.search()
    s = s[1:count]
    s = self.query_scope(s, paper)
    for a in s.execute():
      yield a

  def articles_from_to(self, from_date, to_date, paper=None):
    for d in self.date_range(from_date, to_date):
      for a in self.articles_for_date(d, paper):
        yield a

  def query_scope(self, s, paper=None):
    if not paper:
      return s.query('match_all')
    return s.query('match', newspaper=paper)

  def date_range(self, start, end):
    start = [int(x) for x in DATE_PATTERN.split(start) if x and x.strip()]
    end = [int(x) for x in DATE_PATTERN.split(end) if x and x.strip()]

    start = datetime.date(start[0],start[1],start[2])
    end = datetime.date(end[0],end[1],end[2])

    r = (end+datetime.timedelta(days=1)-start).days
    times = [start+datetime.timedelta(days=i) for i in range(r)]

    return [str(date).replace("-", "") for date in times]


if __name__ == "__main__":
  from_date, to_date = "20150630", "20150704"
  single_date = "20150704"
  paper = "nytimes"

  es = EsSearcher()
  from_to = es.articles_from_to(from_date, to_date, paper)
  for idx, a in enumerate(from_to):
    print(idx + 1, "->", a.url) 

  paper = "theguardian"
  single = es.articles_for_date(single_date, paper)
  res = ", ".join([str(idx) for idx, _ in enumerate(single)])
  print(res)


