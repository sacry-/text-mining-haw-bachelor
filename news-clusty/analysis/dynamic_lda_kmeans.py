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
  ids = {}
  for index, _id, feature in get_features(s_index, e_index):
    if index in features:
      features[index].append( feature )
      ids[index].append( _id )
    else:
      features[index] = [ feature ]
      ids[index] = [ _id ]

  flattened = flatten(features.values())
  print(len(flattened))

  return features, ids


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
  dictionary.filter_extremes(no_below=1, no_above=0.8)
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
    lda_model = models.LdaModel(corpus, id2word=dictionary, num_topics=n_topics, iterations=100, update_every=0, passes=10)
    lda_model.save( lda_path )
    lda_corpus = lda_model[corpus]
  
  x = convert_lda( lda_corpus, n_topics )

  return x, lda_model, lda_corpus


def convert_lda(corpus_lda, n_topics):
  return matutils.corpus2dense(corpus_lda, num_terms=n_topics, dtype=np.float32).T

def cluster(x, num_clusters=1):
  km = KMeans(init='k-means++',n_clusters=num_clusters, max_iter=40, n_init=20, copy_x=True)
  km.fit(x)
  centroids = km.cluster_centers_
  c = km.labels_
  k = km.n_clusters
  return centroids, c, k

def print_doc(lda_model, doc, _id):
  print(_id)
  bow = dictionary.doc2bow(doc)
  some_docs = lda_model.get_document_topics(bow, minimum_probability=0.1)
  for doc, sim in sorted(some_docs, key=lambda x: -x[1]):
    print( lda_model.print_topic(doc, topn=10) )
    print("  sim:", sim)
  print("-"*40)

if __name__ == "__main__":
  s_index = "20150701"
  e_index = "20150705"
  features, ids = extract_features(s_index, e_index)
  features_as_list = sorted(features.items(), key=lambda x: x[0])
  ids_as_list = flatten(list(map(lambda x: x[1], sorted(ids.items(), key=lambda x: x[0]))))
  
  n_topics = 0
  all_features = []
  for index, feature in features_as_list:
    all_features += feature
    round_topics = int( len(feature) / 25 ) + 1
    n_topics += round_topics

  dictionary, corpus = get_corpus(index, all_features)
  # x, lda_model, lda_corpus = do_lda("20150703", corpus, dictionary, n_topics)

  '''
  print(len(ids_as_list))
  s = 50
  for idx, doc in enumerate(all_features[s:s+3]):
    print_doc(lda_model, doc, ids_as_list[s+idx])

  '''
  print("--"*40)
  print(len(corpus))
  m = 0
  for doc in corpus:
    m = max(m, len(doc))
  x = matutils.corpus2dense(corpus, num_terms=m, dtype=np.float32).T
  # x = reduce_dimensions(x, dims)
  centroids, c, k = cluster(x, n_topics)
  # cluster_plot_2d(x, centroids, c, k)
  clusters = {}
  for idx, el in enumerate(c):
    if not el in clusters:
      clusters[el] = []
    clusters[el].append( idx )

  for key, doc in clusters.items():
    for _id in doc[:5]:
      print(_id)
    print("-"*40)

