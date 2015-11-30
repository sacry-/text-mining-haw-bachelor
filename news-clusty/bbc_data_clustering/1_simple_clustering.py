from __future__ import division

from data_view import BBCDocuments
from data_view import BBCData

from io_utils import plot
from io_utils import print_clusters
from io_utils import print_measure

import logging
import numpy as np

from features import count_vector
from features import tfidf_vector
from features import hash_vector

from features import lsa
from features import pca

from clustering import silhouette
from collections import Counter
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics.pairwise import euclidean_distances

from clustering import birch
from clustering import kmeans
from clustering import ward_linkage
from clustering import dbscan
from clustering import mean_shift
from clustering import spectral
from clustering import affinity_propagation


def get_algo(algorithm_id=0):
  return {
    0 : ("K-Means", kmeans),
    1 : ("Ward Agglomerative", ward_linkage),
    2 : ("Birch", birch),
    3 : ("DBSCAN", dbscan),
    4 : ("Mean Shift", mean_shift),
    5 : ("Spectral", spectral),
    6 : ("Affinity Propagation", affinity_propagation)
  }[ algorithm_id ]



def setup_data(bbc_data):
  X = bbc_data.X()
  X, vsmodel = tfidf_vector( X, ngram=(1,2), max_df=0.99, min_df=1 )
  print("X: {}".format(X.shape))

  y = bbc_data.y()
  print("y: {}".format(len(y)))

  X_test = bbc_data.X_test()
  X_test = vsmodel.transform(X_test)
  print("X_test: {}".format(X_test.shape))
  y_test = bbc_data.y_test()
  print("y_test: {}".format(len(y_test)))

  return X, y, X_test, y_test


def mplot(x_train, n_clusters, algo_name):
  dim = 2
  x_red, _ = pca(x_train, dim)

  centroids, c, k = algorithm(
    x_red, 
    n_clusters=n_clusters
  )

  plot(x_red, centroids, c, k, algo_name, dim)


if __name__ == "__main__":
  logging.basicConfig(format='%(asctime)s %(message)s', level=logging.INFO)

  (algo_name, algorithm) = get_algo(algorithm_id=0)

  # Data
  bbc = BBCDocuments()
  bbc_data = BBCData( bbc, percent=0.4 )

  ids = {idx: bbc.categories()[_id] for idx, _id in enumerate(bbc_data.index_train)}

  X, y, X_test, y_test = setup_data(bbc_data)

  # x_train = euclidean_distances(X)
  n_clusters = 5

  print(X.shape)

  # mplot(x_train, n_clusters, algo_name)

  X, _ = lsa( X, 300 )
  centroids, c, k = algorithm(
    X, 
    n_clusters=n_clusters
  )

  if ids: 
    print_clusters(c, ids)

  print_measure(algo_name, "silhouette", silhouette(X, c))





