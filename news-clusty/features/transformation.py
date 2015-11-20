import numpy as np

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import HashingVectorizer

from gensim import corpora


'''
  m = documents
  n = features
  d = all words accross documents

  m x d | very sparse in case d gets large
          mouse cat dog
  doc1 :   2    1   0
  doc2 :   0    2   2
  ...
''' 
def term_vector(features, 
                ngram=(1,1),
                n_features=None, 
                max_df=0.95, 
                min_df=2):

  vectorizer = CountVectorizer(
    analyzer='word', 
    ngram_range=ngram,
    stop_words = 'english',
    max_df=max_df,
    min_df=min_df,
    max_features=n_features
  )
  fitted = vectorizer.fit( features )
  return fitted.transform( features ), fitted


'''
  m = documents
  n = features

  m x m
          doc1 doc2 ..
  doc1 :   1    0.5
  doc2 :   0.5   1   
  ...
''' 
def distance_matrix(features, 
                    ngram=(1,1),
                    n_features=None, 
                    max_df=0.95, 
                    min_df=0.1):

  vectorizer = TfidfVectorizer(
    analyzer='word', 
    ngram_range=ngram,
    stop_words = 'english',
    max_features=n_features,
    max_df=max_df,
    min_df=min_df, 
    norm='l2', 
    use_idf=False,
    sublinear_tf=False
  )
  fitted = vectorizer.fit( features )
  return fitted.transform( features ), fitted


'''
  m x d | very sparse in case d gets large
  transforms bag of words to a sparse
  tfidf transformation
'''
def tfidf(features, 
          ngram=(1,1),
          n_features=None, 
          max_df=0.95, min_df=1):

  vectorizer = TfidfVectorizer(
    analyzer='word', 
    ngram_range=ngram,
    stop_words = 'english',
    max_features=n_features,
    max_df=max_df,
    min_df=min_df, 
    use_idf=True,
    smooth_idf=True,
    sublinear_tf=False
  )
  fitted = vectorizer.fit( features )
  return fitted.transform( features ), fitted


'''
  Hash Vector
''' 
def hash_vector(features, 
                ngram=(1,1),
                n_features=1048576, 
                **kwargs):
  vectorizer = HashingVectorizer(
    analyzer='word', 
    ngram_range=ngram,
    stop_words = 'english',
    norm='l2', 
    non_negative=True, 
    lowercase=True,
    n_features=n_features
  )
  fitted = vectorizer.fit( features )
  return fitted.transform( features ), fitted


'''
Persisted Corpus by gensim
'''
def corpus_gensim(x):
  pass



if __name__ == "__main__":
  pass



