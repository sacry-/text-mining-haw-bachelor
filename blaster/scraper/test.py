

def data_test():
  from newspaper import Article
  from data import Data
  from downloader import download_article

  b = "http://www.theguardian.com/us-news/2015/may/01/chris-christie-david-wildstein-bridgegate"
  a = Article(b)
  a = download_article(a)
  d = Data(a)
  print( d.to_h() )


def persister_test():
  from newspaper import Article
  from data import Data
  from downloader import download_article

  sp = ScraperPersister("theguardian")
  b = "http://www.theguardian.com/us-news/2015/may/01/chris-christie-david-wildstein-bridgegate"
  a = Article(b)
  a = download_article(a)
  d = Data(a)
  d.persist(sp)
  print( d.title )


if __name__ == "__main__":
  data_test()
  persister_test()
