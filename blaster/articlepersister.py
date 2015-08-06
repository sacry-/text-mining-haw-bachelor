from logger import Logger
from esconnect import EsConnect

from article import Article
from article import article_from_data


logger = Logger(__name__).getLogger()

class ArticlePersister():

  def __init__(self, paper, connector=None):
    if not connector:
      connector = EsConnect()
    self.es = connector.createConnection()
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


if __name__ == "__main__":
  pass
