from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler


'''
Name: DBSCAN
  
  Areas of high density separated by areas of low density

Params: 
  min_samples (minimum samples that form a core),
  eps (within a distance of eps)

Scale: 
  Very large n_samples, 
  medium n_clusters

Character: 
  non-flat geometry, 
  uneven cluster sizes

Geometry/Metrics: Distances between nearest points

Description:
  - Clusters are cores
  - desity is set by min_samples per core and the maximum distance eps to a core  

Sources:
  - “A Density-Based Algorithm for Discovering Clusters in Large Spatial Databases with Noise” 
    Ester, M., H. P. Kriegel, J. Sander, and X. Xu, 1996
    In Proceedings of the 2nd International Conference on Knowledge Discovery and Data Mining, 
    Portland, OR, AAAI Press, pp. 226–231
  - http://scikit-learn.org/stable/modules/clustering.html#dbscan
'''
def dbscan(x, eps=0.2, min_samples=5):
  x = StandardScaler().fit_transform(x)
  db = DBSCAN(eps=eps, min_samples=min_samples).fit(x)

  labels = db.labels_
  k = len(set(labels)) - (1 if -1 in labels else 0)

  return db, (None, labels, k)



if __name__ == "__main__":
  pass