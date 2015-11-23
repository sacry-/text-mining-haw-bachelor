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
from_date = "20151114"
to_date = "20151114"

decomposer = [lsa, lda, nmf, None][0]
n_topics = 3

ffeatures, fids = get_training_set( 
  from_date, to_date
)

failed = []
new_features = []
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

    if decomposer == nmf and x_hat.shape[0] <= n_topics:
      continue

    if x_hat.shape[1] > n_topics:

      x, topic_model = decomposer( x_hat, n_topics )
      feature_set = important_sentences(topic_model, doc)

      if feature_set:
        print(feature_set[0])

      else:
        failed.append((fids[idx], doc, "Topic Model"))

      new_features.append( 
        "__PLACE_HOLDER__".join(feature_set) 
      )

append_to_file("generative_1", new_features)

if failed:
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



