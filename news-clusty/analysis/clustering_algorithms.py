import logging

import numpy as np

from collections import defaultdict

from clustering import cluster_plot_2d
from clustering import cluster_plot_3d
from clustering import big_clusterd_plot_2d
from clustering import reduce_dimensions

from utils.helpers import unique
from utils.helpers import flatten
from clustering.feature_selection import get_features

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import Normalizer
from sklearn.decomposition import TruncatedSVD
from sklearn.preprocessing import StandardScaler

from sklearn.cluster import AgglomerativeClustering
from sklearn.cluster import DBSCAN
from sklearn.cluster import KMeans
from sklearn.cluster import Birch

from sklearn import metrics
from sklearn.metrics import pairwise_distances


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

def unfold(data):
  return flatten(list(map(lambda x: x[1], sorted(data, key=lambda x: x[0]))))

def get_data(s_index="20150701", e_index="20150704"):
  features, ids = extract_features(s_index, e_index)
  features_as_list = list( map(lambda e: " ".join(e), unfold( features.items() )) )
  ids_as_list = unfold( ids.items() )

  return features_as_list, ids_as_list

def red(x, dim=3):
  svd = TruncatedSVD(dim)
  normalizer = Normalizer(copy=False)
  lsa = make_pipeline(svd, normalizer)

  x = lsa.fit_transform(x)

  explained_variance = svd.explained_variance_ratio_.sum()
  print("Explained variance of the SVD step: {}% and dim={}".format(
      int(explained_variance * 100), dim))

  return x

def k_means_cluster(x, num_clusters=1):
  km = KMeans(init='k-means++',n_clusters=num_clusters, n_init=20, copy_x=True)
  km.fit(x)
  centroids = km.cluster_centers_
  c = km.labels_
  k = km.n_clusters
  return centroids, c, k


def hierarch_cluster(x,num_clusters=1):
  ac = AgglomerativeClustering(n_clusters=num_clusters,
                               linkage="ward")
  ac.fit(x)
  c = ac.labels_
  k = ac.n_clusters

  return None, c, k

def birch(x):
  b = Birch(branching_factor=5, n_clusters=None, threshold=0.3, compute_labels=True)
  b.fit(x)
  centroids = b.subcluster_centers_
  c = b.labels_
  k = len(centroids)
  return centroids, c, k


def dbscan(x):
  x = StandardScaler().fit_transform(x)
  db = DBSCAN(eps=0.1, min_samples=15).fit(x)
  core_samples_mask = np.zeros_like(db.labels_, dtype=bool)
  core_samples_mask[db.core_sample_indices_] = True
  labels = db.labels_

  # Number of clusters in labels, ignoring noise if present.
  k = len(set(labels)) - (1 if -1 in labels else 0)
  return None, labels, k

def print_clusters(c, fids):
  clusters = {}
  for doc, cid in enumerate(c):
    if not cid in clusters:
      clusters[cid] = []  
    clusters[cid].append( doc )

  for cid, docs in list(clusters.items()):
    if len(docs) <= 3:
      continue
    print("Cluster {}".format(cid))
    for doc in docs:
      print(fids[doc]) 
    print("-"*40)

def main():
  vectorizer = TfidfVectorizer(max_df=0.5,
                               min_df=2, stop_words='english',
                               use_idf=True)

  ffeatures, fids = get_data()
  x = vectorizer.fit_transform(ffeatures)

  labels = int(len(ffeatures) * (1 / 4)) + 1
  x = red(x, labels)
  x_red = reduce_dimensions(x, 2)
  n_clusters = int(len(ffeatures) * (1 / 5)) + 1
  centroids, c, k = k_means_cluster(x, n_clusters)

  print_clusters(c, fids)

  print( metrics.silhouette_score(x, c, metric='euclidean') )

def find_optimal_k_means():
  vectorizer = TfidfVectorizer(max_df=0.5,
                               min_df=2, stop_words='english',
                               use_idf=True)
  ffeatures, fids = get_data()
  x = vectorizer.fit_transform(ffeatures)
  (m, n) = x.shape

  m_score, clusters, dim = 0, 0, 0
  for o_off in [7.5,7,6.5,6,5.5]:
    o_off = int(m * (1 / o_off))
    x_red = red(x, o_off)

    for i_off in [7,6.5,6,5.5]:
      n_clusters = int(m * (1 / i_off)) + 1
      centroids, c, k = k_means_cluster(x_red, n_clusters)
      print("  kmeans with:", n_clusters, "i_off:", i_off)

      new_score = metrics.silhouette_score(x_red, c, metric='euclidean')

      if new_score >= m_score:
        print("    new score:", new_score, "clusters:", n_clusters, "dim for lsa:", o_off)
        m_score = new_score
        clusters = n_clusters
        dim = o_off

  print("final score:", m_score, "with k=",clusters, "dim lsa=",dim)
  x_red = red(x, dim)
  x_pcad = reduce_dimensions(x_red, 2)
  centroids, c, k = k_means_cluster(x_pcad, clusters)
  cluster_plot_2d(x_pcad, centroids, c, k)
  print_clusters(c, fids)


if __name__ == "__main__":
  find_optimal_k_means()



