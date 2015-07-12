import json

from os import listdir
from essearcher import EsSearcher
from article import article_from_data, article_from_hash, article_to_hash
from utils import date_today
from router import backup_path

from logger import Logger
from elasticsearch_dsl.connections import connections
from elasticsearch_dsl import Index
from article import Article


logger = Logger(__name__).getLogger()

class EsPersister():

  def __init__(self, paper, config=None):
    host, port = "localhost", 9200 # defaults
    if config:
      host, port = config["host"], config["port"]
    connections.create_connection(hosts=['{}:{}'.format(host,port)])
    self.paper = paper

  def save(self, data):
    try:
      Article.init()
      a = article_from_data(data)
      a.save()
      logger.info(self.logging_text(a))
    except Exception as e:
      logger.error("article could not be created: " + e)
      return False
    return True

  def logging_text(self, a):
    return ("> " + a.newspaper + " uri/" + a._index + "/article/" + a.meta.id)

  def dump_all(self):
    a = input("Really? (y|n) ").strip()
    if a != "y":
      return

    results = []
    for a in EsSearcher().all_articles():
      results.append( article_to_hash(a) )
    backup_dir = "{}/{}.json".format( backup_path(), date_today() )
    print("dumping all es indices to {}".format( backup_dir ))
    with open(backup_dir, "w+") as f:
      data = json.dumps(results, indent=2)
      f.write( data )

  def import_all(self):
    a = input("Really? (y|n) ").strip()
    if a != "y":
      return

    name = max([int(f.strip(".json")) for f in listdir(backup_path())])
    backup_dir = "{}/{}.json".format( backup_path(), str(name) )
    print("this is the dir: {}".format( backup_dir ))
    with open(backup_dir, "r+") as f:
      all_data = json.load(f)
      for h in all_data:
        Article.init()
        a = article_from_hash( h )
        a.save()


if __name__ == "__main__":
  pass

'''
  p = EsPersister("none")
  p.import_all()
  p.dump_all()
'''
