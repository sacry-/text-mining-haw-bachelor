from utils import timeit
from scraper import Scraper
from newspaper_scraper import Source
from newspaper_scraper import Download
from router import newspaper_conf, app_conf

@timeit
def persist_articles(source_name, download):
  conf = app_conf()
  persister = Scraper(source_name, conf["elasticsearch"])
  for data in download.start():
    data.newspaper = source_name
    persister.save(data)

def build_newspapers():
  conf = newspaper_conf()
  sources = []
  for name, data in conf.items():
    memoize = data["memoize"]
    for url in data["urls"]:
      print("paper: ", name, " with: ", url)
      source = Source(name, url, memoize)
      source.build()
      sources.append( source )

  return sources

def download_papers_from_sources():
  sources = build_newspapers()

  for source in sources:  
    download = Download(source)
    persist_articles(source.name, download)