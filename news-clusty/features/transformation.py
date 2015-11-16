import lda as lda_alg
import numpy as np

from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import Normalizer
from sklearn.preprocessing import scale
from sklearn.decomposition import TruncatedSVD
from sklearn.decomposition import PCA
from sklearn.decomposition import NMF
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.random_projection import johnson_lindenstrauss_min_dim
from sklearn.random_projection import SparseRandomProjection

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer


# m = documents
# n = features
# d = all words accross documents

# m x d | very sparse in case d gets large
#        mouse cat dog
# doc1 :   2    1   0
# doc2 :   0    2   2
# ... 
def term_vector(features, 
                ngram=(1,1),
                max_feat=None, 
                max_df=0.95, min_df=2):
  vectorizer = CountVectorizer(
    analyzer='word', 
    ngram_range=ngram,
    stop_words = 'english',
    max_df=max_df,
    min_df=min_df,
    max_features=max_feat
  )
  fitted = vectorizer.fit( features )
  return fitted.transform( features ), fitted


def distance_matrix(features, 
                    ngram=(1,1),
                    max_feat=None, 
                    max_df=0.8, min_df=0.1):
  vectorizer = TfidfVectorizer(
    analyzer='word', 
    ngram_range=ngram,
    stop_words = 'english',
    max_features=max_feat,
    max_df=max_df,
    min_df=min_df, 
    norm='l2', 
    use_idf=False,
    sublinear_tf=False
  )
  fitted = vectorizer.fit( features )
  return fitted.transform( features ), fitted



# m x d | very sparse in case d gets large
# transforms bag of words to a sparse
# tfidf transformation
def tfidf(features, 
          ngram=(1,1),
          max_feat=None, 
          max_df=0.8, min_df=0.1):
  vectorizer = TfidfVectorizer(
    analyzer='word', 
    ngram_range=ngram,
    stop_words = 'english',
    max_features=max_feat,
    max_df=max_df,
    min_df=min_df, 
    use_idf=True,
    smooth_idf=True,
    sublinear_tf=False
  )
  fitted = vectorizer.fit( features )
  return fitted.transform( features ), fitted

def corpus_gensim(x):
  pass

# n x m
def lsa(x, topics=3):
  svd = TruncatedSVD(topics)
  normalizer = Normalizer(copy=False)
  lsa_model = make_pipeline(svd, normalizer)
  x_red = lsa_model.fit_transform( to_ndarray(x) )

  explained_variance = svd.explained_variance_ratio_.sum()
  print("Explained variance of the SVD step: {}% and topics={}".format(
      int(explained_variance * 100), topics))

  return x_red, None

def lsi_gensim(x, topics=20):
  pass


def lda_sklearn(x, n_topics=20, max_iter=5):
  ldam = LatentDirichletAllocation(
    n_topics=n_topics, 
    max_iter=max_iter,
    learning_method='online',
    learning_offset=50.,
    random_state=0
  )
  x = to_ndarray(x)
  lda_fitted = ldam.fit( x )
  return lda_fitted.transform( x ), lda_fitted


def lda(x, topics=20, n_iter=100):
  lda_model = lda_alg.LDA(n_topics=topics, n_iter=n_iter, random_state=1)
  x = to_ndarray(x)
  lda_fitted = lda_model.fit( x )
  return lda_fitted.transform( x ), lda_fitted


def lda_gensim(x, topics=20, n_iter=150):
  pass


def nmf(x, n_topics):
  nmf = NMF(
    n_components=n_topics, 
    random_state=1, 
    alpha=.1, 
    l1_ratio=.5
  )
  x = to_ndarray(x)
  nmf_fitted = nmf.fit( x )
  return nmf_fitted.transform(x), nmf_fitted


def pca(x, dims=3):
  x = to_ndarray(x)
  s = scale(x, axis=0, with_mean=True, with_std=True, copy=True)
  pca_model = PCA(dims, copy=True, whiten=True)
  y = pca_model.fit_transform(s)
  print("Reduced dims from {} to {}".format( x.shape, y.shape ))
  return y


def random_projections(x):
  x = to_ndarray(x)
  rp_fitted = SparseRandomProjection().fit( x )
  return rp_fitted.transform(x), rp_fitted


def to_ndarray(x):
  if not isinstance(x, np.ndarray):
    return x.toarray()
  return x

if __name__ == "__main__":
  pass



