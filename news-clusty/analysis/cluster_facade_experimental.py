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



def pick_algo(a_index=0):
  return {
    0 : ("K-Means", kmeans),
    1 : ("Ward Agglomerative", ward_linkage),
    2 : ("Birch", birch),
    3 : ("DBSCAN", dbscan),
    4 : ("Mean Shift", mean_shift),
    5 : ("Spectral", spectral)
  }[a_index]


def run_algo(ffeatures, name_algo, n_topics=100, pca_dim=2, n_clusters=60):
  (cluster_algo_name, clusterer) = name_algo
  x = tfidf( ffeatures, ngram=(1,1), max_feat=None )
  x = lsa(x, topics=n_topics)
  x_red = pca(x, pca_dim)
  centroids, c, k = clusterer(x_red, n_clusters)

  print( silhouette(x_red, c) )
  return x_red, centroids, c, k

def process_output(x_red, centroids, c, k, cluster_algo_name, fids=None):
  cluster_plot_2d(x_red, centroids, c, k, cluster_algo_name)
  if fids:
    print_clusters(c, fids)
  print( silhouette(x_red, c) )

def simple_example():
  return np.array([
    [1,1],[1.1,1.1],
    [-1.1,-1.1],[-1,-1],
    [0,0],[0.2,0.2], 
    [1,-1],[1.2,-1.2],
    [-1,1],[-1.2,1.2]], dtype=np.float32
  )
  

if __name__ == "__main__":
  name_algo = (cluster_algo_name, _) = pick_algo( a_index=1 )

  n_topics=100
  pca_dim=2
  n_clusters=60

  ffeatures, fids = flattened_features( 
    "20150703", "20150704" 
  )
  
  x_red, centroids, c, k = run_algo(ffeatures, 
                                    name_algo, 
                                    n_topics=100, 
                                    pca_dim=2, 
                                    n_clusters=60)

  process_output(x_red, centroids, c, k, cluster_algo_name, fids)



