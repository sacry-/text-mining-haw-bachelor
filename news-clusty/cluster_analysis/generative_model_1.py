from __future__ import division

import logging
import numpy as np

from es import EsSearcher
from preprocessing import TextNormalizer
from preprocessing import sentence_tokenize

from features import flattened_features
from features import count_vector
from features import tfidf_vector
from features import hash_vector

from features import pca
from features import nmf
from features import lsa
from features import lda

from io_utils import print_clusters
from io_utils import print_measure
from io_utils import append_to_file
from io_utils import plot

from clustering import silhouette


def get_training_set(from_date, to_date, limit=None):
  es = EsSearcher()
  tn = TextNormalizer()

  features, titles = [], []
  skipped = 0
  for idx, a in enumerate(es.articles_from_to(from_date, to_date)):
    if len(a.text.split(" ")) < 40:
      skipped += 1
      continue

    sentences = sentence_tokenize(a.text, tn.normalize)
    features.append( sentences )
    titles.append( str(a) )

    if limit and limit == idx:
      break

  if not limit:
    limit = len(titles) + skipped

  print("lim: {}, actual: {}, ratio: {}%".format(
    limit, len(features), (len(features) / limit) * 100)
  )

  return features, titles


def important_sentences(topic_model, doc):
  sorted_by_prob = []
  for topic_probs in topic_model.components_:
    id_to_prob = list(enumerate(topic_probs))
    s = sorted(id_to_prob, key=lambda x: -x[1])
    for idx, prob in s[:min(5,len(s))]:
      if len(doc) > idx:
        sorted_by_prob.append((doc[idx], prob))
  sorted_by_prob = sorted(sorted_by_prob, key=lambda x: -x[1])
  return [sentence for sentence, prob in sorted_by_prob]


# Script
def topic_model_run(decomposer, n_topics, ffeatures, fids):
  failed = []
  x_global = []

  for idx, doc in enumerate(ffeatures):
    try:
      x_hat, _ = count_vector( 
        doc, 
        ngram=(1,2),
        max_df=0.8, 
        min_df=0
      )
    except:
      failed.append((fids[idx], doc, "Sparse"))
      continue

    if x_hat.shape[1] > n_topics:

      x, topic_model = decomposer( x_hat, n_topics )
      feature_set = important_sentences(topic_model, doc)

      if feature_set:
        print(feature_set[0])
        x_global.append( " ".join( feature_set ) )

      else:
        failed.append((fids[idx], doc, "Topic Model"))

  try:
    docs = [doc for (_, doc, _) in failed]
    sent_docs = [len(doc) for doc in docs]
    word_docs = [len(" ".join(doc).split(" ")) for doc in docs]

    print("-"*40)
    for idx, (fail, _, reason) in enumerate(failed):
      print(fail, reason, sent_docs[idx], word_docs[idx] )

    avg_sent = np.average(sent_docs)
    avg_word = np.average(word_docs)
    print("average sent count:", avg_sent)
    print("average word count:", avg_word)
  except:
    print("Something went wrong during failure statistic generation")

  return x_global



if __name__ == "__main__":
  logging.basicConfig(format='%(asctime)s %(message)s', level=logging.INFO)

  # Data
  from_date = "20151114"
  to_date = "20151114"
  ffeatures, fids = get_training_set( 
    from_date, to_date
  )

  # Topic modelling
  decomposer = [lsa, lda, nmf, None][1]
  n_topics = 3
  x_topic = topic_model_run(decomposer, n_topics, ffeatures, fids)


  # Clustering
  from clustering import birch
  from clustering import kmeans

  x, _ = count_vector( 
    x_topic, 
    ngram=(1,2),
    max_df=0.99, 
    min_df=0.1
  )

  plot_dimension = 2
  x, _ = pca(x, plot_dimension)
  centroids, c, k = kmeans(x, 8)
  plot(x, centroids, c, k, "Birch", plot_dimension)
  if fids: 
    print_clusters(c, fids)

  print_measure("Birch", "silhouette", silhouette(x, c))

