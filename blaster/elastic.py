# coding: utf-8
import json

from elasticsearch import Elasticsearch
from datetime import datetime

from article import article_from_hash
from article import Article
from router import backup_path
from utils import date_today
from os import listdir

# localhost:9200/index/type/document
class Elastic():

  def __init__(self, host='localhost', port=9200):
    self.es = Elasticsearch([{'host': host, 'port' : port}])
    print("connection established to %s:%s" % (host, port))

  def update(self, _index, _doc_type, _id, script):
    self.es.update(index=_index, doc_type=_doc_type, id=_id, body=script)
    
  def count(self, _index="", _doc_type="", le_search={"query" : {"match_all" : {}}}):
    return self.es.count(index=_index, doc_type=_doc_type, body=le_search)["count"]

  def paginate(self, _index, _doc_type, _size=10):
    _id = self.retrieve_scroll_id(_index, _doc_type, _size)
    initial_id = _id
    retry = 3
    while retry > 0:
      data = self.scroll_by_id(_index, _doc_type, _id)
      for entry in data["hits"]["hits"]:
        yield entry
      _id = data['_scroll_id']
      data = None
      if _id != initial_id:
        retry -= 1

  def retrieve_scroll_id(self, _index, _doc_type, _size=100):
    query = {"query" : {"match_all" : {}}}
    first_response = self.es.search(index=_index, doc_type=_doc_type, body=query, search_type="scan", scroll="1m", size=_size)  
    return first_response['_scroll_id']

  def scroll_by_id(self, _index, _doc_type, _scroll_id):
    return self.es.scroll(scroll_id=_scroll_id, scroll= "1m")

  def all_indices(self):
    indices = self.es.indices.stats()["indices"]
    return map(str, sorted(map(int, indices)))

  def all_articles(self, doc_type="article", per_page=10):
    for index in self.all_indices():
      for hit in self.paginate(index, doc_type, per_page):
        source = hit["_source"]
        source["id"] = hit["_id"]
        source["index"] = index
        yield source

  def dump_all(self):
    a = input("Really? (y|n) ").strip()
    if a != "y":
      return

    results, c = [], 0
    for source in self.all_articles():
      source["ts_in"] = str(source["ts_in"])
      results.append( source )
      c += 1
    print("loaded:",c,"documents from:", self.count())

    backup_dir = "{}/{}.json".format( backup_path(), date_today() )
    with open(backup_dir, "w+") as f:
      data = json.dumps(results, indent=2)
      f.write( data )

  def import_all(self):
    a = input("Really? (y|n) ").strip()
    if a != "y":
      return

    c = 0
    name = max([int(f.strip(".json")) for f in listdir(backup_path())])
    backup_dir = "{}/{}.json".format( backup_path(), str(name) )
    with open(backup_dir, "r+") as f:
      all_data = json.load(f)
      for h in all_data:
        Article.init()
        a = article_from_hash( h )
        a.save()
        c += 1
    print("imported:",c,"documents")

  def add_field(self, field_name, field_val):
    script = {
      "doc": {
        field_name: field_val
      }
    }
    total_updates = 0
    for source in self.all_articles():
      self.es.update(source["index"], "article", source["id"], script)
      total_updates += 1
    print("updated:", total_updates)

if __name__ == "__main__":
  es = Elastic()
  es.add_field("preprocessed", False)


