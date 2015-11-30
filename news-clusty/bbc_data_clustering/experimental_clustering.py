from __future__ import division

from data_view import BBCDocuments
from data_view import BBCData

from io_utils import plot
from io_utils import print_clusters
from io_utils import print_measure

from sklearn.preprocessing import scale, normalize
from sklearn.metrics import f1_score

import logging
import numpy as np

from features import count_vector
from features import tfidf_vector
from features import hash_vector

from features import lsa
from features import lda
from features import pca

from clustering import silhouette
from collections import Counter, defaultdict
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
  X, vsmodel = tfidf_vector( X, ngram=(1,1), max_df=0.8, min_df=3 )
  print("X: {}".format(X.shape))

  y = bbc_data.y()
  print("y: {}".format(len(y)))

  X_test = bbc_data.X_test()
  X_test = vsmodel.transform(X_test)
  print("X_test: {}".format(X_test.shape))
  y_test = bbc_data.y_test()
  print("y_test: {}".format(len(y_test)))

  return X, y, X_test, y_test


if __name__ == "__main__":
  logging.basicConfig(format='%(asctime)s %(message)s', level=logging.INFO)

  (algo_name, algorithm) = get_algo(algorithm_id=1)

  # Data
  bbc = BBCDocuments()
  bbc_data = BBCData( bbc, percent=0.8 )

  ids = {idx: bbc.categories()[_id] for idx, _id in enumerate(bbc_data.index_train)}

  X, y, X_test, y_test = setup_data(bbc_data)

  n_clusters = 8

  print(X.shape)

  x_train, _ = lsa( X, int(X.shape[1] / 36) )
  x_train = cosine_similarity(x_train)
  x_train = normalize(x_train)
  centroids, c, k = algorithm(
    x_train, 
    n_clusters=n_clusters
  )

  r = defaultdict(list)
  for idx, assign in enumerate(c):
    r[assign].append( ids[idx] )

  t, f = 0, 0
  centroid_map = {k: Counter(v) for k, v in r.items()}
  new_map = defaultdict(dict)
  for k, v in centroid_map.items():
    max_sort = sorted(v.items(), key=lambda x: -x[1])
    s = [b for _, b in max_sort]
    t += s[0]
    f += sum(s[1:])
    new_map[max_sort[0][0]].update(centroid_map[k])

  if False:
    for k,v in new_map.items():
      max_sort = sorted(v.items(), key=lambda x: -x[1])
      s = [b for _, b in max_sort]
      t_ = s[0]
      f_ = sum(s[1:])
      print(k, ": {}%".format((t_ / (t_ + f_))* 100), sorted(v.items(), key=lambda x: -x[1]))

  # f1 = f1_score(t, f, average=None)
  print("accuracy: {}%".format((t / (t + f))* 100))
  print_measure(algo_name, "silhouette", silhouette(X, c))





