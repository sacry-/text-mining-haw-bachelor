import logging

import numpy as np

from sklearn.cluster import KMeans
from clustering import cluster_plot_2d
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


def do_lda(features):

  features_as_list = sorted(features.items(), key=lambda x: x[0])
  
  for index, feature in features_as_list:
    n_topics = int( len(feature) / 10 ) + 1

    lda_path = '/tmp/{}_lda.gensim'.format( index )

    corpus_lda = None

    try:
      corpus_lda = models.LdaModel.load( lda_path )
    except:
      print("no corpus_lda found for: {}".format( lda_path ))

    if not corpus_lda:
      print( "  creating..." )

      sents = flatten( feature )
      freqs = FreqDist(sents)
      freq_sents = [[token for token in text if freqs[token] > 1] 
                    for text in feature]

      dictionary = corpora.Dictionary(freq_sents)
      dictionary.save('/tmp/{}_dict.dict'.format( index ))

      corpus = [dictionary.doc2bow(text) for text in freq_sents if text]
      corpora.MmCorpus.serialize('/tmp/{}_corpus.mm'.format( index ), corpus)

      tfidf = models.TfidfModel(corpus, normalize=True)
      corpus_tfidf = tfidf[corpus]

      lda = models.LdaModel(corpus_tfidf, id2word=dictionary, num_topics=n_topics, eval_every=3)
      corpus_lda = lda[corpus_tfidf]
      corpus_lda.save( lda_path )

    yield matutils.corpus2dense(corpus_lda, num_terms=n_topics, dtype=np.float32).T


def cluster(x, dims=2, num_clusters=1):
  x = reduce_dimensions(x, dims)
  km = KMeans(init='k-means++',n_clusters=num_clusters, max_iter=40, n_init=20, copy_x=True)
  km.fit(x)
  centroids = km.cluster_centers_
  c = km.labels_
  k = km.n_clusters
  cluster_plot_2d(x, centroids, c, k)


if __name__ == "__main__":
  s_index = "20150701"
  e_index = "20150703"
  features = extract_features(s_index, e_index)

  for x in do_lda(features):
    print("sims#shape", x.shape)
    cluster(x, 2, x.shape[1])


