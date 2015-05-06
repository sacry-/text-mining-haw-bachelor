import os, sys
import path_router
from logger import Logger

logger = Logger("blaster").getLogger()

def not_implemented(cmd):
  print("{} not implemented!".format(cmd))

def delegate(cmd, tail):

  if cmd == "scrape":
    from scraper_api import download_papers_from_sources

    logger.info("scrape")
    download_papers_from_sources()

  elif cmd == "tokenize":
    not_implemented(cmd)
    logger("tokenize")

  elif cmd == "tag":
    not_implemented(cmd)
    logger("tag")

  elif cmd == "features":
    not_implemented(cmd)
    logger("features")

  elif cmd == "cluster":
    not_implemented(cmd)
    logger("cluster")

  elif cmd == "summarize":
    not_implemented(cmd)
    logger("summarize")

  else:
    print("{} : {} currently not available!".format(cmd, tail))


def consolify(args):
  head, tail = None, []

  if len(sys.argv) > 1:
    args = [x.lower().strip() for x in args if x]
    head = args[0]

    if len(sys.argv) > 2:
      tail = args[1:]

  return head, tail


if __name__ == "__main__":
  head, tail = consolify(sys.argv[1:])
  delegate(head, tail)


