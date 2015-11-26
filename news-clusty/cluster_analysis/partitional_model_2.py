from __future__ import division

import logging
import numpy as np
from pickle_utils import get_sents_training

from features import count_vector
from features import tfidf_vector
from features import hash_vector

from features import lsa

from io_utils import print_clusters
from io_utils import print_measure
from io_utils import append_to_file
from io_utils import plot

from clustering import silhouette

from collections import Counter
from sklearn.metrics.pairwise import cosine_similarity

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

if __name__ == "__main__":
  logging.basicConfig(format='%(asctime)s %(message)s', level=logging.INFO)

  (algo_name, algorithm) = get_algo(algorithm_id=2)

  # Data
  model_name = "20151116"
  x_train, ids = get_sents_training( model_name )

  x_train = [" ".join(s) for s in x_train]
  x_train, _ = tfidf_vector( 
    x_train, 
    ngram=(1,2),
    max_df=0.8, 
    min_df=1
  )
  xtrain = cosine_similarity(x_train)
  n_clusters = 10

  x_train, _ = lsa(x_train, n_clusters)
  centroids, c, k = algorithm(
    x_train, 
    n_clusters=n_clusters, 
    threshold=0.5, 
    branching_factor=5
  )

  # plot(x_train, centroids, c, k, algo_name, 3)

  if ids: 
    print_clusters(c, ids)

  print_measure(algo_name, "silhouette", silhouette(x_train, c))

