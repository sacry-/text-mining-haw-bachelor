from nltk import PorterStemmer
from collections import defaultdict

from preprocessing import TextNormalizer

from utils.helpers import unique
from utils.helpers import flatten

from features.raw_doc import get_features


def flattened_features( s_index, e_index, feature_func=None ):
  if not feature_func:
    feature_func = without_noun_func

  features, ids = hashed_features(s_index, e_index, feature_func)
  features_as_list = [" ".join(e) for e in __unfold(features.items())]
  ids_as_list = __unfold( ids.items() )

  return features_as_list, ids_as_list

def indexed_features( s_index, e_index, feature_func=None ):
  if not feature_func:
    feature_func = without_noun_func

  features, ids = hashed_features(s_index, e_index, feature_func)
  features_as_list = __sort_by_index( features.items() )
  ids_as_list = __unfold( ids.items() )
  return features_as_list, ids_as_list

def hashed_features(s_index, e_index, feature_func):
  features = defaultdict(list)
  ids = defaultdict(list)
  for index, _id, feature in get_features(s_index, e_index, feature_func):
    features[index].append( feature )
    ids[index].append( _id )
  return features, ids


def without_noun_func(doc):
  tn = TextNormalizer()
  return __stem__( tn.fmap( 
    [word for word, pos in doc["pos"] 
     if pos != 'NNP' and pos != 'NNPS'] + __ners(doc["ner"])
  ))

def noun_phrase_func(doc):
  tn = TextNormalizer()
  noun_tokens = tn.fmap(doc["np"])
  title_tokens = tn.tnormalize(doc["title"])
  keyword_tokens = tn.fmap(doc["keywords"])
  ners = __ners(doc["ner"])
  return __stem__( 
    unique(noun_tokens + title_tokens + keyword_tokens + ners) 
  )

def __sort_by_index(seq):
  return sorted(seq, key=lambda x: x[0])

def __unfold(data):
  return flatten(
    [y for _, y in __sort_by_index(data)]
  )

__PORTER__ = PorterStemmer()
def __stem__(tokens):
  return [stem for stem in 
            [__PORTER__.stem(token).lower() for token in tokens 
             if token and len(token) > 0] 
          if stem and len(stem) > 0]

def __ners(seq):
  r = []
  for entities in seq:
    entities = flatten( flatten( entities ) )
    fst = [x for idx, x in enumerate(entities) 
           if idx % 2 == 0]
    snd = [x for idx, x in enumerate(entities) 
           if (idx + 1) % 2 == 0]
    if all(x==snd[0] for x in snd):
      r.append( " ".join(fst) )
  return unique( r )


if __name__ == "__main__":
  pass

