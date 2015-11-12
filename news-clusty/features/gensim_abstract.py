import numpy as np
import logging

from gensim import matutils
from gensim import similarities
from gensim import models
from gensim import corpora

from nltk import data
from nltk import FreqDist

from utils.helpers import unique
from utils.helpers import flatten



def create_corpus(index, features):
  dict_path = '/tmp/{}_dict.dict'.format( index )
  corpus_path_tfidf = '/tmp/{}_corpus_tfidf.mm'.format( index )

  dictionary = None
  corpus_tfidf = None
  try:
    dictionary = corpora.Dictionary.load(dict_path)
    corpus_tfidf = corpora.MmCorpus.load(corpus_path_tfidf)
    return dictionary, corpus_tfidf
  except:
    print( "no corpus or dictionary found, creating..." )

  sents = flatten( features )
  freqs = FreqDist(sents)
  freq_sents = [[token for token in text if freqs[token] > 1] 
                for text in features]

  dictionary = corpora.Dictionary(freq_sents)
  dictionary.filter_extremes(no_below=1, no_above=0.8)
  dictionary.save( dict_path )

  corpus = [dictionary.doc2bow(text) for text in freq_sents if text]
  corpora.MmCorpus.serialize('/tmp/{}_corpus.mm'.format( index ), corpus)

  tfidf = models.TfidfModel(corpus, normalize=True)
  corpus_tfidf = tfidf[corpus]
  corpus_tfidf.save( corpus_path_tfidf )

  return dictionary, corpus_tfidf


def single_lda(index, corpus, dictionary, n_topics):
  lda_path = "/tmp/{}.gensim".format( index )
  lda_model = None
  lda_corpus = None

  try:
    lda_model = models.LdaModel.load( lda_path )
    lda_corpus = lda_model[corpus]

  except:
    print("no corpus_lda found for: {}".format( lda_path ))
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    lda_model = models.LdaModel(corpus, id2word=dictionary, num_topics=n_topics, iterations=100, update_every=0, passes=10)
    lda_model.save( lda_path )
    lda_corpus = lda_model[corpus]
  
  x = to_ndarray( lda_corpus, n_topics )
  return x, lda_model, lda_corpus


def consecutive_lda(features_as_list):
  for index, features in features_as_list:
    dictionary, corpus_tfidf = create_corpus(index, features)
    n_topics = int( len(features) / 10 ) + 1
    x, lda_model, lda_corpus = single_lda(index, corpus_tfidf, dictionary, n_topics)
    yield (x, lda_model, lda_corpus, corpus_tfidf, dictionary)


def to_ndarray(corpus_lda, n_topics):
  return matutils.corpus2dense(corpus_lda, num_terms=n_topics, dtype=np.float32).T

# TODO:
def print_lda_with_id(lda_model, doc, _id):
  print(_id)
  bow = dictionary.doc2bow(doc)
  some_docs = lda_model.get_document_topics(bow, minimum_probability=0.1)
  for doc, sim in sorted(some_docs, key=lambda x: -x[1]):
    print( lda_model.print_topic(doc, topn=10) )
    print("  sim:", sim)
  print("-"*40)


if __name__ == "__main__":
  pass



