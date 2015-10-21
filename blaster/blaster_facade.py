import os
import sys

from termcolor import colored

from utils import Logger
from utils import ElasticSnapper

from scraping_facade import download_and_persist_sources
from preprocessing_facade import preprocess_articles
from es import EsSearcher


logger = Logger("blaster").getLogger()

def usage():
  description = "Process newspaper articles and cluster them with blaster!"
  print("\n", colored(description, "green", attrs=["underline"]))

  cmds = [
    ["(--help | -h)", ["prints this summary"]],
    ["scrape", ["for scraping newspapers defined in your newspaper config found under 'resources'"]],
    ["preprocess (None|from_date|from_date to_date)", ["for preprocessing articles from to a time period, or all if none provided", "e.g. blaster preprocess 20150712 20150716"]],
    ["features", ["create features for articles (not implemented)"]],
    ["cluster", ["cluster preprocessed articles (not implemented)"]],
    ["dump", ["dumps all articles persisted in elasticsearch to a json document"]],
    ["import", ["imports all articles from a JSON into elasticsearch"]],
    ["count", ["provides some general counts and es information"]],
  ]
  for cmd, descr in cmds:
    print("  blaster", 
      colored(cmd, "yellow"), 
      colored("\n\t" + "\n\t".join(descr), "magenta"), "\n")

def check_db_is_up():
  es = None
  try:
    es = EsSearcher()
  except:
    pass
  if not es or (es and not es.ping()):
    raise Exception("Failed to connect to elasticsearch at localhost:9200!")

def blaster_facade(cmd, args):
  check_db_is_up()

  if cmd == "scrape": 
    logger.info("scrape")
    download_and_persist_sources()

  elif cmd == "preprocess": 
    logger.info("preprocess")
    from_date, to_date = pick_date_range(args)
    preprocess_articles(from_date, to_date)

  elif cmd == "features": 
    usage()

  elif cmd == "cluster": 
    usage()

  elif cmd == "dump":
    ElasticSnapper().dump()

  elif cmd == "import":
    ElasticSnapper().reimport()

  elif cmd == "count":
    do_count()

  else:
    usage()

def do_count():
  es = EsSearcher()
  article_count = es.count_all("article")
  preped_article_count = es.count_all("article", {"match" : { "preprocessed" : True}})
  print("article count:",article_count)
  print("preped article count:",preped_article_count)
  print("missing:", article_count - preped_article_count)

def pick_date_range(args):
  if not args or len(args) > 2:
    return None, None
  if len(args) == 1:
    return args[0], None
  elif len(args) == 2:
    return args[0], args[1]

def consolify():
  cmd, args = None, []
  if len(sys.argv) > 1:
    cmd = sys.argv[1]
    if len(sys.argv) > 2:
      args = [x.lower().strip() for x in sys.argv[2:] if x]
  return cmd, args


if __name__ == "__main__":
  cmd, args = consolify()
  blaster_facade(cmd, args)

