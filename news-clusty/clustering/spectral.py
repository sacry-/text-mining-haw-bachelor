import numpy as np

from sklearn.cluster import SpectralClustering
from sklearn.cluster import AffinityPropagation


def spectral(x, num_clusters):
  spec = SpectralClustering(
    affinity='rbf', # 'rbf'
    n_clusters=num_clusters,
    n_init=10,
    assign_labels='kmeans', 
    gamma=1.0, 
    degree=3, 
    coef0=1
  )
  spec.fit(x)

  c = spec.labels_
  k = len(np.unique(c))

  return None, c, k


def affinity_propagation(x, damping=0.5):
  ap = AffinityPropagation(
    damping=damping, 
    max_iter=400, 
    convergence_iter=30, 
    copy=True, 
    preference=None, 
    affinity='euclidean', 
    verbose=False
  )
  ap.fit(x)
  centroids = ap.cluster_centers_
  c = ap.labels_
  k = len(centroids)
  
  return centroids, c, k


if __name__ == "__main__":
  pass