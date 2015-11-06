import json

from es import EsConnect
from es import Elastic

from scraping import article

from router import backup_path
from utils.helpers import date_today
from utils.logger import Logger
from os import listdir


logger = Logger(__name__).getLogger()

class ElasticSnapper():

  def __init__(self, connector=None):
    self.connector = connector
    if not self.connector:
      self.connector = EsConnect()
    self.es = Elastic( self.connector )

  def dump(self):
    if not self.should_proceed("dump"):
      return

    logger.info("proceeding with dumping!")

    documents = []
    for source in self.es.all_documents():
      source["ts_in"] = str(source["ts_in"])
      documents.append( source )

    backup_dir = self.backup( date_today() )

    with open(backup_dir, "w+") as f:
      data = json.dumps(documents, indent=2)
      f.write( data )

    self.print_affected("dumped", len(documents))


  def reimport(self):
    if not self.should_proceed("import"):
      return

    logger.info("proceeding with import!")

    self.connector.createConnection() 

    backup_dir = self.backup( self.latest_backup_file() )

    affected_documents = 0
    with open(backup_dir, "r+") as f:

      Article.init()

      for h in json.load(f):
        a = article.article_from_hash( h )
        a.save()
        affected_documents += 1

    self.print_affected("imported", affected_documents)


  # Helpers
  def print_affected(self, scope, affected):
    msg = scope + " " + str(affected) + " documents"
    logger.info(msg)
    print(msg)

  def should_proceed(self, method):
    message = "Are you sure you want to {}? (yes|anything) ".format( method )
    return "yes" == input( message ).strip()

  def backup(self, name):
    return "{}/{}.json".format( backup_path(), name )

  def latest_backup_file(self):
    return str( max([int(f.strip(".json")) for f in listdir(backup_path())]) )


if __name__ == "__main__":
  eS = ElasticSnapper()
  eS.dump()
  