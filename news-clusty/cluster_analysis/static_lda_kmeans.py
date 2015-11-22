import logging
import numpy as np

from clustering import cluster_plot_2d
from clustering import cluster_plot_3d
from clustering import kmeans

from features import indexed_features
from features import single_lda
from features import consecutive_lda
from features import pca



def list_topic(c, ids_as_list):
  clusters = {}
  for idx, el in enumerate(c):
    if not el in clusters:
      clusters[el] = []
    clusters[el].append( idx )
  for key, doc in clusters.items():
    for _id in doc[:5]:
      print(ids_as_list[_id])
    print("-"*40)


if __name__ == "__main__":
  s_index = "20150701"
  e_index = "20150705"
  features, ids = indexed_features(s_index, e_index)
  
  c = 0
  t = {}
  for (x, lda, corpus_lda, corpus, dictionary) in consecutive_lda(features):
    for index, feature_space in features:
      for doc in feature_space:
        bow = dictionary.doc2bow(doc)
        topics = lda.get_document_topics(bow, minimum_probability=0.1)
        for topicid, score in topics:
          if topicid in t:
            if not c in t[topicid]:
              t[topicid].append( c )
          else:
            t[topicid] = [c]
        c += 1
    break

  for topic, _ids in t.items():
    if len(_ids) > 20:
      continue
    print(topic)
    for _id in _ids:
      print(ids[_id])
    print("-"*40)





