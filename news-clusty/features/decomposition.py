import logging
import numpy as np

from nltk import data
from nltk import FreqDist

from gensim import matutils
from gensim import similarities
from gensim import models

from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import Normalizer
from sklearn.preprocessing import scale
from sklearn.decomposition import TruncatedSVD
from sklearn.decomposition import PCA
from sklearn.decomposition import FactorAnalysis
from sklearn.decomposition import NMF
from sklearn.decomposition import LatentDirichletAllocation

from utils.helpers import unique
from utils.helpers import flatten


'''
Name: Latent Semantic Analysis (LSA) / Latent Semantic Index (LSI)

Sources:
  - Christopher D. Manning, Prabhakar Raghavan and Hinrich Schütze (2008), 
  Introduction to Information Retrieval, Cambridge University Press, 
  Chapter 18: Matrix decompositions & latent semantic indexing 
'''
def lsa(x, topics=3):
  print("LSA with SVD, topics={}".format(topics))
  svd = TruncatedSVD(topics)
  x = to_ndarray(x)
  fitted = svd.fit(x)
  x_red = fitted.transform( x )

  explained_variance = svd.explained_variance_ratio_.sum()
  print("Explained variance of the SVD step: {}% and topics={}".format(
      int(explained_variance * 100), topics))

  x_norm = Normalizer(copy=False).fit_transform(x_red)
  return x_norm, fitted

def lsi_gensim(x, topics=20):
  pass



'''
Name: Latent Dirichlecht Allocation (LDA)

Sources:
  - Latent Dirichlet Allocation, D. Blei, A. Ng, M. Jordan, 2003
  - Online Learning for Latent Dirichlet Allocation, M. Hoffman, D. Blei, F. Bach, 2010
  - Stochastic Variational Inference, M. Hoffman, D. Blei, C. Wang, J. Paisley, 2013
'''
def lda(x, n_topics=20, max_iter=5):
  print("LDA sklearn: topics={}".format(n_topics))
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


def lda_gensim(x, topics=20, n_iter=150):
  pass


'''
Name: Non Negative Matrix Factorization (NMF)

Sources:
  - Christopher D. Manning, Prabhakar Raghavan and Hinrich Schütze (2008), 
  Introduction to Information Retrieval, Cambridge University Press, 
  Chapter 18: Matrix decompositions & latent semantic indexing 
'''
def nmf(x, n_topics):
  print("Non Negative Matrix Factorization (NMF), topics={}".format(n_topics))
  nmf = NMF(
    n_components=n_topics, 
    random_state=1, 
    alpha=.1, 
    l1_ratio=.5
  )
  x = to_ndarray(x)
  nmf_fitted = nmf.fit( x )
  return nmf_fitted.transform(x), nmf_fitted


'''
  Principal Component Analysis (PCA)
'''
def pca(x, dims=3):
  x = to_ndarray(x)
  s = scale(x, axis=0, with_mean=True, with_std=True, copy=True)
  pca_model = PCA(dims, copy=True, whiten=True)
  fitted = pca_model.fit(s)
  y = fitted.transform(s)
  print("PCA - Reduced dims from {} to {}".format( x.shape, y.shape ))
  return y, fitted


'''
  Factor Analysis (FA)
'''
def factor_analysis(x, dims=3):
  x = to_ndarray(x)
  s = scale(x, axis=0, with_mean=True, with_std=True, copy=True)
  fa_model = FactorAnalysis(n_components=dims, svd_method="lapack")
  fitted = fa_model.fit(s)
  y = fitted.transform(s)
  print("Factor Analysis - Reduced dims from {} to {}".format( x.shape, y.shape ))
  return y, fitted



def to_ndarray(x):
  if not isinstance(x, np.ndarray):
    return x.toarray()
  return x

if __name__ == "__main__":
  pass



