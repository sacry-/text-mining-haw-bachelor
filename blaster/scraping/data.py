from datetime import datetime
from langdetect import detect_langs

from utils.logger import Logger
from utils.helpers import normalize_title


logger = Logger(__name__).getLogger()

class Data():

  def __init__(self, article):
    self.newspaper = None
    self.ts_in = datetime.now()

    self.title = article.title
    self.text = article.text
    self.url = article.url

    self.normalized_title = normalize_title(self.title)

    self.canonical_link = article.canonical_link
    if self.url == self.canonical_link:
      self.canonical_link = ""

    self.article_html = article.article_html
    self.keywords = list(article.keywords)
    self.meta_keywords = list(article.meta_keywords)
    self.tags = list(article.tags)
    self.authors = list(article.authors)

    self.publish_date = str(article.publish_date)
    if not self.publish_date:
      self.publish_date = str(datetime.now())

  def is_valid(self, whitelist):
    if not self.title.strip():
      logger.info("has invalid title: " + self.url)
      return False

    if not self.text.strip():
      logger.info("has invalid text: " + self.url)
      return False
      
    if self.normalized_title in whitelist:
      logger.info("is whitelisted: " + self.url)
      return False
    
    possible_langs = detect_langs(self.title) + detect_langs(self.normalized_title)
    if not "en" in map(lambda x: x.lang, possible_langs):
      logger.info("could not detect english language: " + self.url)
      return False

    return True

if __name__ == "__main__":
  pass
