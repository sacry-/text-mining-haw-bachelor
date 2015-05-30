from utils import read_json
from utils import timeit
from persistence import FileScraper
from scraper import Source
from scraper import Download
from scraper import newspaper_config

@timeit
def persist_articles(source_name, download):
  persister = FileScraper(source_name)
  for data in download.start():
    persister.save(data.to_h())

def build_newspapers():
  config = newspaper_config()

  sources = []
  for name, data in config.items():
    url, memoize = data["url"], data["memoize"]
    source = Source(name, url, memoize)
    source.build()
    sources.append( source )

  return sources

def download_papers_from_sources():
  sources = build_newspapers()

  for source in sources:  
    download = Download(source)
    persist_articles(source.name, download)