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



s_index = "20150701"
e_index = "20150708"
features = []
for feature in get_features(s_index, e_index):
  features.append( feature )
print(len(features))


sents = flatten( features )
freqs = FreqDist(sents)
freq_sents = [[token for token in text if freqs[token] > 1] 
              for text in features]

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

dictionary = corpora.Dictionary(freq_sents)
dictionary.save('/tmp/20150629.dict')

corpus = [dictionary.doc2bow(text) for text in freq_sents if text]
corpora.MmCorpus.serialize('/tmp/20150629.mm', corpus)

tfidf = models.TfidfModel(corpus, normalize=True)
corpus_tfidf = tfidf[corpus]

lsi = models.LsiModel(corpus_tfidf, id2word=dictionary, num_topics=300)
corpus_lsi = lsi[corpus_tfidf]

x = matutils.corpus2dense(corpus_lsi, num_terms=300, dtype=np.float32).T

print("sims#shape",x.shape)

x = reduce_dimensions(x, 3)
km = KMeans(init='k-means++',n_clusters=50, max_iter=40, n_init=20, copy_x=True)
km.fit(x)
centroids = km.cluster_centers_
c = km.labels_
k = km.n_clusters
cluster_plot_3d(x[0:400,:], centroids, c[0:400], k)

