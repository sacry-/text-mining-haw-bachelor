from clustering import silhouette

from sklearn.metrics.cluster import adjusted_rand_score
from sklearn.metrics.cluster import adjusted_mutual_info_score
from sklearn.metrics.cluster import completeness_score
from sklearn.metrics.cluster import v_measure_score

from paths import base_path

from collections import Counter
from collections import defaultdict



class Run():

  def __init__(self, iteration):
    self.config = (self.k, self.n_topics, self.percentage) = (None, None, None)
    self.iteration = iteration
    self.report_str = None

  def __lt__(self, other):
    return self.v_measure < other.v_measure

  def __eq__(self, other):
    return self.v_measure == other.v_measure

  def __repr__(self):
    return "{}. {} - precision: {} v_measure: {} adjusted_rand: {}".format(self.iteration, self.config, self.precision, self.v_measure, self.adjusted_rand)

  def invoke(self, f, config):
    self.config = (self.k, self.n_topics, self.percentage) = config
    X, c, ids, cats = f(*self.config)
    self.report_str = self.report(X, c, ids, cats)
    print(self.report_str)

  def dump(self):
    p = "{}/1_tfidf_lsa_cosine_ward_report.txt".format(base_path())
    with open(p, "a+") as fp:
      fp.write(self.report_str)

  def report(self, X, c, ids, cats):
    report_str = ["", "-"*40]
    report_str.append("Ward Linkage:")
    report_str.append( "  config: {}".format(", ".join([str(a) for a in self.config])) )
    report_str.append( "  {}".format("-"*40) )

    r = defaultdict(list)
    for idx, assign in enumerate(c):
      r[assign].append( ids[idx] )

    true, false = 0, 0
    centroid_map = {assign: Counter(v) for assign, v in r.items()}
    for assign, counter in centroid_map.items():
      max_sort = sorted(counter.items(), key=lambda x: -x[1])
      category_proportions = [b for _, b in max_sort]
      
      curr_true = category_proportions[0]
      curr_false = sum(category_proportions[1:])
      
      true += curr_true
      false += curr_false

      precision_curr = (curr_true / (curr_true + curr_false))* 100
      s = "  {}: precision: {}% - {}".format(assign, precision_curr, max_sort)
      report_str.append( s )

    report_str.append( "  {}".format("-"*40) )

    self.v_measure = v_measure_score(c, cats)
    self.complete = completeness_score(c, cats)
    self.adjusted_mutual = adjusted_mutual_info_score(c, cats)
    self.adjusted_rand = adjusted_rand_score(c, cats)
    self.precision = (true / (true + false)) * 100

    report_str.append( "  Precision: {}%".format(self.precision) )
    report_str.append( "  V Measure {}".format(self.v_measure) )
    report_str.append( "  Adjusted rand score {}".format(self.adjusted_rand) )
    report_str.append( "  Adjusted mutual info score {}".format(self.adjusted_mutual) )
    report_str.append( "  Completeness score {}".format(self.complete) )
    report_str.append( "  Silhouette {}".format(silhouette(X, c)) )
    
    return "\n".join(report_str)


if __name__ == "__main__":
  pass



