from matplotlib import pyplot as plt
from scipy.cluster.hierarchy import dendrogram, linkage, ward

from sklearn.preprocessing import scale, normalize
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from features import lsa, lda, pca

import numpy as np


features = np.array([
  "document clustering",
  "cluster documents",
  "unsupervised clustering",
  "cluster documents",
  "compute clusters",
  "text clustering",
  "text clusters",
  "supervised clustering",
  "unsupervised clustering",
  "document text",
  "text document",
])

vectorizer = TfidfVectorizer(
  analyzer='word', 
  ngram_range=(1,2),
  stop_words = 'english'
)
x_train = vectorizer.fit_transform( features )
x_train, _ = lsa(x_train, 4)
x_train = scale(x_train)
Z = linkage(x_train, "ward")

plt.figure(facecolor='white')
plt.title('Hierarchical Clustering Dendrogram')
plt.xlabel('sample index')
plt.ylabel('distance')
dendrogram(
    Z,
    labels=[f.replace(" ", "\n") for f in features],
    leaf_font_size=2,
)
plt.xticks(rotation=90)
plt.subplots_adjust(bottom=0.4)
plt.show()


