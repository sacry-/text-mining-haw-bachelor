from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler



def dbscan(x, eps=0.3, min_samples=2):
  x = StandardScaler().fit_transform(x)
  db = DBSCAN(eps=0.3, min_samples=2).fit(x)

  labels = db.labels_
  k = len(set(labels)) - (1 if -1 in labels else 0)

  return None, labels, k


if __name__ == "__main__":
  pass