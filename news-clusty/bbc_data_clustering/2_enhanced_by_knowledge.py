from data_view import BBCDocuments
from data_view import BBCData

from cluster_run import find_optimum
from cluster_report import report_for_run, Report

from features import tfidf_vector, count_vector
from features import lsa, pca
from features import lda, nmf

from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics.pairwise import euclidean_distances
from sklearn.metrics.pairwise import laplacian_kernel

from sklearn.preprocessing import normalize
from clustering import ward_linkage


def setup_data(bbc_data):
  X = bbc_data.X()
  X, vsmodel = tfidf_vector( X, ngram=(1,1), max_df=0.8, min_df=3 )
  print("X: {}".format(X.shape))

  y = bbc_data.y()
  print("y: {}".format(len(y)))

  return X, y

def configuration():
  for idx, topics in enumerate([5, 10, 20, 25, 225]):
    yield (idx, 5, topics)


if __name__ == "__main__":
  bbc = BBCDocuments()
  knowledge = bbc.concat( bbc.wordnet("wordnet_hyper_1"), bbc.nouns() )
  
  bbc_data = BBCData( 
    bbc, 
    percent=0.8, 
    data_domain=list(knowledge)
  )
  X, y = setup_data(bbc_data)

  named_labels = bbc_data.categories_train()
  labels = bbc_data.category_ids_train()

  runs, reports = [], []
  report_name = "2_enhanced_by_knowledge.txt"
  should_create_report = False

  for index, n_clusters, n_topics in configuration():

    run = find_optimum(X, 
      clusterer=lambda x, n_clusters: ward_linkage(x, n_clusters),
      topic_model=lambda x, n_topics: lsa(x, n_topics),
      similarity=lambda x: cosine_similarity(x),
      normalization=lambda x: normalize(x),
      labels=labels, 
      named_labels=named_labels,
      n_topics=n_topics, 
      n_clusters=n_clusters,
      index=index
    )

    report = Report( run )
    print( report.generate() )
    runs.append( run )
    reports.append( report )

  for run in sorted(runs, key=lambda x: -x.v_measure):
    print(run)

    if should_create_report: 
      report_for_run(run, reports).dump( report_name )




