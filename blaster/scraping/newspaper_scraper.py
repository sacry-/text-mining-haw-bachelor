import newspaper

from newspaper import Article
from scraping.data import Data
from utils.helpers import timeit
from utils.logger import Logger


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
    s = "total articles: {} for {}".format(self.size, self.name)
    print(s)
    logger.info(s)


class Download():

  def __init__(self, source):
    self.name = source.name
    self.paper = source.paper

  @timeit
  def start(self):
    return self.download_paper()

  @timeit
  def download_paper(self):
    for article in self.paper.articles:
      article = self.download_article(article, 1)

      if not article:
        logger.info("Lost article after download: {}".format(self.name))
        continue

      title = article.title
      
      if not article.html:
        logger.info("no html in body: {}".format(title))
        continue
      
      article = self.parse_article(article)
      
      if not article:
        logger.info("could not be parsed: {}".format(title))
        continue

      yield Data(article)

  @timeit
  def download_article(self, article, retry):
    article = Article(article.url, 
                language='en', 
                keep_article_html=True, 
                fetch_images=False)
    try:
      article.download()
      if article.is_downloaded:
        return article

    except (KeyboardInterrupt, SystemExit):
      raise SystemExit("\nKeyboard was interrupted - Exiting System")
      
    except Exception as e:
      doc = "could not be downloaded: " + article.url
      exc = "exception: " + e + " - " + e.__doc__
      logger.error(doc + " " + exc)
    
    if retry > 0:
      return self.download_article(article, retry - 1)
    else:
      return None

  @timeit
  def parse_article(self, article):
    try:
      article.parse()
      if article.is_parsed:
        return article

    except (KeyboardInterrupt, SystemExit):
      raise SystemExit("\nKeyboard was interrupted - Exiting System")

    except Exception as e:
      doc = "could not be parsed: " + article.url
      exc = "exception: " + e + " - " + e.__doc__
      logger.error(doc + " " + exc)

    return None


if __name__ == "__main__":
  pass