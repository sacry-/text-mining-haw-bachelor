import dateutil.parser
from datetime import datetime
from elasticsearch_dsl import DocType, Nested, analysis
from elasticsearch_dsl import String, Boolean, Date
from utils import date_for_index
from utils import date_today


class Article(DocType):
  ts_in = Date()
  newspaper = String()
  publish_date = String()
  title = String()
  text = String()
  article_html = String()
  url = String()
  canonical_link = String()
  preprocessed = Boolean()
  keywords = String(fields={'raw': String(index='not_analyzed')})
  meta_keywords = String(fields={'raw': String(index='not_analyzed')})
  tags = String(fields={'raw': String(index='not_analyzed')})
  authors = String(fields={'raw': String(index='not_analyzed')})
  categories = String(fields={'raw': String(index='not_analyzed')})

  class Meta:
    index = date_today()

  def save(self, ** kwargs):
    return super(Article, self).save(** kwargs)

def article_from_data(d):
  a = Article(
    meta={'id' : d.normalized_title}, 
    ts_in=datetime.now(), 
    newspaper=d.newspaper,
    url=d.url,
    preprocessed=False,
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

def article_from_hash(h):
  if not isinstance(h["ts_in"], datetime):
    h["ts_in"] = dateutil.parser.parse(h["ts_in"])
  if not "preprocessed" in h:
    h["preprocessed"] = False
  a = Article(
    meta={'id' : h["id"]}, 
    ts_in=h["ts_in"], 
    newspaper=h["newspaper"],
    url=h["url"],
    preprocessed=h["preprocessed"],
    canonical_link=h["canonical_link"],
    title=h["title"],
    text=h["text"],
    article_html=h["article_html"],
    keywords=h["keywords"],
    meta_keywords=h["meta_keywords"],
    tags=h["tags"],
    authors=h["authors"],
    publish_date=h["publish_date"],
    categories=[]
  )
  a._index = h["index"]
  return a

def article_to_hash(a):
  h = a.to_dict()
  h["index"] = a._index
  h["id"] = a.meta.id
  h["ts_in"] = str(h["ts_in"])
  return h

if __name__ == "__main__":
  pass

