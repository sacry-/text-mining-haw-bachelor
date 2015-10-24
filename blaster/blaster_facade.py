from utils import shell_tools
from utils import Logger
from utils import ElasticSnapper

from scraping_facade import download_and_persist_sources
from preprocessing_facade import preprocess_articles
from es import check_es_is_up
from stats import diff_count


logger = Logger("blaster").getLogger()

def usage():
  description = "Process newspaper articles and cluster them with blaster!"
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
  shell_tools.to_shell(description, cmds)

def blaster_facade(cmd, args):

  logger.info("{} with: {}".format(cmd, args))
  if cmd == "scrape": 
    check_es_is_up()
    download_and_persist_sources()

  elif cmd == "preprocess": 
    check_es_is_up()
    from_date, to_date = shell_tools.pick_date_range(args)
    preprocess_articles(from_date, to_date)

  elif cmd == "features": 
    usage()

  elif cmd == "cluster": 
    usage()

  elif cmd == "dump":
    check_es_is_up()
    ElasticSnapper().dump()

  elif cmd == "import":
    check_es_is_up()
    ElasticSnapper().reimport()

  elif cmd == "count":
    check_es_is_up()
    diff_count()

  else:
    usage()


if __name__ == "__main__":
  cmd, args = shell_tools.consolify()
  blaster_facade(cmd, args)

