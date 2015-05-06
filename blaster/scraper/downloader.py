import newspaper

from newspaper import Article
from data import Data
from persister import Persister
from utils import timeit
from logger import Logger

logger = Logger(__name__).getLogger()

class Source():

  def __init__(self, name, url, memoize=True):
    self.name = name
    self.url = url
    self.memoize = memoize
    self.paper = None
    self.size = 0

  @timeit
  def build(self):
    s = "building {} : {}".format(self.name, self.url)
    print(s)
    logger.info(s)
    self.paper = newspaper.build(self.url, 
                            language='en', 
                            memoize_articles=self.memoize)
    self.size = len(self.paper.articles)
    s = "total articles: {}".format(self.size)
    print(s)
    logger.info(s)


class Download():

  def __init__(self, source):
    self.name = source.name
    self.url = source.url
    self.paper = source.paper
    self.persister = Persister(self.name)

  @timeit
  def start(self):
    downloaded = self.download_paper()
    self.persist_articles(downloaded)

  @timeit
  def download_paper(self):
    for article in self.paper.articles:
      article = self.download_article(article)
      if not article:
        continue
      yield Data(article)

  @timeit
  def download_article(self, article):
    a = Article(article.url, 
                language='en', 
                keep_article_html=True, 
                fetch_images=False)
    try:
      a.download()
    except:
      logger.info("could not be downloaded: " + article.url)
      return None

    try:
      a.parse()
    except:
      logger.info("could not be parsed: " + article.url)
      return None

    return a

  @timeit
  def persist_articles(self, articles):
    for data in articles:
      self.persister.save(data.to_h())


