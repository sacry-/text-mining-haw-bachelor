from sklearn import metrics
from sklearn.metrics import pairwise_distances


def silhouette(x, centers, metric='euclidean'):
  return metrics.silhouette_score(x, centers, metric=metric)


if __name__ == "__main__":
  pass