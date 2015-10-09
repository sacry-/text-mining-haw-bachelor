import hashlib

from prepare import Prepare

from es import EsSearcher
from langdetect import detect
from gensim import corpora, models, similarities
from nltk import data
from nltk import FreqDist
from pprint import pprint


def flatten(seq):
  return sum(seq,[])

def unique(seq):
  return list(set(seq))

def md5_hex(seq):
  s = "".join(seq)
  return hashlib.md5(s.encode('utf-8')).hexdigest()

SENTENCE_DETECTOR = data.load('tokenizers/punkt/english.pickle')
def dtokenize(sent):
  sentences = []
  for sentence in SENTENCE_DETECTOR.tokenize(doc):
    try:
      if detect(sentence) == "en":
        sentences += stokenize(sentence)
    except:
      pass
  return sentences

def ctokenize(docs):
  docs_ = []
  for doc in docs:
    docs_.append( stokenize(doc) )
  return docs_

# "20150719"
def get_docs():
  searcher = EsSearcher()
  documents = []
  noun_phrases = {}
  article_names = {}
  for article in searcher.articles_from_to("20150629", "20150701"):
    nps = searcher.nps_for_index(article._index, article.meta.id)

    noun_tokens = flatten([Prepare(np).tokens() for np in nps])
    title_tokens = Prepare(article.title).tokens()
    unique_tokens = unique(noun_tokens + title_tokens)
    md5_article = md5_hex(unique_tokens)

    noun_phrases[article.title] = unique_tokens
    article_names[md5_article] = article.title
    documents.append(unique_tokens)

  return documents, noun_phrases, article_names

def highest_n_matches(tfidf, dictionary, index, title, n=10):
  doc = Prepare(title).tokens()
  vec = dictionary.doc2bow(doc)
  step = tfidf[vec]
  sims = index[step]
  assorted = sorted(list(enumerate(sims)), key=lambda x: -x[1])
  for (idx, score) in assorted[:10]:
    yield articles[md5_hex(documents[idx])]

def setup(documents):
  sents = flatten(documents)
  freqs = FreqDist(sents)
  freq_sents = [[token for token in text if freqs[token] > 1] for text in documents]

  dictionary = corpora.Dictionary(freq_sents)
  dictionary.save('/tmp/20150629.dict')

  corpus = [dictionary.doc2bow(text) for text in freq_sents if text]
  corpora.MmCorpus.serialize('/tmp/20150629.mm', corpus)

  return corpus, dictionary

if __name__ == "__main__": 
  documents, nps, articles = get_docs()
  corpus, dictionary = setup(documents)

  tfidf = models.TfidfModel(corpus)
  index = similarities.MatrixSimilarity(tfidf[corpus], num_features=1000000)

  k = "More than 100 asylum seekers to walk free after detention system quashed"
  matches = highest_n_matches(tfidf, dictionary, index, k, 5)
  pprint( list(matches) )




