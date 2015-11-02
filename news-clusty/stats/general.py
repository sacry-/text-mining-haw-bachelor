from es import EsSearcher

def diff_count():
  es = EsSearcher()
  article_count = es.count_all("article")
  preped_article_count = es.count_all("article", {"match" : { "preprocessed" : True}})
  print("article count:",article_count)
  print("preped article count:",preped_article_count)
  print("missing:", article_count - preped_article_count)