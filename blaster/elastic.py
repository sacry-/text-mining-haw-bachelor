# coding: utf-8
import math

from elasticsearch import Elasticsearch
from datetime import datetime


# localhost:9200/index/type/document
class Elastic():

  def __init__(self, host='localhost', port=9200):
    self.es = Elasticsearch([{'host': host, 'port' : port}])
    print("connection established to %s:%s" % (host, port))

  def count(self, _index, _doc_type, le_search={"query" : {"match_all" : {}}}):
    return self.es.count(index=_index, doc_type=_doc_type, body=le_search)["count"]

  def pagiante(self, _index, _doc_type, _size=100):
    total_items = self.count(_index, _doc_type)
    _id = self.retrieve_scroll_id(_index, _doc_type, _size)
    while _id and total_items > 0:
      data = self.scroll_by_id(_index, _doc_type, _id)
      for entry in data["hits"]["hits"]:
        yield entry
      _id = data['_scroll_id']
      total_items -= _size

  def retrieve_scroll_id(self, _index, _doc_type, _size=100):
    query = {"query" : {"match_all" : {}}}
    first_response = self.es.search(index=_index, doc_type=_doc_type, body=query, search_type="scan", scroll="1m", size=_size)  
    return first_response['_scroll_id']

  def scroll_by_id(self, _index, _doc_type, _scroll_id):
    return self.es.scroll(scroll_id=_scroll_id, scroll= "1m")

  def all_indices(self):
    indices = self.es.indices.stats()["indices"]
    return map(str, sorted(map(int, indices)))

if __name__ == "__main__":
  es = Elastic()
  indices = list(es.all_indices())
  for idx, index in enumerate(indices):
    print(idx + 1, index)
  index = "20150704"
  date_count = es.count(index, "article")
  print(index, "count:", date_count)

