from sklearn.cluster import AgglomerativeClustering
from sklearn.cluster import Birch
from sklearn.neighbors import kneighbors_graph



'''
Name: Agglomerative hierarchical clustering
  
  Ward: Minimizes sum of squared differences/variance-minimizing. Similar to k-means
    only euclidean
  Maximum/complete linkage: minimizes the maximum distance between observations
    graph, l1, l2, cosine, euclidean
  Average linkage: minimizes the average of the distances between observations
    graph, l1, l2, cosine, euclidean

Params: 
  number of clusters, 
  linkage type, 
  distance

Scale: Large n_samples and n_clusters

Character: 
  Many clusters

Geometry/Metrics: 
  Connectivity constraints, 
  non Euclidean distances 
  Any pairwise distance

Description:
  - nearest neighbour searches to find best centroid for sample

  - PCA before, to avoid dimensionality inflation
  - automatic cluster finding

Sources:
  - http://scikit-learn.org/stable/modules/clustering.html#hierarchical-clustering
'''
def ward_linkage(x, n_clusters=20, 
    affinity='euclidean', connectivity=None, 
    n_components=None, compute_full_tree='auto'):
  return __agglomerative__(x, n_clusters, "ward", affinity, connectivity, n_components, compute_full_tree)

def average_linkage(x, n_clusters=20, 
    affinity='euclidean', connectivity=None, 
    n_components=None, compute_full_tree='auto'):
  return __agglomerative__(x, n_clusters, "average", affinity, connectivity, n_components, compute_full_tree)

def complete_linkage(x, n_clusters=20, 
    affinity='euclidean', connectivity=None, 
    n_components=None, compute_full_tree='auto'):
  return __agglomerative__(x, n_clusters, "complete", affinity, connectivity, n_components, compute_full_tree)


def __agglomerative__(x, n_clusters, linkage, affinity, connectivity, n_components, compute_full_tree):
  ac = AgglomerativeClustering(
    n_clusters=n_clusters,
    connectivity=connectivity,
    linkage=linkage,
    affinity=affinity,
    n_components=n_components,
    compute_full_tree=compute_full_tree
  )
  ac.fit(x)
  c = ac.labels_
  k = ac.n_clusters
  return ac, (None, c, k)



'''
Name: Birch
  
Params: 
  branching factor (limits the number of subclusters in a node), 
  threshold (limits the distance between the entering sample), 
  optional global clusterer (n clusters, derived from the structure before)

Scale: 
  Large n_clusters and n_samples,
  Large dataset

Character: 
  outlier removal, 
  data reduction

Geometry/Metrics: Euclidean distance between points

Description:
  - nearest neighbour searches to find best centroid for sample

  - PCA before, to avoid dimensionality inflation
  - automatic cluster finding if global clusterer not set

Sources:
  - Tian Zhang, Raghu Ramakrishnan, Maron Livny 
    BIRCH: An efficient data clustering method for large databases
  - http://scikit-learn.org/stable/modules/clustering.html#birch
'''
def birch(x, n_clusters=None, threshold=0.5, branching_factor=5):
  birch_model = Birch(
    threshold=threshold, 
    n_clusters=n_clusters, 
    branching_factor=branching_factor
  )
  birch_model.fit(x)

  centroids = birch_model.subcluster_centers_
  c = birch_model.labels_
  k = len(centroids)

  return birch_model, (centroids, c, k)




if __name__ == "__main__":
  pass