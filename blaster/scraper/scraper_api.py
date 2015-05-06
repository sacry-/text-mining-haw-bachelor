
def build_papers_from_sources():
  from utils import read_json
  from paths import newspapers_path
  from downloader import Source

  json = read_json(newspapers_path())

  sources = []
  for name, data in json.items():
    url, memoize = data["url"], data["memoize"]
    source = Source(name, url, memoize)
    source.build()
    sources.append( source )

  return sources


def download_papers_from_sources():
  from downloader import Download

  sources = build_papers_from_sources()
  for source in sources:
    Download(source).start()





