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

from features import tfidf_vector


def n_nyms(nyms, n):
  if nyms:
    return nyms[:n]
  return []

def n_synssets(w, n):
  return n_nyms( wn.synsets(w, pos=wn.NOUN), n )

def n_hyponyms(syn, n):
  return n_nyms( syn.hyponyms(), n )

def n_hypernyms(syn, n):
  return n_nyms( syn.hypernyms(), n )

def lemma_names(nyms):
  return flatten( 
    [[y.name() for y in syn.lemmas()] 
      for syn in nyms]
  )

def synsets_for_word(word, n):
  syns = n_synssets(word, n)
  hypers = flatten( [n_hypernyms(syn, 1) for syn in syns] )[:n]
  hypos = flatten( [n_hyponyms(syn, 1) for syn in syns] )[:n]
  return flatten([
    syns, 
    hypers,
    hypos,
  ])

def unique_nouns(nouns):
  unique_nouns = set([])
  for noun in nouns:
    unique_nouns.update(tokenize(noun))
  return unique_nouns

def get_synsets(nouns):
  synsets = []
  for noun in nouns:
    synsets.append( synsets_for_word( noun, n=5 ) )
  return synsets

def paired_sets(synsets):
  for noun_set in synsets:
    for id1, syn1 in enumerate(noun_set):
      for id2, syn2 in enumerate(noun_set):
        if id1 != id2:
          yield (syn1, syn2)

def argmax(group):
  result = set([])
  for s1 in group:
    for s2 in group:
      if s1 != s2:
        result.update( 
          lemma_names( s1.lowest_common_hypernyms(s2) )
        )
  return result

def cut(seq, max_df=0.8, min_df=1):
  counted = sorted(Counter(seq).items(), key=lambda x: x[1]) 
  min_dfd = [(x, c) for (x, c) in counted if c >= min_df]
  return dict(min_dfd[:int(len(min_dfd) * max_df)])

def peek(mapping):
  for k, v in list(mapping.items())[:5]:
    print(" ", k, v)
  print("-"*40)

def wordnet_projection( bbc ):
  tn = TextNormalizer()

  for idx, entry in enumerate(bbc.nouns()):
    nouns = unique_nouns( entry )
    synsets = get_synsets( nouns )

    mapping = defaultdict(list)
    total = []
    for noun, group in zip(nouns, synsets):
      for maximized in argmax(group):
        mapping[noun].append( maximized )
        total.append(maximized)

    normalized = cut( total, max_df=0.7, min_df=1 )

    final_mapping = defaultdict(list)  
    for noun, group in mapping.items():
      for syn in group:
        if syn in normalized:
          final_mapping[noun].append(syn)

    doc = tn.tnormalize( " ".join( 
      ["{} {}".format(k, " ".join(v)) for k, v in final_mapping.items()] 
    ))

    yield (idx, doc)


def stream_wordnet_projection():
  bbc = BBCDocuments()
  for (idx, doc) in wordnet_projection( bbc ):
    stream_to_set("wordnet", doc)
    print(idx, bbc.titles()[idx])
    print(" ", doc)

if __name__ == "__main__":
  bbc = BBCDocuments()
  bbc_data = BBCData(bbc, percent=0.8, data_domain=bbc.wordnet())
  X = bbc_data.X()
  X, vsmodel = tfidf_vector( X, ngram=(1,1), max_df=0.8, min_df=3 )
  print("X: {}".format(X.shape))

