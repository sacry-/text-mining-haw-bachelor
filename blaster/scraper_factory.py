from utils import read_json
from utils import timeit
from filescraper import FileScraper
from newspaper_scraper import Source
from newspaper_scraper import Download
from paths import newspaper_config

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