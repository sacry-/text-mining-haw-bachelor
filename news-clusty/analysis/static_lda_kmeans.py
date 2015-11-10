import logging

import numpy as np

from sklearn.cluster import KMeans
from clustering import cluster_plot_2d
from clustering import cluster_plot_3d
from clustering import reduce_dimensions
from clustering import create_sample

from utils.helpers import unique
from utils.helpers import flatten
from clustering.feature_selection import get_features

from gensim import corpora, models, similarities, matutils
from nltk import data
from nltk import FreqDist
from pprint import pprint


def extract_features(s_index, e_index):
  features = {}
  ids = {}
  for index, _id, feature in get_features(s_index, e_index):
    if index in features:
      features[index].append( feature )
      ids[index].append( _id )
    else:
      features[index] = [ feature ]
      ids[index] = [ _id ]

  flattened = flatten(features.values())
  print(len(flattened))

  return features, ids


def do_lda(features_as_list):
  
  for index, feature in features_as_list:
    sents = flatten( feature )
    freqs = FreqDist(sents)
    freq_sents = [[token for token in text if freqs[token] > 1] 
                  for text in feature]

    dictionary = corpora.Dictionary(freq_sents)
    dictionary.save('/tmp/{}_dict.dict'.format( index ))

    corpus = [dictionary.doc2bow(text) for text in freq_sents if text]
    corpora.MmCorpus.serialize('/tmp/{}_corpus.mm'.format( index ), corpus)

    tfidf = models.TfidfModel(corpus, normalize=True)
    corpus_tfidf = tfidf[corpus]

    n_topics = int( len(feature) / 10 ) + 1
    lda_path = '/tmp/{}_lda.gensim'.format( index )
    lda_model = None
    corpus_lda = None

    try:
      lda_model = models.LdaModel.load( lda_path )
      corpus_lda = lda_model[corpus_tfidf]
    except:
      print("no corpus_lda found for: {}".format( lda_path ))

    if not lda_model:
      print( "  creating..." )

      logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

      lda_model = models.LdaModel(corpus_tfidf, id2word=dictionary, num_topics=n_topics, update_every=0, iterations=100, passes=20)
      lda_model.save( lda_path )
      corpus_lda = lda_model[corpus_tfidf]

    x = matutils.corpus2dense(corpus_lda, num_terms=n_topics, dtype=np.float32).T

    yield (x, lda_model, corpus_lda, corpus_tfidf, dictionary)


def cluster(x, num_clusters=1):
  km = KMeans(init='k-means++',n_clusters=num_clusters, max_iter=40, n_init=20, copy_x=True)
  km.fit(x)
  centroids = km.cluster_centers_
  c = km.labels_
  k = km.n_clusters
  return centroids, c, k

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

def print_doc(lda_model, doc, _id):
  print(_id)
  bow = dictionary.doc2bow(doc)
  some_docs = lda_model.get_document_topics(bow, minimum_probability=0.1)
  for doc, sim in sorted(some_docs, key=lambda x: -x[1])[1:]:
    print( lda_model.print_topic(doc, topn=10) )
    print("  sim:", sim)
  print("-"*40)

  return some_docs

if __name__ == "__main__":
  s_index = "20150701"
  e_index = "20150705"
  features, ids = extract_features(s_index, e_index)
  features_as_list = sorted(features.items(), key=lambda x: x[0])
  ids_as_list = flatten(list(map(lambda x: x[1], sorted(ids.items(), key=lambda x: x[0]))))

  c = 0
  t = {}
  for (x, lda, corpus_lda, corpus, dictionary) in do_lda(features_as_list):
    for index, feature_space in features_as_list:
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
      print(ids_as_list[_id])
    print("-"*40)





