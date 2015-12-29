from data_view import BBCDocuments
from data_view import BBCData

from cluster_run import Run
from cluster_eval import ClusterEval
from cluster_report import report_for_run, Report

from features import tfidf_vector, count_vector
from features import lsa, pca
from features import lda, nmf

from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics.pairwise import euclidean_distances
from sklearn.metrics.pairwise import laplacian_kernel

from sklearn.preprocessing import normalize
from clustering import ward_linkage, kmeans


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
  knowledge = bbc.concat( 
    bbc.wordnet("fst_hyper"), 
    bbc.nouns() 
  )

  bbc_data = BBCData( 
    bbc, 
    percent=0.8, 
    data_domain=list(knowledge)
  )
  X, y = setup_data(bbc_data)

  named_labels = bbc_data.categories_train()
  labels = bbc_data.category_ids_train()

  runs, reports = [], []
  report_name = "2_wordnet_model.txt"
  algo_name = "Ward Linkage"
  should_create_report = False

  for index, n_clusters, n_topics in configuration():
    print(index, "-"*20, (n_clusters, n_topics), "-"*20)

    run = Run( 
      clusterer=ward_linkage,
      cluster_config=(n_clusters,),
      topic_model=lsa,
      similarity=cosine_similarity,
      normalization=normalize,
      labels=labels, 
      named_labels=named_labels,
      n_topics=n_topics,
      index=index
    )
    x, c, k = run.start( X )

    evaluation = ClusterEval(x, c, labels, named_labels)
    evaluation.calculate_scores()
    run.set_scores(evaluation)

    report = Report( run, evaluation )
    print( report.generate( algo_name ) )
    runs.append( run )
    reports.append( report )

  for run in sorted(runs, key=lambda x: -x.v_measure):
    print(run)

    if should_create_report: 
      report_for_run(run, reports).dump( report_name )




