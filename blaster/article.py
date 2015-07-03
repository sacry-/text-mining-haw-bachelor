from datetime import date
from datetime import datetime
from elasticsearch_dsl import DocType, String, Date, Nested, analysis
from utils import date_for_index

class Article(DocType):
  ts_in = Date()
  newspaper = String()
  publish_date = String()
  title = String()
  text = String()
  article_html = String()
  url = String()
  canonical_link = String()
  keywords = String(fields={'raw': String(index='not_analyzed')})
  meta_keywords = String(fields={'raw': String(index='not_analyzed')})
  tags = String(fields={'raw': String(index='not_analyzed')})
  authors = String(fields={'raw': String(index='not_analyzed')})

  class Meta:
    index = date.today().strftime("%Y%m%d")

  def save(self, ** kwargs):
    return super(Article, self).save(** kwargs)

def createArticle(d):
  a = Article(
    meta={'id' : d.normalized_title}, 
    ts_in=datetime.now(), 
    newspaper=d.newspaper,
    url=d.url,
    canonical_link=d.canonical_link,
    title=d.title,
    text=d.text,
    article_html=d.article_html,
    keywords=d.keywords,
    meta_keywords=d.meta_keywords,
    tags=d.tags,
    authors=d.authors,
    publish_date=d.publish_date
  )
  date_index = date_for_index(d.publish_date)
  if date_index:
    a._index = date_index
  return a

if __name__ == "__main__":
  pass

