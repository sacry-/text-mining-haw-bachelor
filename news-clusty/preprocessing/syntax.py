# coding: utf-8
import re
import enchant

from langdetect import detect

from nltk import word_tokenize
from nltk import data
from nltk import PorterStemmer
from nltk import WordNetLemmatizer
from nltk.corpus import stopwords

from textblob import TextBlob
from textblob_aptagger import PerceptronTagger
from textblob.np_extractors import ConllExtractor

from utils import flatten


STOPS = stopwords.words('english')
EN_US_DICT = enchant.Dict("en_US")
EN_GB_DICT = enchant.Dict("en_GB")
PORTER = PorterStemmer()
WN_LEMMATIZER = WordNetLemmatizer()
SENTENCE_DETECTOR = data.load('tokenizers/punkt/english.pickle')
TAGGER = PerceptronTagger()
EXTRACTOR = ConllExtractor()


def get_fast_blob(text):
  return TextBlob(text, pos_tagger=TAGGER, np_extractor=EXTRACTOR) 

def get_blob(text):
  return TextBlob(text, np_extractor=EXTRACTOR) 

def tokenize_string(doc):
  return word_tokenize(doc)

def sentence_tokenize(s):
  sentences = []
  for sentence in SENTENCE_DETECTOR.tokenize(s.strip()):
    try:
      if detect(sentence) == "en":
        sentences.append( sentence )
    except:
      pass
  return sentences

def tokenize(s):
  words = []
  for sentence in SENTENCE_DETECTOR.tokenize(s.strip()):
    try:
      if detect(sentence) == "en":
        words += word_tokenize(sentence)
    except:
      pass
  return words

def word_is_valid(word):
  return (
    word and
    (EN_US_DICT.check(word) and EN_GB_DICT.check(word)) and
    (len(word) > 0)
  )

def stem(tokens):
  return [stem for stem in 
            [PORTER.stem(token).lower() for token in tokens 
             if token and len(token) > 0] 
          if stem and len(stem) > 0]

def stemmatize(tokens):
  for token in tokens:
    if word_is_valid(token):
      yield PORTER.stem(WN_LEMMATIZER.lemmatize(token)).lower()

def lemmatize(tokens):
  for token in tokens:
    if word_is_valid(token):
      yield WN_LEMMATIZER.lemmatize(token).lower()


if __name__ == "__main__":
  s = "it was a very long and cool day. I am satisfied! Mr. crowley said this."
  tokens = tokenize(s)
  print(tokens)
  lemmas = list(lemmatize(tokens))
  print(lemmas)
  stemas = list(stemmatize(tokens))
  print(stemas)
  stems = stem(tokens)
  print(stems)
  sents = sentence_tokenize(s)
  print(sents)
  blob = get_blob(s)
  print(blob)




