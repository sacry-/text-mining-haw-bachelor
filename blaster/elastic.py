# coding: utf-8
from esconnect import EsConnect
from datetime import datetime


# localhost:9200/index/type/document
class Elastic():

  def __init__(self, connector=None):
    if not connector:
      connector = EsConnect()
    self.es = connector.getConnection()

  def get(self, _index, _doc_type, _id):
    return self.es.get(index=_index, doc_type=_doc_type, id=_id)["_source"]

  def delete(self, _index, _doc_type, _id):
    self.es.delete(index=_index, doc_type=_doc_type, id=_id)

  def update(self, _index, _doc_type, _id, script):
    self.es.update(index=_index, doc_type=_doc_type, id=_id, body=script)
    
  def count(self, _index="", _doc_type="", le_search={"query" : {"match_all" : {}}}):
    return self.es.count(index=_index, doc_type=_doc_type, body=le_search)["count"]

  def paginate(self, _index, _doc_type, query={"query" : {"match_all" : {}}}, _size=10):
    _id = self.retrieve_scroll_id(_index, _doc_type, query, _size)
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

  def retrieve_scroll_id(self, _index, _doc_type, query, _size=10):
    first_response = self.es.search(index=_index, doc_type=_doc_type, body=query, search_type="scan", scroll="1m", size=_size)  
    return first_response['_scroll_id']

  def scroll_by_id(self, _index, _doc_type, _scroll_id):
    return self.es.scroll(scroll_id=_scroll_id, scroll= "1m")

  def all_indices(self):
    indices = self.es.indices.stats()["indices"]
    return map(str, sorted(map(int, indices)))

  def all_documents(self, doc_type="article", query={"query" : {"match_all" : {}}}, per_page=10):
    for index in self.all_indices():
      for doc in self.all_docs_by_index(index, doc_type, query, per_page):
        yield doc

  def all_docs_by_index(self, index, doc_type="article", query={"query" : {"match_all" : {}}}, per_page=10):
    for hit in self.paginate(index, doc_type, query, per_page):
      source = hit["_source"]
      source["id"] = hit["_id"]
      source["index"] = index
      yield source

  def add_field(self, doc_type, field_name, field_val):
    script = {
      "doc": {
        field_name: field_val
      }
    }
    total_updates = 0
    for source in self.all_documents():
      self.es.update(source["index"], doc_type, source["id"], script)
      total_updates += 1
    print("updated:", total_updates)


if __name__ == "__main__":
  es = Elastic()

  f = lambda x: "{}/{}".format(x["index"],x["id"])
  a = list(map(f, es.all_documents("article")))
  b = list(map(f, es.all_documents("prep")))

  out_a = []
  for e in a:
    if not e in b and not e in out_a:
      out_a.append( e )
  for o in out_a:
    print(o)
  print("articles not preped:",len(out_a))

  out_b = []
  for e in b:
    if not e in a and not e in out_b:
      out_b.append( e )
  for o in out_b:
    print(o)
  print("preps with no article:",len(out_b))








  