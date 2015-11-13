from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler



def dbscan(x, eps=0.2, min_samples=5):
  x = StandardScaler().fit_transform(x)
  db = DBSCAN(eps=eps, min_samples=min_samples).fit(x)

  labels = db.labels_
  k = len(set(labels)) - (1 if -1 in labels else 0)

  return None, labels, k


if __name__ == "__main__":
  pass