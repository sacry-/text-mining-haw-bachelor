import newspaper

from utils.helpers import timeit
from utils.logger import Logger


logger = Logger(__name__).getLogger()


class Source():

  def __init__(self, name, url, memoize=True, whitelist=[]):
    self.name = name
    self.url = url
    self.memoize = memoize
    self.whitelist = whitelist
    self.paper = None
    self.size = 0

  @timeit
  def build(self):
    s = "building {} : {}".format(self.name, self.url)
    print(s)
    logger.info(s)
    self.paper = newspaper.build(self.url, 
                            language='en', 
                            memoize_articles=self.memoize)
    self.size = len(self.paper.articles)
    s = "total articles: {} for {}".format(self.size, self.name)
    print(s)
    logger.info(s)


if __name__ == "__main__":
  pass


