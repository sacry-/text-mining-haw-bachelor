from matplotlib import pyplot as plt
from scipy.cluster.hierarchy import dendrogram, linkage, ward

from sklearn.preprocessing import scale, normalize
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from features import lsa, lda, pca
import numpy as np


def argmax(I, x, m):
  maxi = 10000000
  r_i, r_j = 0, 0
  for i in range(0, m):
    for j in range(i+1, m):
      if i != j and I[i] == 1 and I[j] == 1:
        if x[i][j] <= maxi:
          maxi = x[i][j]
          r_i, r_j = i, j
  return r_i, r_j

def cluster(y):
  x = np.array(y, copy=True)
  (m, _) = x.shape
  I = [1 for _ in range(0, m)]
  A = []
  for k in range(0, m-1):
    (i, j) = argmax(I, x, m)
    A.append( (i, j) )
    for z in range(0, m):
      sim = max(x[i][j], x[j][z])
      x[i][z] = sim
      x[z][i] = sim
    I[j] = 0
  return A

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
x_train = cosine_similarity(x_train)

print("    i  j")
for idx, (i, j) in enumerate(reversed(cluster(x_train))):
  print("{} | {}  {}".format(idx,i,j))

Z = linkage(x_train, "complete")

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

