# coding: utf-8
import math

from elasticsearch import Elasticsearch
from datetime import datetime


# localhost:9200/index/type/document
class Elastic():

  def __init__(self, host='localhost', port=9200):
    self.es = Elasticsearch([{'host': host, 'port' : port}])
    print("connection established to %s:%s" % (host, port))

  def update(self, _index, _doc_type, _id, script):
    self.es.update(index=_index, doc_type=_doc_type, id=_id, body=script)
    
  def count(self, _index, _doc_type, le_search={"query" : {"match_all" : {}}}):
    return self.es.count(index=_index, doc_type=_doc_type, body=le_search)["count"]

  def paginate(self, _index, _doc_type, _size=10):
    _id = self.retrieve_scroll_id(_index, _doc_type, _size)
    initial_id = _id
    while _id == initial_id:
      data = self.scroll_by_id(_index, _doc_type, _id)
      for entry in data["hits"]["hits"]:
        yield entry
      _id = data['_scroll_id']

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
  c = 0
  for hit in es.paginate("20150704", "article"):
    print(hit["_id"])
    c += 1
    print(c)


