from datetime import date
from logger import Logger
from elasticsearch_dsl.connections import connections
from article import createArticle
from article import Article

logger = Logger(__name__).getLogger()

class EsScraper():

  def __init__(self, paper):
    connections.create_connection(hosts=['localhost:9200'])
    self.paper = paper

  def save(self, data):
    Article.init()
    article = createArticle(data)
    logger.info("post es/" + date.today().strftime("%Y%m%d") + "/" + self.paper + "/" + article.meta.id)
    article.save()

  def read(self, identifier):
    return Article.get(id=identifier)

  def date_today(self):
    return date.today().strftime("%Y%m%d")