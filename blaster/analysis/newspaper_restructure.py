import newspaper


class Source():

  def __init__(self, name="", base_url="", memoize=True, whitelist=[]):
    self.name = name
    self.base_url = base_url
    self.memoize = memoize
    self.whitelist = whitelist
    self.builds = []

  def build(self):
    print(self)

    for (topics, category_name) in self.categories():
      for (url, topic) in topics:
        print( "building {} : {}".format(self.name, url) )
        paper = newspaper.build(url, 
                            language='en', 
                            memoize_articles=self.memoize)
        size = len(paper.articles)
        print( "total articles: {} for {}".format(size, self.name) )
        self.builds.append( paper )

  def __repr__(self):
    accu = []
    accu.append( "name: {}".format(self.name) )
    accu.append( "base_url: {}".format(self.base_url) )
    accu.append( "memoize: {}".format(self.memoize) )
    accu.append( "whitelist: {}".format(self.whitelist) )
    for (topics, category_name) in self.categories():
      accu.append( "category: {}".format(category_name) )
      for (url, topic) in topics:
        accu.append( "   {}, {}".format(topic, url) )
    return "\n".join(accu)


class Guardian():

  def __init__(self):
    self.base_url = "http://www.theguardian.com"
 
  def categories(self):
    yield ( self.politics(), "politics" )
    yield ( self.economics(), "economics" )
    yield ( self.environment(), "environment" )

  def politics(self):
    return self.expand([
      ("world", "politics-global"),
      ("world/europe-news", "politics-europe"),
      ("us-news", "politics-us"),
      ("world/asia", "politics-asia"),
      ("australia-news", "politics-australia"),
      ("world/africa", "politics-africa"),
      ("world/middleeast", "politics-middleeast"),
      ("cities", "politics-cities"),
      ("global-development", "politics-development"),
      ("world/americas", "politics-americas")
    ])

  def economics(self):
    return self.expand([
      ("uk/business", "economics-uk"),
      ("business/economics", "economics"),
      ("business/banking", "economics-banking"),
      ("business/retail", "economics-retail"),
      ("business/markets", "economics-markets"),
      ("business/eurozone", "economics-eurozone")
    ])

  def environment(self):
    return self.expand([
      ("uk/environment", "environment-uk"),
      ("environment/climate-change", "environment-climate-change"),
      ("environment/wildlife", "environment-wildlife"),
      ("environment/energy", "environment-energy"),
      ("environment/pollution", "environment-pollution"),
    ])

  def expand(self, seq):
    for (url_head, category) in seq:
      url = "{}/{}".format(self.base_url, url_head)
      yield (url, category)


if __name__ == "__main__":
  s = Guardian()
  paper = newspaper.build("http://www.theguardian.com", 
                          language='en', 
                          memoize_articles=False)
  size = len(paper.articles)
  for article in paper.article_urls():
    print(article)
  print( "total articles: {}".format(size) )


  
