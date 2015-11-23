import logging
import numpy as np

from collections import defaultdict
from sklearn.preprocessing import normalize

from clustering import cluster_plot_2d
from clustering import cluster_plot_3d

from clustering import silhouette

from clustering import kmeans
from clustering import ward_linkage
from clustering import dbscan
from clustering import mean_shift
from clustering import birch
from clustering import spectral
from clustering import affinity_propagation


from features import flattened_features
from features import count_vector
from features import tfidf_vector
from features import hash_vector


from features import pca
from features import nmf
from features import lsa
from features import lda


from io_utils import print_clusters
from io_utils import print_measure
from io_utils import plot


# Script
from_date = "20151113"
to_date = "20151113"

algorithm_id = 2
n_clusters = 8

decomposer = [lsa, lda, nmf, None][0]
n_topics = 8

dim_reduction_method = [pca, None][0]
plot_dimension = 2


ffeatures, fids = flattened_features( 
  from_date, to_date
)

(cluster_algo_name, clusterer, has_args) = {
  0 : ("K-Means", kmeans, 1),
  1 : ("Ward Agglomerative", ward_linkage, 1),
  2 : ("Birch", birch, 0),
  3 : ("DBSCAN", dbscan, 0),
  4 : ("Mean Shift", mean_shift, 0),
  5 : ("Spectral", spectral, 1),
  6 : ("Affinity Propagation", affinity_propagation, 0)
}[ algorithm_id ]


print( "-"*40, "\n", cluster_algo_name, "\n", "-"*40 )

x, vsmodel = tfidf_vector( 
  ffeatures, 
  ngram=(1,2),
  max_df=0.8, 
  min_df=2
)
# x = normalize(x, norm='l2', axis=1)


if decomposer:
  x, topic_model = decomposer( x, n_topics )

if dim_reduction_method:
  x, _ = dim_reduction_method(x, plot_dimension)

if has_args:
  centroids, c, k = clusterer(x, n_clusters)
else:
  centroids, c, k = clusterer(x)

if dim_reduction_method:
  plot(x, centroids, c, k, cluster_algo_name, plot_dimension)

if fids: 
  print_clusters(c, fids, word="paris", threshold=3)

print_measure(cluster_algo_name, "silhouette", silhouette(x, c))











