import logging

import numpy as np

from clustering import cluster_plot_2d
from clustering import cluster_plot_3d
from clustering import kmeans

from features import indexed_features
from features import single_lda
from features import consecutive_lda
from features import pca
from features import create_corpus


if __name__ == "__main__":
  s_index = "20150701"
  e_index = "20150702"
  features_as_list, ids = indexed_features(s_index, e_index)
 
  n_topics = 0
  all_features = []
  for index, feature in features_as_list:
    all_features += feature
    round_topics = int( len(feature) / 25 ) + 1
    n_topics += round_topics

  dictionary, corpus = create_corpus(index, all_features)
  x, lda_model, lda_corpus = single_lda("20150703", corpus, dictionary, n_topics)

  x = pca(x, 2)
  centroids, c, k = kmeans(x, n_topics)
  cluster_plot_2d(x, centroids, c, k)

  clusters = {}
  for idx, el in enumerate(c):
    if not el in clusters:
      clusters[el] = []
    clusters[el].append( idx )

  for key, doc in clusters.items():
    for _id in doc[:5]:
      print(_id)
    print("-"*40)

