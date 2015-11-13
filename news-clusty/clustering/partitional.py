import numpy as np

from sklearn.cluster import KMeans
from sklearn.cluster import MeanShift
from sklearn.cluster import estimate_bandwidth



def kmeans(x, num_clusters=1):
  km = KMeans(
    init='k-means++', 
    n_clusters=num_clusters, 
    n_init=20, 
    copy_x=True
  )
  km.fit(x)

  centroids = km.cluster_centers_
  c = km.labels_
  k = km.n_clusters

  return centroids, c, k



def mean_shift(x, quantile=0.01):
  bandwidth = estimate_bandwidth(x, quantile=quantile)
  ms = MeanShift(bandwidth=bandwidth)
  ms.fit(x)

  c = ms.labels_
  centroids = ms.cluster_centers_
  c_unique = np.unique(c)
  k = len(c_unique)

  return centroids, c, k


if __name__ == "__main__":
  pass


