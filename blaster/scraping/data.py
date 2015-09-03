from datetime import datetime
from langdetect import detect_langs
from utils.logger import Logger
from utils.helpers import normalize_title
from router import newspaper_conf


logger = Logger(__name__).getLogger()

class Data():

  def __init__(self, article):
    self.newspaper = None
    self.ts_in = datetime.now()

    self.title = article.title
    if not self.text_valid(self.title):
      self.title = "invalid_title"
      logger.info("has no title: " + article.url)

    self.text = article.text
    if not self.text_valid(self.title):
      self.text = "invalid_text"
      logger.info("has no text: " + article.url)

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

  def text_valid(self, s):
    return s and s.strip()

  def is_valid(self, paper):
    if not self.text.strip():
      return False
      
    config = newspaper_conf()
    if not paper in config:
      return False

    news_conf = config[paper]
    whitelisted = news_conf["whitelist"]
    if self.normalized_title in whitelisted:
      return False
    
    possible_langs = detect_langs(self.title) + detect_langs(self.normalized_title)
    if not "en" in map(lambda x: x.lang, possible_langs):
      return False

    return True

if __name__ == "__main__":
  pass
