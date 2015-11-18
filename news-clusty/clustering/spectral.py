import numpy as np

from sklearn.cluster import SpectralClustering
from sklearn.cluster import AffinityPropagation



'''
Name: Spectral clustering
  
   Message passing between data points, samples choose (availability), 
   self finds responsibility

Params: 
  number of clusters

Scale: 
  Medium n_samples, 
  small n_clusters

Character: 
  Few clusters, 
  even cluster size, 
  non-flat geometry

Geometry/Metrics: Graph distance (e.g. nearest-neighbor graph)

Description:
  - responsibility r(i, k), the accumulated evidence that sample k 
  should be the exemplar for sample i
  - availability a(i, k), the accumulated evidence that sample i should 
  choose sample k to be its exemplar
  - exemplars are chosen
    (1) similar enough to many samples 
    (2) chosen by many samples to be representative of themselves

Sources:
  - “On Spectral Clustering: Analysis and an algorithm” 
    Andrew Y. Ng, Michael I. Jordan, Yair Weiss, 2001
  - http://scikit-learn.org/stable/modules/clustering.html#spectral-clustering
'''
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


'''
Name: Affinity propagation
  
   Message passing between data points, samples choose (availability), 
   self finds responsibility

Params: 
  damping (convergence), 
  sample preference (number of clusters influenced by this)

Scale: Not scalable with n_samples

Character: 
  Many clusters, 
  uneven cluster size, 
  non-flat geometry 

Geometry/Metrics: Graph distance (e.g. nearest-neighbor graph) 

Description:
  - responsibility r(i, k), the accumulated evidence that sample k 
  should be the exemplar for sample i
  - availability a(i, k), the accumulated evidence that sample i should 
  choose sample k to be its exemplar
  - exemplars are chosen
    (1) similar enough to many samples 
    (2) chosen by many samples to be representative of themselves

Sources:
  - Brendan J. Frey and Delbert Dueck, 
    “Clustering by Passing Messages Between Data Points”, 
    Science Feb. 2007
  - http://scikit-learn.org/stable/modules/clustering.html#affinity-propagation
'''
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