# coding: utf-8
import re
import enchant # pip install pyenchant
from nltk import word_tokenize
from nltk import data
from nltk import PorterStemmer
from nltk import WordNetLemmatizer
from nltk.corpus import stopwords

STOPS = stopwords.words('english')
EN_US_DICT = enchant.Dict("en_US")
EN_GB_DICT = enchant.Dict("en_GB")
PORTER = PorterStemmer()
WN_LEMMATIZER = WordNetLemmatizer()
SENTENCE_DETECTOR = data.load('tokenizers/punkt/english.pickle')


'''
  CC Coordinating conjunction
  CD Cardinal number
  DT Determiner
  EX Existential there
  FW Foreign word
  IN Preposition or subordinating conjunction
  JJ Adjective
  JJR Adjective, comparative
  JJS Adjective, superlative
  LS List item marker
  MD Modal
  NN Noun, singular or mass
  NNS Noun, plural
  NNP Proper noun, singular
  NNPS Proper noun, plural
  PDT Predeterminer
  POS Possessive ending
  PRP Personal pronoun
  PRP$ Possessive pronoun
  RB Adverb
  RBR Adverb, comparative
  RBS Adverb, superlative
  RP Particle
  SYM Symbol
  TO to
  UH Interjection
  VB Verb, base form
  VBD Verb, past tense
  VBG Verb, gerund or present participle
  VBN Verb, past participle
  VBP Verb, non­3rd person singular present
  VBZ Verb, 3rd person singular present
  WDT Wh­determiner
  WP Wh­pronoun
  WP$ Possessive wh­pronoun
  WRB Wh­adverb
'''


def is_num(s):
  try:
    float(s)
    return True
  except ValueError:
    return False

def is_noisy(x):
  if not x:
    return False
  x = x.strip().lower()
  return (
    # not be in stopwords
    x in STOPS or 
    # not be in specials
    re.match('(^\W+|\W+$)', x) or 
    # should be larger than 1 i.e. not "a" etc.
    len(x) <= 1
  )

def word_is_valid(word):
  return (
    # word should not be none
    word and 
    # word should be valid in a english dictionary
    (EN_US_DICT.check(unicode(word)) and EN_GB_DICT.check(unicode(word))) or
    # average word length for biology assuming that the english word_list
    # does not contain specialized biology words
    (len(word) > 0)
  )

def remove_noise(tokens):
  return [remove_special(token) for token in tokens if not is_noisy(token)]

def remove_special(token):
  return re.sub("[\W\s]", "", token)

def sentence_tokenize(s):
  sentences = []
  for sentence in SENTENCE_DETECTOR.tokenize(s.strip()):
    sentences.append( word_tokenize(sentence) )
  return sentences

def stemmatize(tokens): # work heavy!
  for token in tokens:
    if word_is_valid(token):
      yield PORTER.stem(WN_LEMMATIZER.lemmatize(token)).lower()

def lemmatize(tokens):
  for token in tokens:
    if word_is_valid(token):
      yield WN_LEMMATIZER.lemmatize(token).lower()

def stem(tokens):
  for token in tokens:
    if word_is_valid(token):
      yield PORTER.stem(token).lower()


if __name__ == "__main__":
  pass




