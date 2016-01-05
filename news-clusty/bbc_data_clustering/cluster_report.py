from __future__ import division

from paths import base_path
from collections import defaultdict


class CompositeStats():

  def __init__(self, evals):
    self.evals = evals
    self.n = len(self.evals)

  def v_measure(self):
    return self.average( [r.v_measure for r in self.evals] )

  def purity(self):
    return self.average( [r.purity for r in self.evals] )

  def silhouette(self):
    return self.average( [r.silhouette for r in self.evals] )

  def partial_purity(self):
    d = {
      "entertainment" : defaultdict(int),
      "politics" : defaultdict(int),
      "tech" : defaultdict(int),
      "sport" : defaultdict(int),
      "business" : defaultdict(int)
    }
    for run in self.evals:
      segments = [b for (_,_,b) in run.partial_purity]
      for segment in segments:
        fst = segment[0][0]
        for assign, count in segment:
          d[fst][assign] += count

    average_partial_purity = {}
    for main, d_sub in d.items():
      s = sorted(list(d_sub.items()), key=lambda x: -x[1])
      average_partial_purity[main] = [(a, int(b / self.n)) for (a, b) in s]

    return average_partial_purity.items()

  
  def average(self, seq):
    return sum(seq) / self.n

  def __repr__(self):
    accu = []  
    accu.append( "-"*40 )
    accu.append( "averaged v-measure {}".format(self.v_measure()) )
    accu.append( "averaged purity {}".format(self.purity()) )
    accu.append( "averaged silhouette {}".format(self.silhouette()) )
    accu.append( "-"*40 )
    return "\n".join( accu )

  def long_repr(self):    
    accu = [] 
    for main, sub in self.partial_purity():
      accu.append( "  {}".format(main) )
      for clazz, count in sub:
        accu.append( "    {}: {}".format(clazz, count) )
    return "\n".join( accu )


class Report():

  def __init__(self, evaluation):
    self.eval = evaluation
    self.report_str = self.generate()

  def dump(self, report_name):
    p = "{}/reports/{}".format(base_path(), report_name)
    with open(p, "a+") as fp:
      fp.write(self.report_str)

  def generate(self):
    report_str = ["", "-"*40]
    report_str.append(self.eval.algo_name)
    
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

  def __repr__(self):
    return self.report_str


if __name__ == "__main__":
  pass
