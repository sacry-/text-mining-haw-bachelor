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


def preprocess(args=None):
  from preprocessor import preprocess

  from_date, to_date = mode(args)

  articles = []
  if from_date and not to_date:
    if from_date == "all":
      print("get_all_articles()")
    else:
      print("get_articles_at_date(from_date)")
  elif from_date and to_date:
    print("get_articles(from_date, to_date)")

  for article in articles:
    prep = preprocess( article.text )

    postags = prep.pos_tags()
    nertags = prep.ner_extract()
    aptags = prep.noun_phrases()

    print("should persist it here")

  logger.info("preprocess finished")


def mode(args):
  date, from_date, to_date = None, None, None

  if args[0] == "at":
    date = args[1]

  elif args[0] == "all":
    date = "all"

  elif args[0] == "from":
    from_date = args[1]
    if args[2] == "to":
      if args[3] == "now":
        to_date = "now"
      else:
        to_date = args[3]

  elif args[0] == "start":
    from_date = "start"
    if args[1] == "to":
      to_date = args[2]

  if date:
    return date, None

  elif from_date and to_date:
    return from_date, to_date

  return None, None



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


