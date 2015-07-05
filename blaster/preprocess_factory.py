from preprocessor import preprocess
from essearcher import EsSearcher


def preprocess_articles(from_date, to_date):
  articles = fetch_articles(from_date, to_date)

  for article in articles:
    prep = preprocess( article.text )

    postags = prep.pos_tags()
    nertags = prep.ner_extract()
    aptags = prep.noun_phrases()

    persist_prep(prep)

def fetch_articles(from_date, to_date):
  searcher = EsSearcher()

  articles = []
  if from_date and not to_date:
    if from_date == "all":
      articles = searcher.all_articles()
    else:
      articles = searcher.articles_for_date(from_date)
  elif from_date and to_date:
    articles = searcher.articles_from_to(from_date, to_date)

  return articles


def persist_prep(prep):


  return False
