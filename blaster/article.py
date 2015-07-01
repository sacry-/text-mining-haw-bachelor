from datetime import date
from datetime import datetime
from elasticsearch_dsl import DocType, String, Date, Nested, analysis


class Article(DocType):
  ts_in = Date()
  newspaper = String(analyzer='snowball')
  publish_date = String()
  title = String()
  text = String(analyzer='snowball')
  article_html = String(analyzer='snowball')
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

'''
  Article(
    meta={'id' : "some_title"}, 
    ts_in=datetime.now(), 
    newspaper="theguardian"
    normalized_title="some_title",
    url="www.url_canonical.de/us/Some-title",
    canonical_link="www.url_canonical.de/us/Some-title",
    title="Some title",
    text="text",
    article_html="<html>text</html>",
    keywords=[],
    meta_keywords=[],
    tags=[],
    authors=[],
    publish_date = datetime.now()
  )
'''
def createArticle(d):
  return Article(
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
    publish_date=datetime.now()
  )

