from sklearn import metrics
from sklearn.metrics import pairwise_distances



'''
Intuition: 
  (1) The score is higher when clusters are dense and well separated, 
  which relates to a standard concept of a cluster
  (2) -1 for incorrect clustering and +1 for highly dense clustering

Mathematics:
  a = mean distance between a sample and all other points in the same class
  b = mean distance between a sample and all other points in the next nearest cluster

  s = (b - a) / max(a, b)

Source:
  - Peter J. Rousseeuw (1987)
    “Silhouettes: a Graphical Aid to the Interpretation and Validation of Cluster Analysis”
    Computational and Applied Mathematics 20: 53–65
    doi:10.1016/0377-0427(87)90125-7
'''
def silhouette(x, centers, metric='euclidean'):
  return metrics.silhouette_score(x, centers, metric=metric)


if __name__ == "__main__":
  pass