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

from features import flattened_features
from features import term_vector
from features import tfidf
from features import pca
from features import lsa
from features import lda
from features import random_projections



def print_measure(cluster_algo_name, measure_name, measure):
  print( "-"*40, "\n", cluster_algo_name, "-", measure_name, "-", measure, "\n","-"*40 )

def process_output(x_red, centroids, c, k, cluster_algo_name, dim, fids=None):
  if dim == 2:
    cluster_plot_2d(x_red, centroids, c, k, cluster_algo_name)
  else:
    cluster_plot_3d(x_red, centroids, c, k, cluster_algo_name)
  if fids:
    print_clusters(c, fids)

  print_measure(cluster_algo_name, "silhouette", silhouette(x_red, c))

def simple_example():
  return np.array([
    [1,1],[1.1,1.1],
    [-1.1,-1.1],[-1,-1],
    [0,0],[0.2,0.2], 
    [1,-1],[1.2,-1.2],
    [-1,1],[-1.2,1.2]], dtype=np.float32
  )


# Main
def pick_algo(a_index=0):
  return {
    0 : ("K-Means", kmeans, 1),
    1 : ("Ward Agglomerative", ward_linkage, 1),
    2 : ("Birch", birch, 1),
    3 : ("DBSCAN", dbscan, 0),
    4 : ("Mean Shift", mean_shift, 0),
    5 : ("Spectral", spectral, 1)
  }[a_index]

def run_algo(ffeatures, name_algo, n_topics=100, pca_dim=2, n_clusters=60):
  (cluster_algo_name, clusterer, has_args) = name_algo
  x = term_vector( ffeatures, ngram=(1,2), max_feat=100000, max_df=0.9, min_df=0.1 )
  x = lsa( x, n_topics )
  x_red = pca(x, pca_dim)

  if has_args:
    centroids, c, k = clusterer(x_red, n_clusters)

  else:
    centroids, c, k = clusterer(x_red)

  print_measure(cluster_algo_name, "silhouette", silhouette(x_red, c))

  return x_red, centroids, c, k


def main(ffeatures, fids, a_index=0):
  name_algo = (cluster_algo_name, _, _) = pick_algo( a_index )
  
  print( "-"*40, "\n", cluster_algo_name, "\n", "-"*40 )

  n_topics=100
  pca_dim=2
  n_clusters=60
  
  x_red, centroids, c, k = run_algo(ffeatures, 
                                    name_algo, 
                                    n_topics=n_topics, 
                                    pca_dim=pca_dim, 
                                    n_clusters=n_clusters)

  process_output(x_red, centroids, c, k, cluster_algo_name, pca_dim, fids)


if __name__ == "__main__":
  ffeatures, fids = flattened_features( 
    "20150703", "20150704" 
  )
  main( ffeatures, fids, 4 )



