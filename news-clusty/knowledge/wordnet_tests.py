# encoding: utf-8
import enchant 
from langdetect import detect
from nltk.corpus import brown, reuters
from nltk.corpus import wordnet as wn
from nltk import word_tokenize
from nltk.corpus import stopwords
from nltk import data

from textblob import TextBlob
from textblob_aptagger import PerceptronTagger
from textblob.np_extractors import ConllExtractor

STOPS = stopwords.words('english')
SENTENCE_DETECTOR = data.load('tokenizers/punkt/english.pickle')
TAGGER = PerceptronTagger()
EXTRACTOR = ConllExtractor()
EN_US_DICT = enchant.Dict("en_US")
EN_GB_DICT = enchant.Dict("en_GB")

def sentence_tokenize(s, f=lambda x: x):
  sentences = []
  for sentence in SENTENCE_DETECTOR.tokenize(s.strip()):
    try:
      if detect(sentence) == "en":
        words = word_tokenize(sentence)
        sentences.append( f(words) )
    except:
      pass
  return sentences

def remove_stopwords( words ):
  result = []
  for word in words:
    if not word.strip() in STOPS:
      result.append( word )
  return result

def as_tokens(text, f=lambda x: x):
  return [word for sentence in sentence_tokenize( text, f ) for word in sentence]

def splitter(seq):
  seq_ = []
  for e in seq:
    seq_ += e.split(" ")
  return seq_

def hyperfy(bag):
  lowest_hypernyms = []
  for (t1, t2) in zip(bag, bag[1:]):
    s1 = wn.synsets(t1)
    s2 = wn.synsets(t2)

    for (syn1, syn2) in zip(s1, s2):
      hyper = syn1.lowest_common_hypernyms(syn2)
      lowest_hypernyms += hyper
      
  return list(set(lowest_hypernyms))

def get_nouns( text ):
  t = sentence_tokenize(text)
  text = " ".join(map(lambda x: " ".join(x), t))
  blob = TextBlob(text)
  print(blob.noun_phrases)
  return blob.noun_phrases


def lemma_names(syns):
  return [syn.lemmas()[0].name() for syn in syns]

def hyper_hierarchy(syns, depth):
  for s in syns:
    if depth > 0:
      yield from hyper_hierarchy( s.hypernyms(), depth - 1 )
    yield s

def gloss(syns):
  fst = syns[0]
  hypers = list( hyper_hierarchy(syns, 2) )
  new_syns = hypers[:hypers.index(fst)+1]
  return new_syns, lemma_names( new_syns )

if __name__ == "__main__":
  d = wn.synsets("dog")[0]
  c = wn.synsets("cat")[0]
  print(d.member_holonyms())
  print(d.member_meronyms())



