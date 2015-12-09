from __future__ import division

import logging
import numpy as np

from data_view import BBCDocuments
from data_view import BBCData

from features import tfidf_vector
from features import lsa

from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import normalize

from clustering import ward_linkage

from preprocessing import tokenize_string
from preprocessing import stem
from preprocessing import stemmatize


from cluster_run import Run


'''
Ward linkage: 94.70422535211269%
  - BBC Data percent = 0.8
  - tfidf ngram = (1,1) max_df = 0.8 min_df = 3 
  - topics = 225
  - cosine_simimilarity on X (as Covariance X*X.T)
  - normalize # unit vector norm "l2"
  - ward_linkage n = 5

0: accuracy: 99.75186104218362% - [('sport', 402), ('tech', 1)]
1: accuracy: 93.63057324840764% - [('entertainment', 294), ('tech', 11), ('politics', 5), ('business', 3), ('sport', 1)]
2: accuracy: 97.12041884816755% - [('business', 371), ('tech', 6), ('politics', 3), ('sport', 2)]
3: accuracy: 91.64265129682997% - [('politics', 318), ('business', 17), ('tech', 6), ('entertainment', 5), ('sport', 1)]
4: accuracy: 89.96960486322189% - [('tech', 296), ('business', 17), ('entertainment', 9), ('politics', 7)]
Accuracy: 94.70422535211269%
Silhouette 0.1059495054508847
Adjusted rand score 0.87757112392113
Adjusted mutual info score 0.844703689201236
Completeness score 0.8467376266903127
V Measure 0.8459387472004234
'''

def preprocess(x):
  print("tokenizing")
  doc_tokens = [tokenize_string(doc) for doc in x] 
  print("stemming")
  doc_stems = [stemmatize(tokens) for tokens in doc_tokens]
  print("joining")
  X = [" ".join(stems) for stems in doc_stems]
  # X = preprocess(X)
  X, vsmodel = tfidf_vector( X, ngram=(1,1), max_df=0.99, min_df=1 )
  return X, vsmodel

def setup_data(bbc_data):
  X = bbc_data.X()
  X, vsmodel = tfidf_vector( X, ngram=(1,1), max_df=0.8, min_df=3 )
  print("X: {}".format(X.shape))

  y = bbc_data.y()
  print("y: {}".format(len(y)))

  X_test = bbc_data.X_test()
  X_test = vsmodel.transform(X_test)
  print("X_test: {}".format(X_test.shape))
  y_test = bbc_data.y_test()
  print("y_test: {}".format(len(y_test)))

  return X, y, X_test, y_test


def main(n_clusters, n_topics, percent_data):
  algo_name = "Ward"

  # Data
  bbc = BBCDocuments()
  bbc_data = BBCData( bbc, percent=percent_data )

  ids = {idx: bbc.categories()[_id] for idx, _id in enumerate(bbc_data.index_train)}
  cats = [bbc.cat_to_id()[bbc.categories()[_id]] for _id in bbc_data.index_train]
  
  X, y, X_test, y_test = setup_data(bbc_data)

  X, _ = lsa( X, n_topics )
  X = cosine_similarity(X)
  X = normalize(X)
  print(X.shape)

  centroids, c, k, ward = ward_linkage( X, n_clusters = n_clusters )

  return X, c, ids, cats

def get_config(k=5, percentage=0.9):
  topics = [220, 225, 230, 235, 240]
  for n_topics in topics:
    yield (k, n_topics, percentage)



if __name__ == "__main__":
  logging.basicConfig(format='%(asctime)s %(message)s', level=logging.INFO)

  runs = []
  iteration = 1

  for _ in range(0, 2 + 1):
    for config in get_config():
      print(iteration, "-"*20, config, "-"*20)

      a_run = Run(iteration)
      a_run.invoke(main, config)
      runs.append(a_run)

      iteration += 1

  should_dump = False
  for r in sorted(runs, key= lambda x: -x.v_measure):
    print(r)

    if should_dump:
      r.dump()




