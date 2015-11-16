import argparse

from utils import Logger
from utils import ElasticSnapper

from es import check_es_is_up


logger = Logger("news-clusty").getLogger()


def main():
  parser = argparse.ArgumentParser(
    description="Process newspaper articles and cluster them with news-clusty!"
  )
  sub_parser = parser.add_subparsers()

  sub_parser.add_parser(
    "scrape", help="for scraping newspapers defined in scraping.papers", 
  )

  count_parser = sub_parser.add_parser(
    "count", help="no args = general overview, from and to_date for counting each indice"
  )
  count_parser.add_argument(
    "index", help="give an index e.g. article or prep", default="article"
  )
  count_parser.add_argument(
    "from_date", help="a date in form of 20150712", default="20150701"
  )
  count_parser.add_argument(
    "to_date", help="a date in form of 20150716 >= 'from_date'", default="20150702"
  )

  args = parser.parse_args()
  print( args.index, args.from_date, args.to_date )

if __name__ == "__main__":
  main()

