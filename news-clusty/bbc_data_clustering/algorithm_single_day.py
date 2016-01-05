from data_view import BBCDocuments
from data_view import BBCData

from io_utils import print_clusters
from io_utils import print_top_words
from io_utils import plot

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


def flattened_mapping(c, x_orig, bbc):
  cluster_to_docs = defaultdict(list)
  for doc_id, c_id in enumerate(c):
    cluster_to_docs[c_id].append( doc_id )

  for c_id, doc_ids in cluster_to_docs.items():
    docs, fids = [], []
    for doc_id in doc_ids:
      docs.append( x_orig[doc_id] )
      fids.append( bbc.titles()[doc_id] )

    yield (c_id, docs, fids)


def cluster(c, x_orig, bbc):
  switch = 2

  for c_id, docs, fids in flattened_mapping(c, x_orig, bbc):
    n_events = int(len(docs) / 2)

    if switch == 0:
      z, _ = tfidf_vector( docs, ngram=(1,1), max_df=0.8, min_df=3 )
      z, _ = lsa( z, n_events )
      z = cosine_similarity(z)
      z = normalize(z)
      _, (centroids, c_sub, k) = ward_linkage(z, n_clusters=n_events )

      d = defaultdict(list)
      for sub_doc_id, sub_cluster_id in enumerate(c_sub):
        d[sub_cluster_id].append( fids[sub_doc_id] )

      for cluster_id, document_titles in d.items():
        if len(document_titles) > 1:
          print(cluster_id, len(document_titles))
          for document_title in document_titles:
            print(" ", document_title)

    elif switch == 1:
      z, vsmodel = count_vector( docs, ngram=(1,1), max_df=0.9, min_df=2 )
      z, model = lda( z, n_topics=int(n_events / 4), max_iter=50 )
      print_top_words(
        model, vsmodel.get_feature_names(), 
        n_top_words=7, n_topics=10
      )

    elif switch == 2:
      z, _ = tfidf_vector( docs, ngram=(1,1), max_df=0.8, min_df=3 )
      z, _ = lsa( z, n_events )
      z, _ = pca( z, 2 )
      _, (centroids, c_sub, k) = birch(z, threshold=0.19, branching_factor=10)
      plot(z, centroids, c_sub, k, "BIRCH", 2)

def single_day(bbc):
  knowledge = list(bbc.concat(
    bbc.sents(),
    bbc.title_tokens(),
    bbc.nouns()
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

