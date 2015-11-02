from es import EsSearcher
from es import Elastic


def unique(seq):
  return list(set(seq))

class Guardian():

  def __init__(self):
    pass

  def flattened(self):
    for (topics, main_category) in self.categories():
      for (url, sub_topic) in topics:
        yield (main_category, sub_topic, url)

  def flat_to_tokens(self, seq):
    tokens = []
    for category in seq:
      (main_category, sub_topic, url) = category
      tokens = []
      tokens.append( main_category )
      more = sub_topic.split("-")
      tokens += more
      tokens.append( url )
    return unique(tokens)

  def categories(self):
    yield ( self.politics(), "politics" )
    yield ( self.economics(), "economics" )
    yield ( self.environment(), "environment" )

  def politics(self):
    return [
      ("world", "politics-global"),
      ("europe-news", "politics-europe"),
      ("us-news", "politics-us"),
      ("asia", "politics-asia"),
      ("australia-news", "politics-australia"),
      ("africa", "politics-africa"),
      ("middleeast", "politics-middleeast"),
      ("cities", "politics-cities"),
      ("global-development", "politics-development"),
      ("americas", "politics-americas")
    ]

  def economics(self):
    return [
      ("business", "economics"),
      ("economics", "economics"),
      ("banking", "economics-banking"),
      ("retail", "economics-retail"),
      ("markets", "economics-markets"),
      ("eurozone", "economics-eurozone")
    ]

  def environment(self):
    return [
      ("environment", "environment"),
      ("climate-change", "environment-climate-change"),
      ("wildlife", "environment-wildlife"),
      ("energy", "environment-energy"),
      ("pollution", "environment-pollution"),
    ]


if __name__ == "__main__":
  searcher = EsSearcher()
  elastic = Elastic()
  g = Guardian()

  categories = list(g.flattened())

  c, updates = 0, 0
  for article in searcher.articles_from_to("20150629", "20150719", "theguardian"):
    cats = list(filter(lambda t: t[2] in article.url, categories))
    if cats:
      tokens = g.flat_to_tokens( cats )
      script = {
        "doc": {
          "categories" : tokens
        }
      } 
      s = "self.es.update({},{},{},{})".format(
        article._index, 
        "article", 
        article._id, 
        script
      )
      # print(s)
      updates += 1
    else:
      print(article.url, article.meta_keywords )
    c += 1
  print("-"*40)
  print(c, updates)


