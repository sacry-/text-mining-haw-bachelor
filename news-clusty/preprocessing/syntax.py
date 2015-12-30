# coding: utf-8
import re
import enchant

from langdetect import detect

from nltk import word_tokenize
from nltk import data
from nltk import PorterStemmer
from nltk import WordNetLemmatizer
from nltk.corpus import stopwords
from nltk.corpus import wordnet as wn

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


def stemmatize(pos_tags):
  for token, tag in pos_tags:
    tag = morph(tag)
    if word_is_valid(token):
      lemma = WN_LEMMATIZER.lemmatize(token, tag)
      
      if not lemma:
        lemma = token

      yield PORTER.stem(lemma).lower()


MORPHY_MAP = {
  'nn': wn.NOUN,
  'jj': wn.ADJ,
  'vb': wn.VERB,
  'rb': wn.ADV
}

def morph(key):
  if not key:
    return wn.NOUN
  key = key.lower()
  if key in MORPHY_MAP:
    return MORPHY_MAP[key]
  return wn.NOUN

def lemmatize(pos_tags):
  for token, tag in pos_tags:
    tag = morph(tag)
    if word_is_valid(token):
      yield WN_LEMMATIZER.lemmatize(token, tag).lower()


if __name__ == "__main__":
  s = "It was a very long and cool day. 'I am satisfied!' Mr. crowley said. Have you heard that Google held a lot of coding competitions in the past?"
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




