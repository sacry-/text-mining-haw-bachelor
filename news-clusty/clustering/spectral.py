import numpy as np

from sklearn.cluster import SpectralClustering


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


if __name__ == "__main__":
  pass