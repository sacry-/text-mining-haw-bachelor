import os
import sys
from logger import Logger


logger = Logger("blaster").getLogger()

def not_implemented(cmd):
  print("{func} not implemented!".format(func=cmd))

def blaster_facade(cmd, tail):
  if cmd == "scrape": 
    scrape()
  elif cmd == "preprocess": 
    preprocess()
  elif cmd == "features": 
    features()
  elif cmd == "cluster": 
    cluster()
  elif cmd == "summarize": 
    summarize()
  else: 
    not_avaliable(cmd, tail)


def scrape(cmd="scrape"):
  from scraper_factory import download_papers_from_sources

  logger.info(cmd)

  download_papers_from_sources()


def preprocess(cmd="preprocess"):
  from preprocessor import preprocess
  '''
    flags = --overwrite | --dry | --allow-collisions
    mode = all | from date to now| start to date | from date to date | at date
    articles = get_articles(mode)
    for article in articles:
      tokens = tokenize( article.text )
      postags = tag( tokens )
      nertags = ner_tag( tokens )
      aptags = ap_tag( tokens )
      persist( article, tokens, postags, nertags, aptags )
  '''
  not_implemented(cmd)
  logger.error(cmd)


def features(cmd="features"):
  not_implemented(cmd)
  logger.error(cmd)


def cluster(cmd="cluster"):
  not_implemented(cmd)
  logger.error(cmd)


def summarize(cmd="summarize"):
  not_implemented(cmd)
  logger.error(cmd)


def not_avaliable(cmd, tail):
  out = "Command invalid: {command} -> {args}".format(command=cmd, args=tail)
  print(out)
  logger.error(out)


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
  blaster_facade(head, tail)


