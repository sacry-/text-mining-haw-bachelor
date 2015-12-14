from __future__ import division

from collections import defaultdict
from collections import Counter

from sklearn.metrics.cluster import adjusted_rand_score
from sklearn.metrics.cluster import silhouette_score
from sklearn.metrics.cluster import adjusted_mutual_info_score
from sklearn.metrics.cluster import completeness_score
from sklearn.metrics.cluster import v_measure_score



class ClusterEval():

  def __init__(self, x, c, labels, named_labels):
    self.x = x
    self.c = c
    self.labels = labels
    self.named_labels = named_labels

  def calculate_scores(self):
    x, c, labels = self.x, self.c, self.labels
    self.v_measure = v_measure_score(c, labels)
    self.complete = completeness_score(c, labels)
    self.adjusted_mutual = adjusted_mutual_info_score(c, labels)
    self.adjusted_rand = adjusted_rand_score(c, labels)
    self.silhouette = silhouette_score(x, c)
    self.purity, self.partial_purity = self.__purity__()

  def __purity__(self):
    r = defaultdict(list)
    for idx, assign in enumerate(self.c):
      r[assign].append( self.named_labels[idx] )

    centroid_map = {assign: Counter(v) for assign, v in r.items()}

    partial_pure, true, false = [], 0, 0
    for assign, counter in centroid_map.items():
      max_sort = sorted(counter.items(), key=lambda x: -x[1])
      category_proportions = [b for _, b in max_sort]
      
      curr_true = category_proportions[0]
      curr_false = sum(category_proportions[1:])
      
      true += curr_true
      false += curr_false

      purity_curr = (curr_true / (curr_true + curr_false))* 100

      partial_pure.append( (assign, purity_curr, max_sort) )

    purity = (true / (true + false)) * 100

    return purity, partial_pure



