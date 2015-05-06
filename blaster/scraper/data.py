from datetime import datetime
from utils import ts_now
from utils import normalize_title
from logger import Logger

logger = Logger(__name__).getLogger()

class Data():

  def __init__(self, article):
    self.ts_in = ts_now()

    self.title = article.title
    if not self.title_valid():
      self.title = "invalid_title"
      logger.info("has no title: " + article.url)

    self.text = article.text
    if not self.text_valid():
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

    date = article.publish_date
    if isinstance(date, datetime):
      date = date.isoformat()
    self.publish_date = date

  def to_h(self):
    return { 
      "ts_in" : self.ts_in,
      "ntitle" : self.normalized_title,
      "url" : self.url,
      "canonical_link" : self.canonical_link,
      "title" : self.title,
      "text" : self.text,
      "article_html" : self.article_html,
      "keywords" : self.keywords,
      "meta_keywords" : self.meta_keywords,
      "tags" : self.tags,
      "authors" : self.authors,
      "publish_date" : self.publish_date
    }

  def title_valid(self):
    return self.title and self.title.strip()

  def text_valid(self):
    return self.text and self.text.strip()
