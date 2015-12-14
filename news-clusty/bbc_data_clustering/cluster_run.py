from __future__ import division

from paths import base_path

from sklearn.metrics.cluster import adjusted_rand_score
from sklearn.metrics.cluster import silhouette_score
from sklearn.metrics.cluster import adjusted_mutual_info_score
from sklearn.metrics.cluster import completeness_score
from sklearn.metrics.cluster import v_measure_score

from collections import Counter
from collections import defaultdict


class Run():

  def __init__(self, clusterer, cluster_config,
      topic_model=None,
      similarity=None,
      normalization=None,
      labels=[], 
      named_labels=[],
      n_topics=None, 
      num_iters=None, 
      dr_dim=None,
      index=None
    ):

    self.index = index

    self.clusterer = clusterer
    self.cluster_config = cluster_config
    self.n_clusters = self.cluster_config[0]

    self.topic_model = topic_model
    self.n_topics = n_topics

    self.similarity = similarity
    self.normalization = normalization

    self.labels = labels
    self.named_labels = named_labels
    self.num_iters = num_iters
    self.dr_dim = dr_dim


  def start(self, x):
    if self.topic_model:
      x, _ = self.topic_model( x, self.n_topics )

    if self.similarity:
      x = self.similarity(x)

    if self.normalization:
      x = self.normalization(x)
    
    print(x.shape)

    self.model, (self.centroids, self.c, self.k) = self.clusterer( 
      x, *self.cluster_config
    )

    return (x, self.c, self.k)

  def set_scores(self, evaluation):
    self.v_measure = evaluation.v_measure
    self.complete = evaluation.complete
    self.adjusted_mutual = evaluation.adjusted_mutual
    self.adjusted_rand = evaluation.adjusted_rand
    self.silhouette = evaluation.silhouette
    self.purity, self.partial_purity = evaluation.purity, evaluation.partial_purity

  def __lt__(self, other):
    return self.v_measure < other.v_measure

  def __eq__(self, other):
    return self.v_measure == other.v_measure

  def __repr__(self):
    return "config: ({}, {}) - purity: {}% v_measure: {} adjusted_rand: {} silhouette: {}".format(
      self.n_clusters, 
      self.n_topics, 
      self.purity, 
      self.v_measure, 
      self.adjusted_rand, 
      self.silhouette
    )

  def config(self):
    return (self.n_clusters, self.n_topics)

if __name__ == "__main__":
  pass




