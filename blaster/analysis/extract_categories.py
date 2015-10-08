from es import EsSearcher


def unique(seq):
  return list(set(seq))

if __name__ == "__main__":
  searcher = EsSearcher()
  guardian_categories = []
  nytimes_categories = []

  for article in searcher.articles_from_to("20150629", "20150719"):
    url = article.url
    parts = article.url.split("/")

    if "theguardian" in article.url:
      try:
        category = parts[3]
        if not category in guardian_categories:
          print(article.url)
          guardian_categories.append( category )
      except:
        pass

    if "www.nytimes.com" in article.url:
      try:
        category, snd_category = parts[6], None
        if len(parts) > 9:
          snd_category = parts[7]

        if not category in nytimes_categories:
          print(article.url)
          nytimes_categories.append( category )
      except:
        pass

  print( unique( guardian_categories ) )
  print( unique( nytimes_categories ) )

