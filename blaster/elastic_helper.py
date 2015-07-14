import json

from esconnect import EsConnect

from article import article_from_hash
from article import Article

from router import backup_path
from utils import date_today
from os import listdir


class ElasticHelper():

  def __init__(self, connector=None):
    if not connector:
      connector = EsConnect()
    self.connector = connector
    self.es = self.connector.getConnection()

  def dump_articles(self):
    a = input("Really? (y|n) ").strip()
    if a != "y":
      return

    results, c = [], 0
    for source in self.es.all_documents():
      source["ts_in"] = str(source["ts_in"])
      results.append( source )
      c += 1
    print("loaded:",c,"documents")

    backup_dir = "{}/{}.json".format( backup_path(), date_today() )
    with open(backup_dir, "w+") as f:
      data = json.dumps(results, indent=2)
      f.write( data )

  def import_articles(self):
    a = input("Really? (y|n) ").strip()
    if a != "y":
      return

    self.connector.createConnection()

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
  