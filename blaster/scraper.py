from datetime import date
from logger import Logger
from elasticsearch_dsl.connections import connections
from elasticsearch_dsl import Index
from article import createArticle
from article import Article


logger = Logger(__name__).getLogger()

class Scraper():

  def __init__(self, paper, config=None):
    host, port = "localhost", 9200 # defaults
    if config:
      host, port = config["host"], config["port"]
    connections.create_connection(hosts=['{}:{}'.format(host,port)])
    self.paper = paper

  def save(self, data):
    try:
      Article.init()
      a = createArticle(data)
      a.save()
      logger.info(self.logging_text(a))
    except Exception as e:
      logger.error("article could not be created: " + e)
      return False
    return True

  def date_today(self):
    return date.today().strftime("%Y%m%d")

  def logging_text(self, a):
    return ("> " + a.newspaper + " uri/" + a._index + "/article/" + a.meta.id)


if __name__ == "__main__":
  pass
