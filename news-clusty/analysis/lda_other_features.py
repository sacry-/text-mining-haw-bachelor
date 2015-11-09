import logging

import numpy as np
import itertools

from sklearn.cluster import KMeans
from clustering import cluster_plot_2d
from clustering import big_clusterd_plot_2d
from clustering import cluster_plot_3d
from clustering import reduce_dimensions
from clustering import create_sample

from utils.helpers import unique
from utils.helpers import flatten
from clustering.feature_selection import get_features

from gensim import corpora, models, similarities, matutils
from nltk import data
from nltk import FreqDist
from pprint import pprint


def extract_features(s_index, e_index):
  features = {}
  for index, feature in get_features(s_index, e_index):
    if index in features:
      features[index].append( feature )
    else:
      features[index] = [ feature ]

  flattened = flatten(features.values())
  print(len(flattened))

  return features


def get_corpus(index, features):
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
  dictionary.save( dict_path )

  corpus = [dictionary.doc2bow(text) for text in freq_sents if text]
  corpora.MmCorpus.serialize('/tmp/{}_corpus.mm'.format( index ), corpus)

  tfidf = models.TfidfModel(corpus, normalize=True)
  corpus_tfidf = tfidf[corpus]
  corpus_tfidf.save( corpus_path_tfidf )

  return dictionary, corpus_tfidf


def do_lda(index, corpus, dictionary, n_topics):
  lda_path = "/tmp/{}.gensim".format( index )
  lda_model = None
  lda_corpus = None

  try:
    lda_model = models.LdaModel.load( lda_path )
    lda_corpus = lda_model[corpus]

  except:
    print("no corpus_lda found for: {}".format( lda_path ))
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    lda_model = models.LdaModel(corpus, id2word=dictionary, num_topics=n_topics, update_every=0, iterations=100, passes=25)
    lda_model.save( lda_path )
    lda_corpus = lda_model[corpus]
  
  x = convert_lda( lda_corpus, n_topics )

  return x, lda_model, lda_corpus


def convert_lda(corpus_lda, n_topics):
  return matutils.corpus2dense(corpus_lda, num_terms=n_topics, dtype=np.float32).T

def cluster(x, dims=2, num_clusters=1):
  x = reduce_dimensions(x, dims)
  km = KMeans(init='k-means++',n_clusters=num_clusters, max_iter=40, n_init=20, copy_x=True)
  km.fit(x)
  centroids = km.cluster_centers_
  c = km.labels_
  k = km.n_clusters
  return centroids, c, k

if __name__ == "__main__":
  s_index = "20150701"
  e_index = "20150710"
  features = extract_features(s_index, e_index)
  features_as_list = sorted(features.items(), key=lambda x: x[0])

  n_topics = 0
  all_features = []
  for index, feature in features_as_list:
    all_features += feature
    round_topics = int( len(feature) / 10 ) + 1
    n_topics += round_topics

  dictionary, corpus = get_corpus(index, all_features)
  x, lda_model, lda_corpus = do_lda("20150710", corpus, dictionary, n_topics)

  id2word = {k:v for k, v in lda_model.id2word.items()}

  print(id2word)


