from __future__ import division

from collections import Counter
from collections import defaultdict
from math import log


def tfidf( points ):
  n = len(points)

  tfreq, idf = {}, defaultdict(int)
  for doc, vector in points:
    counted = Counter(vector)
    for term in counted.keys():
      idf[term] += 1
    tfreq[doc] = counted

  tf_idf = {}
  for doc, doc_freq in tfreq.items():
    for term, tf in doc_freq.items():
      tf_idf[term] = log( 1 + tf ) * log( n / idf[term] )

  return tf_idf


def score( points, tf_idf, interest=[] ):
  sims = {}
  for doc, vector in points:
    s, c = 0, 1
    for term in vector:
      if term in interest:
        s += tf_idf[term]
        c += 1
    sims[doc] = (s / c)
  return sims


if __name__ == "__main__":
  points = [
    ["d1", ["t","abc","t", "defg", "t"]], 
    ["d2", ["abc", "t", "defg"]], 
    ["d3", ["y", "t", "x"]], 
    ["d4", ["t", "z", "t", "defg"]]
  ]
  for name, point in points:
    print( name, ":", point )

  tf_idf = tfidf( points )
  print( "tfidf:", tf_idf )

  f = lambda term: tf_idf[term] > 0.15 and tf_idf[term] < 0.96
  termset = set(sum(map(lambda x: x[1], points), []))
  filtered = filter(f, termset)
  print( "term:", termset, "| score:", score( points, tf_idf, ["x", "y"]) )






