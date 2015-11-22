from utils import shell_tools
from utils import Logger
from utils import ElasticSnapper

from es import check_es_is_up


logger = Logger("news-clusty").getLogger()


def usage( args ):  
  if not "-h" in args or not "--help" in args:
    print("The command '{}' is not known!".format(cmd))
    
  description = "Download and preprocess newspaper articles and analyze their stats"
  cmds = [
    ["(--help | -h)", ["prints this summary"]],
    ["scrape", ["for scraping newspapers defined in scraping.papers"]],
    ["preprocess (None|from_date|from_date to_date)", ["for preprocessing articles from to a time period, or all if none provided", "e.g. news-clusty preprocess 20150712 20150716"]],
    ["dump", ["dumps all articles persisted in elasticsearch to a json document"]],
    ["import", ["imports all articles from a JSON into elasticsearch"]],
    ["count index (None|from_date|to_date)", ["no args = general overview, from and to_date for counting each indice"]],
  ]
  shell_tools.to_shell(description, cmds)


def news_clusty_facade(cmd, args):

  logger.info("{} with: {}".format(cmd, args))

  if cmd == "scrape": 
    from scraping_facade import download_and_persist_sources

    check_es_is_up()
    download_and_persist_sources()

  elif cmd == "preprocess": 
    from preprocessing_facade import preprocess_articles

    check_es_is_up()
    from_date, to_date = shell_tools.pick_date_range(args)
    preprocess_articles(from_date, to_date)

  elif cmd == "dump":
    check_es_is_up()
    ElasticSnapper().dump()

  elif cmd == "import":
    check_es_is_up()
    ElasticSnapper().reimport()

  elif cmd == "count":
    from stats import cat_indices
    
    check_es_is_up()
    doctype = args[0] if len(args) >= 1 else "article"
    from_date = args[1] if len(args) >= 2 else None
    to_date = args[2] if len(args) >= 3 else None
    
    cat_indices(from_date, _to=to_date, doctype=doctype)

  else:
    usage( args )

if __name__ == "__main__":
  cmd, args = shell_tools.consolify()
  news_clusty_facade(cmd, args)


