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

  x = bbc_data.x()
  x, vsmodel = tfidf_vector( x, ngram=(1,1), max_df=0.8, min_df=3 )
  print("X: {}".format(x.shape))

  y = bbc_data.y()

  print("y: {}".format(len(y)))

  return x, y, labels, named_labels


def knowledge_profiles(bbc, scope=None):
  knowledges = {
    "word_tokens" : bbc.concat(
      bbc.sents(), 
      bbc.title_tokens()
    ),
    "syntactic" : bbc.concat(
      bbc.nouns(), 
      bbc.ners()
    ),
    "word_nouns" : bbc.concat(
      bbc.nouns(),
      bbc.sents()
    ),
    "wordnet_fst_hyper" : bbc.wordnet("fst_hyper"),
    "wordnet_hyper_1" : bbc.wordnet("hyper_1"),
    "wordnet_lemmas" : bbc.wordnet("lemmas")
  }

  if scope:
    return [(scope, knowledges[scope])]

  return knowledges.items()



def classify_cluster( bbc ):
  report_name = "1_simple_model.txt"
  algo_name = "Ward Linkage"
  should_create_report = False

  n_clusters = 5
  n_topics = 150
  topic_model = pca
  similarity = cosine_similarity
  normalization = normalize

  evals = []
  for _ in range(0, 5):
    x, y, labels, named_labels = setup_data( bbc, knowledge )

    if topic_model:
      x, _ = topic_model( x, n_topics )

    if similarity:
      x = similarity(x)

    if normalization:
      x = normalization(x)
    
    print( x.shape )

    _, (centroids, c, k) = ward_linkage( x, n_clusters )

    evaluation = ClusterEval(algo_name, x, c, 
      labels, named_labels,
      n_clusters=n_clusters, 
      n_topics=n_topics
    )
    evals.append( evaluation )

    report = Report( evaluation )
    print( report )
    if should_create_report: 
      report.dump( report_name )

  return evals

def evaluate_classification(bbc):
  composites = []
  for knowledge_name, knowledge in knowledge_profiles( bbc ):
    evals = classify_cluster( bbc, knowledge )

    for evaluation in sorted(evals, key=lambda x: -x.v_measure):
      print( evaluation )
    print( CompositeStats( evals ) )
    composites.append( (knowledge_name, composite) )
    
  for (knowledge_name, composite) in composites:
    print(knowledge_name)
    print(composite)



if __name__ == "__main__":
  bbc = BBCDocuments()
  evaluate_classification( bbc )

