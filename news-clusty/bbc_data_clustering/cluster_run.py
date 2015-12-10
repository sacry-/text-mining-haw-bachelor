from __future__ import division

from paths import base_path


from sklearn.metrics.cluster import adjusted_rand_score
from sklearn.metrics.cluster import silhouette_score
from sklearn.metrics.cluster import adjusted_mutual_info_score
from sklearn.metrics.cluster import completeness_score
from sklearn.metrics.cluster import v_measure_score

from collections import Counter
from collections import defaultdict



def find_optimum(x, clusterer,
    topic_model=None,
    similarity=None,
    normalization=None,
    labels=[], 
    named_labels=[],
    n_topics=225, 
    n_clusters=5, 
    num_iters=None, 
    dr_dim=None,
    index=None
  ):

  run_config = (n_clusters, n_topics)
  print(index, "-"*20, run_config, "-"*20)

  run = Run(
    clusterer,
    config=run_config,
    topic_model=topic_model,
    similarity=similarity,
    normalization=normalization,
    index=index
  )
  run.invoke( x, labels, named_labels )
  run.evaluate()

  return run


class Run():

  def __init__(self, 
      clusterer,
      config=(None, None),
      topic_model=None,
      similarity=None,
      normalization=None,
      index=None
    ):

    self.clusterer = clusterer
    self.config = (self.n_clusters, self.n_topics) = config

    self.topic_model = topic_model
    self.similarity = similarity
    self.normalization = normalization

    self.index = index

  def invoke(self, x, labels, named_labels):
    self.labels = labels
    self.named_labels = named_labels

    if self.topic_model:
      x, _ = self.topic_model( x, self.n_topics )

    if self.similarity:
      x = self.similarity(x)

    if self.normalization:
      x = self.normalization(x)
  
    print(x.shape)

    centroids, c, k, ward = self.clusterer( x, n_clusters = self.n_clusters )

    self.x = x
    self.centroids = centroids
    self.k = k
    self.c = c

  def evaluate(self):
    c, labels = self.c, self.labels
    self.v_measure = v_measure_score(c, labels)
    self.complete = completeness_score(c, labels)
    self.adjusted_mutual = adjusted_mutual_info_score(c, labels)
    self.adjusted_rand = adjusted_rand_score(c, labels)
    self.silhouette = silhouette_score(self.x, c)

  def __lt__(self, other):
    return self.v_measure < other.v_measure

  def __eq__(self, other):
    return self.v_measure == other.v_measure

  def __repr__(self):
    return "config: {} - v_measure: {} adjusted_rand: {} silhouette: {}".format(self.config, self.v_measure, self.adjusted_rand, self.silhouette)


if __name__ == "__main__":
  pass




