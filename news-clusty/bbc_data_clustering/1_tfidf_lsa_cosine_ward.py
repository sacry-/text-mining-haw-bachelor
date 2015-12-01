from __future__ import division

import logging
import numpy as np

from collections import Counter
from collections import defaultdict

from data_view import BBCDocuments
from data_view import BBCData

from features import tfidf_vector
from features import lsa

from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import normalize

from clustering import ward_linkage

from clustering import silhouette
from sklearn.metrics import adjusted_rand_score


'''
Ward linkage: 93.15315315315316%
  - BBC Data percent = 0.5
  - tfidf ngram = (1,1) max_df = 0.8 min_df = 3 
  - topics = 225
  - cosine_simimilarity on X (as Covariance X*X.T)
  - normalize # unit vector norm "l2"
  - ward_linkage n = 8
'''

def preprocess(x):
  from preprocessing import tokenize_string
  from preprocessing import stem
  from preprocessing import stemmatize

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


def report(X, c, ids):
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

    print("  {}: accuracy: {}% - {}".format(assign, (curr_true / (curr_true + curr_false))* 100, max_sort))
  
  print("Accuracy: {}%".format((true / (true + false))* 100))
  print("Silhouette {}".format(silhouette(X, c)))


if __name__ == "__main__":
  logging.basicConfig(format='%(asctime)s %(message)s', level=logging.INFO)
  algo_name = "Ward"

  # Data
  bbc = BBCDocuments()
  bbc_data = BBCData( bbc, percent=0.5 )

  ids = {idx: bbc.categories()[_id] for idx, _id in enumerate(bbc_data.index_train)}

  X, y, X_test, y_test = setup_data(bbc_data)

  X, _ = lsa( X, 225 )
  X = cosine_similarity(X)
  X = normalize(X)
  print(X.shape)

  centroids, c, k, ward = ward_linkage( X, n_clusters = 8 )

  print("-"*40, "\n", algo_name, "\n", "-"*40)
  report(X, c, ids)


