import json

from elastic import Elastic
from elasticsearch_dsl.connections import connections

from article import article_from_hash
from article import Article

from router import backup_path
from utils import date_today
from os import listdir


class ElasticHelper():

  def __init__(self):
    self.es = Elastic()

  def dump_articles(self):
    a = input("Really? (y|n) ").strip()
    if a != "y":
      return

    results, c = [], 0
    for source in self.es.all_articles():
      source["ts_in"] = str(source["ts_in"])
      results.append( source )
      c += 1
    print("loaded:",c,"documents from:", self.count())

    backup_dir = "{}/{}.json".format( backup_path(), date_today() )
    with open(backup_dir, "w+") as f:
      data = json.dumps(results, indent=2)
      f.write( data )

  def import_articles(self):
    a = input("Really? (y|n) ").strip()
    if a != "y":
      return

    connections.create_connection(hosts=['localhost:9200'])

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


if __name__ == "__main__":
  eh = ElasticHelper()
  eh.dump_articles()
  