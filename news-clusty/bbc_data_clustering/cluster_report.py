from __future__ import division

from paths import base_path


def report_for_run(run, reports):
  for report in reports:
    if report.index == run.index:
      return report


class Report():

  def __init__(self, run, evaluation):
    self.index = run.index
    self.config = run.config()
    self.eval = evaluation
    self.report_str = None

  def dump(self, report_name):
    p = "{}/reports/{}".format(base_path(), report_name)
    with open(p, "a+") as fp:
      fp.write(self.report_str)

  def generate(self, algo_name):
    report_str = ["", "-"*40]
    report_str.append(algo_name)
    report_str.append( "  config: {}".format(", ".join([str(a) for a in self.config])) )
    
    report_str.append( "  {}".format("-"*40) )
    for (assign, purity_curr, max_sort) in self.eval.partial_purity:
      s = "  {}: purity: {}% - {}".format(assign, purity_curr, max_sort)
      report_str.append( s )
    report_str.append( "  {}".format("-"*40) )

    report_str.append( "  Purity: {}%".format(self.eval.purity) )
    report_str.append( "  V Measure {}".format(self.eval.v_measure) )
    report_str.append( "  Adjusted rand score {}".format(self.eval.adjusted_rand) )
    report_str.append( "  Adjusted mutual info score {}".format(self.eval.adjusted_mutual) )
    report_str.append( "  Completeness score {}".format(self.eval.complete) )
    report_str.append( "  Silhouette {}".format(self.eval.silhouette) )
    
    self.report_str = "\n".join(report_str)

    return self.report_str


if __name__ == "__main__":
  pass
