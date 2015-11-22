import logging
import numpy as np

from collections import defaultdict


from clustering import cluster_plot_2d
from clustering import cluster_plot_3d
from clustering import print_clusters

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
from features import factor_analysis
from features import nmf
from features import lsa
from features import lda


def print_measure(cluster_algo_name, measure_name, measure):
  print( "-"*40, "\n", cluster_algo_name, "-", measure_name, "-", measure, "\n","-"*40 )

def plot(x_red, centroids, c, k, cluster_algo_name, dim):
  if dim == 2:
    cluster_plot_2d(x_red, centroids, c, k, cluster_algo_name)
  else:
    cluster_plot_3d(x_red, centroids, c, k, cluster_algo_name)

def print_top_words(model, feature_names, n_top_words):
  for topic_idx, topic in enumerate(model.components_):
    print("Topic #%d:" % topic_idx)
    print(" ".join([feature_names[i] for i in topic.argsort()[:-n_top_words - 1:-1]]))
  print()

# Main
def pick_algo(a_index):
  return {
    0 : ("K-Means", kmeans, 1),
    1 : ("Ward Agglomerative", ward_linkage, 1),
    2 : ("Birch", birch, 1),
    3 : ("DBSCAN", dbscan, 0),
    4 : ("Mean Shift", mean_shift, 0),
    5 : ("Spectral", spectral, 1),
    6 : ("Affinity Propagation", affinity_propagation, 0)
  }[a_index]


def pre_cluster_strategy(ffeatures, n_topics, dim):
  x, vsmodel = tfidf( 
    ffeatures, 
    ngram=(1,2),
    max_df=0.99, 
    min_df=1
  )

  topic_model = None
  x, topic_model = lsa( x, n_topics )
  # if topic_model:
  #  print_top_words( topic_model, vsmodel.get_feature_names(), 30 )

  x_red, _ = factor_analysis(x, dim)

  return x_red, vsmodel, topic_model


def cluster_it(ffeatures, name_algo, n_topics, dim, n_clusters):
  (cluster_algo_name, clusterer, has_args) = name_algo
  
  x_red, vsmodel, topic_model = pre_cluster_strategy(
    ffeatures, n_topics, dim
  )

  if has_args:
    centroids, c, k = clusterer(x_red, n_clusters)

  else:
    centroids, c, k = clusterer(x_red)

  print_measure(cluster_algo_name, "silhouette", silhouette(x_red, c))

  return x_red, centroids, c, k


def run_algo(ffeatures, fids, a_index):
  name_algo = (cluster_algo_name, _, _) = pick_algo( a_index )
  
  print( "-"*40, "\n", cluster_algo_name, "\n", "-"*40 )

  n_topics=100
  dim=2
  n_clusters=15
  
  x_red, centroids, c, k = cluster_it(ffeatures, 
                                    name_algo, 
                                    n_topics=n_topics, 
                                    dim=dim, 
                                    n_clusters=n_clusters)

  plot(x_red, centroids, c, k, cluster_algo_name, dim)
  if fids: print_clusters(c, fids, threshold=1)
  print_measure(cluster_algo_name, "silhouette", silhouette(x_red, c))


def cluster_main(_from="20151113", _to="20151114"):
  ffeatures, fids = flattened_features( 
    _from, _to
  )
  run_algo( ffeatures, fids, 0 )

if __name__ == "__main__":
  cluster_main("20151113", "20151114")


