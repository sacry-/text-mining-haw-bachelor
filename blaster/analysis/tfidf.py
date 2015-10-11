import hashlib
import random

from prepare import Prepare

from es import EsSearcher
from es import Elastic
from gensim import corpora, models, similarities
from nltk import data
from nltk import FreqDist
from pprint import pprint
from utils.helpers import timeit


def flatten(seq):
  return sum(seq,[])

def unique(seq):
  return list(set(seq))

def md5_hex(seq):
  s = "".join(seq)
  return hashlib.md5(s.encode('utf-8')).hexdigest()


class TfIdf():

  def __init__(self, from_, to_="20150719", paper=None):
    self.from_ = from_
    self.to_ = to_
    self.paper = paper
    self.documents = None
    self.articles = None
    self.nps = None
    self.corpus = None
    self.dictionary = None
    self.tfidf = None
    self.index = None

  def run(self):
    self.__get_docs__()
    self.__init_corpus__()
    self.tfidf = models.TfidfModel(self.corpus)
    self.index = similarities.MatrixSimilarity(self.tfidf[self.corpus], num_features=1000000)

  def search_space(self, title, n=10, threshold=0.0):
    doc = Prepare(title).tokens()
    vec = self.dictionary.doc2bow(doc)
    sims = self.index[self.tfidf[vec]]
    sorted_space = sorted(list(enumerate(sims)), key=lambda x: -x[1])
    for (idx, score) in sorted_space[:n]:
      if score <= threshold:
        break
      yield (self.articles[md5_hex(self.documents[idx])], score)

  def __get_docs__(self):
    searcher = EsSearcher()
    documents = []
    noun_phrases = {}
    article_names = {}
    for article in searcher.articles_from_to(self.from_, self.to_, self.paper):
      nps = searcher.nps_for_index(article._index, article.meta.id)

      noun_tokens = flatten([Prepare(np).tokens() for np in nps])
      title_tokens = Prepare(article.title).tokens()
      unique_tokens = unique(noun_tokens + title_tokens)
      md5_article = md5_hex(unique_tokens)

      noun_phrases[article.title] = unique_tokens
      article_names[md5_article] = article.title
      documents.append(unique_tokens)

    self.documents = documents
    self.articles = article_names
    self.nps = noun_phrases

  def __init_corpus__(self):
    sents = flatten(self.documents)
    freqs = FreqDist(sents)
    freq_sents = [[token for token in text if freqs[token] > 1] 
                  for text in self.documents]

    dictionary = corpora.Dictionary(freq_sents)
    dictionary.save('/tmp/20150629.dict')

    corpus = [dictionary.doc2bow(text) for text in freq_sents if text]
    corpora.MmCorpus.serialize('/tmp/20150629.mm', corpus)

    self.dictionary = dictionary
    self.corpus = corpus


def collect_indices(indices, collected, k):
  if k > len(indices):
    collected += indices
    return collect_indices(indices, collected, k - len(indices))
  elif k == 0:
    return collected
  else:
    return (collected + random.sample( indices, k ))

def pick_k_random_articles(_from, _to, k=10):
  elastic = Elastic()
  searcher = EsSearcher()
  all_indices = list( elastic.all_indices() )
  f = all_indices.index(_from)
  t = all_indices.index(_to)
  indices = all_indices[f:t]
  picked = collect_indices(indices, [], k)
  return searcher.choose_k(picked)


@timeit
def run():
  _from, _to = "20150629", "20150705"
  tfidf = TfIdf(_from, _to)
  tfidf.run()

  titles = [
    "More than 100 asylum seekers to walk free after detention system quashed"
  ]

  seed = pick_k_random_articles(_from, _to, 10)
  for article in seed:
    print(article.title)
    matches = tfidf.search_space(title=article.title, n=5, threshold=0.1)
    pprint( list(matches) )
    print("-"*40)

if __name__ == "__main__": 
  run()








