import os
import sys

from utils import Logger
from utils import ElasticSnapper
from scraping_facade import download_papers_from_sources
from preprocessing_facade import preprocess_articles
from termcolor import colored


logger = Logger("blaster").getLogger()

def usage():
  description = "Process newspaper articles and cluster them with blaster!"
  print("\n", colored(description, "green", attrs=["underline"]))

  cmds = [
    ["(--help | -h)", ["prints this summary"]],
    ["scrape", ["for scraping newspapers defined in your newspaper config found under 'resources'"]],
    ["preprocess (None|from_date|from_date to_date)", ["for preprocessing articles from to a time period, or all if none provided", "e.g. blaster preprocess 20150712 20150716"]],
    ["features", ["create features for articles (not implemented)"]],
    ["cluster", ["cluster preprocess articles (not implemented)"]],
    ["dump", ["dumps all articles persisted in elasticsearch to a json document"]],
    ["import", ["imports all articles from a JSON into elasticsearch"]],
  ]
  for cmd, descr in cmds:
    print("  blaster", 
      colored(cmd, "yellow"), 
      colored("\n\t" + "\n\t".join(descr), "magenta"), "\n")


def blaster_facade(cmd, args):
  if cmd == "dump":
    ElasticSnapper().dump_articles()

  elif cmd == "import":
    ElasticSnapper().import_articles()

  elif cmd == "scrape": 
    logger.info("scrape")
    download_papers_from_sources()

  elif cmd == "preprocess": 
    logger.info("preprocess")
    from_date, to_date = pick_date_range(args)
    preprocess_articles(from_date, to_date)

  elif cmd == "features": 
    usage()

  elif cmd == "cluster": 
    usage()

  else:
    usage()

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

