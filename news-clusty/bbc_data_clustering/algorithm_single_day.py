from data_view import BBCDocuments
from data_view import BBCData

from io_utils import print_clusters

from cluster_eval import ClusterEval
from cluster_report import Report
from cluster_report import CompositeStats

from features import tfidf_vector, count_vector
from features import lsa
from features import pca
from features import lda
from features import nmf

from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics.pairwise import euclidean_distances
from sklearn.metrics.pairwise import laplacian_kernel

from sklearn.preprocessing import normalize

from clustering import ward_linkage 
from clustering import kmeans
from clustering import birch

from collections import defaultdict
from collections import Counter


def setup_data(bbc, knowledge):
  bbc_data = BBCData( 
    bbc, 
    percent=0.8, 
    data_domain=list(knowledge)
  )

  named_labels = bbc_data.categories_train()
  labels = bbc_data.category_ids_train()

  x_orig = bbc_data.x()
  x, vsmodel = tfidf_vector( x_orig, ngram=(1,1), max_df=0.8, min_df=3 )
  print("X: {}".format(x.shape))

  y = bbc_data.y()

  print("y: {}".format(len(y)))

  return x, y, labels, named_labels, x_orig


def cluster(c, x_orig, bbc):
  print(len(c), len(x_orig))

  cluster_to_docs = defaultdict(list)
  for doc_id, c_id in enumerate(c):
    cluster_to_docs[c_id].append( doc_id )

  for c_id, doc_ids in cluster_to_docs.items():
    docs, fids = [], []
    for doc_id in doc_ids:
      docs.append( x_orig[doc_id] )
      fids.append( bbc.titles()[doc_id] )

    z, _ = tfidf_vector( docs, ngram=(1,1), max_df=0.8, min_df=3 )
    z, _ = lsa( z, 100 )
    z = cosine_similarity(z)
    z = normalize(z)
    _, (centroids, c_sub, k) = birch(z, n_clusters=100, threshold=0.5, branching_factor=10)

    d = defaultdict(list)
    for sub_doc_id, sub_cluster_id in enumerate(c_sub):
      d[sub_cluster_id].append( fids[sub_doc_id] )

    for cluster_id, document_titles in d.items():
      '''
      if len(document_titles) > 2:
        print(cluster_id, len(document_titles))
        for document_title in document_titles:
          print(" ", document_title)
      '''
      pass
    print("total:", k)

def single_day(bbc):
  knowledge = list(bbc.concat(
    bbc.nouns(),
    bbc.sents()
  ))

  x, y, labels, named_labels, x_orig = setup_data( bbc, knowledge )
  x, _ = lsa( x, 150 )
  x = cosine_similarity(x)
  x = normalize(x)
  
  print( x.shape )

  _, (centroids, c, k) = ward_linkage( x, 5 )

  cluster(c, x_orig, bbc)

if __name__ == "__main__":
  bbc = BBCDocuments()
  # evaluate_classification( bbc )
  single_day(bbc)

