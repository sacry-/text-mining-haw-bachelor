# coding: utf-8
import math

from elasticsearch import Elasticsearch
from datetime import datetime


# localhost:9200/index/type/document
class Elastic():

  def __init__(self, host='localhost', port=9200):
    self.es = Elasticsearch([{'host': host, 'port' : port}])
    print("connection established to %s:%s" % (host, port))

  def get_document_by_id(index, doc_type, id):
    document = self.es.get(index=index, doc_type=doc_type, id=id)
    if document:
      return document['_source']
    return None

  def count(self, _index, _doc_type, le_search={"query" : {"match_all" : {}}}):
    return self.es.count(index=_index, doc_type=_doc_type, body=le_search)["count"]

  def index_doc(_index, _doc_type, uid=None, doc={"dummy": "dummy", "timestamp": datetime.now()}):
    if uid:
      self.es.index(index=_index, doc_type=_doc_type, id=uid, body=doc)
    else:
      self.es.index(index=_index, doc_type=_doc_type, body=doc)

  def update_article(self, _index, _doc_type, title, information_as_hash):
    self.es.update(_index, _doc_type, title, {"doc" : information_as_hash})

  def page(self, _index, _doc_type, _size=100):
    _id = self.retrieve_scroll_id(_index, _doc_type, _size)
    content = [""]
    while _id and content:
      data = self.scroll_by_id(_index, _doc_type, _id)
      yield data["hits"]["hits"]
      _id = data['_scroll_id']

  def retrieve_scroll_id(self, _index, _doc_type, _size=100):
    query = {"query" : {"match_all" : {}}}
    first_response = self.es.search(index=_index, doc_type=_doc_type, body=query, search_type="scan", scroll="1m", size=_size)  
    return first_response['_scroll_id']

  def scroll_by_id(self, _index, _doc_type, _scroll_id):
    return self.es.scroll(scroll_id=_scroll_id, scroll= "1m")

  def flush(self):
    if raw_input() != "flush":
      return
    print( "started deleting all" )
    self.es.delete(index="*", master_timeout=60000)
    print( "all deleted: %s elements counted" % self.es.count(index="_all") )

