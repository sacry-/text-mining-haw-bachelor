import os
import sys
from logger import Logger


logger = Logger("blaster").getLogger()

def blaster_facade(cmd, args):
  if cmd == "scrape": 
    logger.info("scrape")
    scrape()

  elif cmd == "preprocess": 
    logger.info("preprocess")
    preprocess(args)

  elif cmd == "features": 
    logger.error("features")
    features()

  elif cmd == "cluster": 
    logger.error("cluster")
    cluster()

  elif cmd == "summarize": 
    logger.error("summarize")
    summarize()

  elif cmd in ["dump", "import"]:
    dump_or_import(cmd)

  else:
    not_available(cmd, args)


def scrape():
  from scraper_factory import download_papers_from_sources

  download_papers_from_sources()


def preprocess(args):
  from preprocess_factory import preprocess_articles

  from_date, to_date = preprocess_mode(args)

  preprocess_articles(from_date, to_date)


def preprocess_mode(args):
  if not args:
    return None, None

  from utils import date_today

  if args[0] == "all":
    return "all", None

  elif args[0] == "at":
    date = args[1]
    return date, None

  elif args[0] == "from":
    from_date = args[1]
    if args[2] == "to":
      to_date = None
      if args[3] == "now":
        to_date = date_today()
      else:
        to_date = args[3]
      print("from:",from_date,"to:",to_date)
      return from_date, to_date

  return None, None


def features():
  not_implemented("features")

def cluster():
  not_implemented("cluster")

def summarize():
  not_implemented("summarize")


def dump_or_import(cmd):
  from elastic import Elastic

  if cmd == "dump":
    Elastic().dump_all()

  elif cmd == "import":
    Elastic().import_all()


# System stuff
def not_implemented(cmd):
  print("{func} not implemented!".format(func=cmd))

def not_available(cmd, tail):
  out = "Command invalid: {command} -> {args}".format(command=cmd, args=tail)
  print(out)
  logger.error(out)

def consolify(args):
  head, tail = None, []
  if len(sys.argv) >= 1:
    args = [x.lower().strip() for x in args if x]
    head = args[0]
    if len(sys.argv) > 1:
      tail = args[1:]
  return head, tail


if __name__ == "__main__":
  head, tail = consolify(sys.argv[1:])
  blaster_facade(head, tail)

  