

class Report():

  def __init__(self, run):
    self.run = run
    self.iteration = self.run.iteration
    self.report_str = None

  def dump(self, report_name):
    p = "{}/reports/{}".format(base_path(), report_name)
    with open(p, "a+") as fp:
      fp.write(self.report_str)

  def generate(self):
    config = self.run.config
    c = self.run.c
    v_measure = self.run.v_measure
    complete = self.run.complete
    adjusted_mutual = self.run.adjusted_mutual
    adjusted_rand = self.run.adjusted_rand
    silhouette = self.run.silhouette
    labels = self.run.labels
    named_labels = self.run.named_labels

    report_str = ["", "-"*40]
    report_str.append("Ward Linkage:")
    report_str.append( "  config: {}".format(", ".join([str(a) for a in config])) )
    report_str.append( "  {}".format("-"*40) )

    r = defaultdict(list)
    for idx, assign in enumerate(c):
      r[assign].append( named_labels[idx] )

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

    precision = (true / (true + false)) * 100

    report_str.append( "  Precision: {}%".format(precision) )
    report_str.append( "  V Measure {}".format(v_measure) )
    report_str.append( "  Adjusted rand score {}".format(adjusted_rand) )
    report_str.append( "  Adjusted mutual info score {}".format(adjusted_mutual) )
    report_str.append( "  Completeness score {}".format(complete) )
    report_str.append( "  Silhouette {}".format(silhouette) )
    
    self.report_str = "\n".join(report_str)

    return self.report_str


if __name__ == "__main__":
  pass
