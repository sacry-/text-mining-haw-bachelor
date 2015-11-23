import numpy as np

from sklearn.cluster import KMeans
from sklearn.cluster import MeanShift
from sklearn.cluster import estimate_bandwidth



'''
Name: K-Means
  
  N samples X into K disjoint clusters C, K is given

Params: number of clusters  

Scale: Very large n_samples

Character: 
  General-purpose, 
  even cluster size, 
  flat geometry, 
  not too many clusters  

Geometry/Metrics: Distances between points in Vectorspace

Description:
  - n groups of equal variance, minimizing a criterion 
  known as the inertia or within-cluster sum-of-squares

  - PCA before, to avoid dimensionality inflation
  - Cluster initialization is hard, several strategies 
    (high distance between clusters vs random)
  - is equal to expectation-maximization (EM) when input is covariance matrix
  - prone to local minima

  steps:
    1. assigns each sample to its nearest centroid
    2. new centroids by taking the mean of the samples of step 1.
    3. converge if difference(old_centroids, new_centroids) < threshold

Sources:
  - “k-means++: The advantages of careful seeding” Arthur, David, and Sergei Vassilvitskii, 
  Proceedings of the eighteenth annual ACM-SIAM symposium on Discrete algorithms, 
  Society for Industrial and Applied Mathematics (2007)
  - http://scikit-learn.org/stable/modules/clustering.html#k-means
'''
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



'''
Name: Mean-shift
  
  Discover blobs in a smooth density of samples. Update 
  candidates for centroids to be the mean of the points 
  within a given region

Params: bandwidth

Scale: Not scalable with n_samples Many clusters

Character: 
  uneven cluster size, 
  non-flat geometry

Geometry/Metrics: Distances between points in Vectorspace

Description:
  - nearest neighbour searches to find best centroid for sample

  - PCA before, to avoid dimensionality inflation
  - automatic cluster finding

Sources:
  - “Mean shift: A robust approach toward feature space analysis.” 
    D. Comaniciu and P. Meer, 2002
    IEEE Transactions on Pattern Analysis and Machine Intelligence
  - http://scikit-learn.org/stable/modules/clustering.html#mean-shift
'''
def mean_shift(x, quantile=0.08):
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


