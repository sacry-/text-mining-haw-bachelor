from utils import shell_tools
from utils import Logger
from utils import ElasticSnapper

from es import check_es_is_up

from scraping_facade import download_and_persist_sources
from preprocessing_facade import preprocess_articles
from features_facade import features_to_cache

from stats import cat_indices


logger = Logger("news-clusty").getLogger()

def usage():
  description = "Process newspaper articles and cluster them with news-clusty!"
  cmds = [
    ["(--help | -h)", ["prints this summary"]],
    ["scrape", ["for scraping newspapers defined in scraping.papers"]],
    ["preprocess (None|from_date|from_date to_date)", ["for preprocessing articles from to a time period, or all if none provided", "e.g. news-clusty preprocess 20150712 20150716"]],
    ["features", ["create features for articles (not implemented)"]],
    ["cluster", ["cluster preprocessed articles (not implemented)"]],
    ["optimize", ["optimize clustering parameters with respect to a cost function (not implemented)"]],
    ["dump", ["dumps all articles persisted in elasticsearch to a json document"]],
    ["import", ["imports all articles from a JSON into elasticsearch"]],
    ["count index (None|from_date|to_date)", ["no args = general overview, from and to_date for counting each indice"]],
  ]
  shell_tools.to_shell(description, cmds)

def news_clusty_facade(cmd, args):

  logger.info("{} with: {}".format(cmd, args))
  if cmd == "scrape": 
    check_es_is_up()
    download_and_persist_sources()

  elif cmd == "preprocess": 
    check_es_is_up()
    from_date, to_date = shell_tools.pick_date_range(args)
    preprocess_articles(from_date, to_date)

  elif cmd == "features": 
    check_es_is_up()
    from_date, to_date = shell_tools.pick_date_range(args)
    features_to_cache(from_date, to_date)

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
    doctype = args[0] if len(args) >= 1 else "article"
    from_date = args[1] if len(args) >= 2 else None
    to_date = args[2] if len(args) >= 3 else None
    
    cat_indices(from_date, _to=to_date, doctype=doctype)

  else:
    usage()


if __name__ == "__main__":
  cmd, args = shell_tools.consolify()
  news_clusty_facade(cmd, args)

