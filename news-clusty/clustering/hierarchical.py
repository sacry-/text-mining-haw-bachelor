from sklearn.cluster import AgglomerativeClustering
from sklearn.cluster import Birch
from sklearn.neighbors import kneighbors_graph


def ward_linkage(x, num_clusters=20):
  knn_graph = kneighbors_graph(x, 40, include_self=False)
  return __agglomerative__(x, num_clusters, "ward", knn_graph)

def average_linkage(x, num_clusters=20):
  return __agglomerative__(x, num_clusters, "average", None)

def complete_linkage(x, num_clusters=20):
  return __agglomerative__(x, num_clusters, "complete", None)


def __agglomerative__(x, num_clusters, linkage, connectivity):
  ac = AgglomerativeClustering(
    n_clusters=num_clusters,
    connectivity=connectivity,
    linkage=linkage
  )
  ac.fit(x)
  c = ac.labels_
  k = ac.n_clusters
  return None, c, k



def birch(x, num_clusters=None, threshold=0.3, branching_factor=10):
  birch_model = Birch(
    threshold=threshold, 
    n_clusters=num_clusters, 
    branching_factor=branching_factor
  )
  birch_model.fit(x)

  centroids = birch_model.subcluster_centers_
  c = birch_model.labels_
  k = len(centroids)

  return centroids, c, k




if __name__ == "__main__":
  pass