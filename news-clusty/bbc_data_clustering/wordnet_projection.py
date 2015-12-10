#encoding: UTF-8

from nltk.corpus import wordnet as wn
from collections import Counter
from collections import defaultdict
from utils import flatten
from utils import unique
from preprocessing import tokenize
from preprocessing import TextNormalizer
from data_view import BBCDocuments
from data_view import BBCData
from data_view import grouper
from data_import import stream_to_set

from preprocessing import lemmatize


# Experimental
def prune(seq, max_df=0.8, min_df=1):
  counted = sorted(Counter(seq).items(), key=lambda x: x[1])
  min_dfd = [x for (x, c) in counted if c >= min_df]
  return min_dfd[:int(len(min_dfd) * max_df)]

def commons(synset1, synset2, depth=2):
  result = []
  for i, syn1 in enumerate(hyper_hierarchy(synset1, depth)):
    for j, syn2 in enumerate(hyper_hierarchy(synset2, depth)):
      if i != j:
        result += syn1.lowest_common_hypernyms(syn2)
  return prune( [lemma_name(x) for x in result] )

# Helpers
def unique_nouns(nouns):
  unique_nouns = set([])
  for noun in nouns:
    unique_nouns.update(tokenize(noun))
  return unique_nouns

def noun_tokens(nouns):
  return tokenize(" ".join(nouns))

def lemma_names(syns):
  return [syn.lemmas()[0].name().lower() for syn in syns]

def hyper_hierarchy(syns, depth):
  for s in syns:
    if depth > 0:
      yield from hyper_hierarchy( s.hypernyms(), depth - 1 )
    yield s

def hypo_hierarchy(syns, depth):
  for s in syns:
    if depth > 0:
      yield from hypo_hierarchy( s.hyponyms(), depth - 1 )
    yield s

def gloss(noun, depth):
  syns = wn.synsets(noun)
  if not syns:
    return [], []

  fst = syns[0]
  nyms = list( hyper_hierarchy(x, depth) )
  new_syns = nyms[:nyms.index(fst)+1]
  return new_syns, lemma_names( new_syns )

def lemma_name(syn):
  return syn.name().split(".")[0]


# Wordnet Strategies
def wordnet_hypernyms(bbc, depth=1):

  def hypers(nouns, depth):
    result = set([])
    for noun in nouns: 
      _, lemmas = gloss(noun, depth)
      result.update( lemmas )
    return result

  for idx, nouns in enumerate(bbc.nouns()):    
    yield idx, hypers(sent, depth)


def wordnet_fst_hyper(bbc):

  def firsts(nouns):
    result = []
    for noun in nouns: 
      synset = wn.synsets(word)
      if synset:
        fst = synset[0].hypernyms()
        if fst:
          result.append( lemma_name(fst[0]) )
    return result

  for idx, nouns in enumerate(bbc.nouns()):    
    yield idx, firsts(sent)


def wordnet_lemmatize(bbc):
  
  def convert_sents(sent):
    s = flatten(map(lambda x: lemmatize(tokenize(x)), sent))
    return [x for x in s if len(x) > 1]

  for idx, sent in enumerate(bbc.sents()):
    yield idx, convert_sents(sent)


# Main
def stream_wordnet_projection( bbc ):
  for idx, doc in wordnet_lemmatize( bbc ):
    stream_to_set("wordnet", doc)
    print(idx, bbc.titles()[idx])
    print(" ", doc)

if __name__ == "__main__":
  bbc = BBCDocuments()
  # stream_wordnet_projection( bbc )



