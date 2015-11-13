from nltk import PorterStemmer

from es import EsSearcher
from preprocessing import TextNormalizer

from features.raw_doc import get_days_by_list
from features.cache import Cache

from utils.helpers import unique
from utils.helpers import flatten



def flattened_features( s_index, e_index, feature_func=None ):
  features, ids = hashed_features(s_index, e_index)
  features_as_list = list( map(lambda e: " ".join(e), __unfold( features.items() )) )
  ids_as_list = __unfold( ids.items() )
  return features_as_list, ids_as_list

def indexed_features( s_index, e_index, feature_func=None ):
  features, ids = hashed_features(s_index, e_index)
  features_as_list = list(sorted(features.items(), key=lambda x: x[0]))
  ids_as_list = __unfold( ids.items() )
  return features_as_list, ids_as_list

def hashed_features(s_index, e_index, feature_func=None):
  features = {}
  ids = {}
  for index, _id, feature in get_features(s_index, e_index, feature_func):
    if index in features:
      features[index].append( feature )
      ids[index].append( _id )
    else:
      features[index] = [ feature ]
      ids[index] = [ _id ]

  flattened = flatten(features.values())
  print(len(flattened))

  return features, ids

def get_features(s_index, e_index, feature_func=None):
  if not feature_func:
    feature_func = without_noun_func

  fcache = Cache()
  searcher = EsSearcher()

  indices = list( searcher.possible_indices(s_index, e_index) )
  docs2get, docs_in_cache = __get_data( fcache, searcher, indices )

  for doc in get_days_by_list( docs2get ):
    feature = feature_func(doc)
    fcache.set(doc["index"], doc["id"], feature)
    yield doc["index"], doc["id"], feature

  for index, _id, feature in docs_in_cache:
    yield index, _id, feature


# initial feature strategies
def noun_phrase_func(doc):
  tn = TextNormalizer()
  noun_tokens = flatten([tn.tnormalize(np) for np in doc["np"]])
  title_tokens = tn.tnormalize(doc["title"])
  keyword_tokens = flatten([tn.tnormalize(kw) for kw in doc["keywords"]])
  return unique(noun_tokens + title_tokens + keyword_tokens)

def without_noun_func(doc):
  tn = TextNormalizer()
  tokens = [tn.normalize(word) for word, pos in doc["pos"] 
            if pos != 'NNP' and pos != 'NNPS']
  res = filter(lambda x: x and len(x.strip()) > 1, 
              [tn.normalize(token) for token in __stem__(tokens)]
        )
  return list( res )


# private Helpers
def __unfold(data):
  return flatten(list(map(lambda x: x[1], sorted(data, key=lambda x: x[0]))))

__PORTER__ = PorterStemmer()
def __stem__(tokens):
  for token in tokens:
    if token and len(token) > 0:
      yield __PORTER__.stem(token).lower()

# Private
def __get_data(fcache, searcher, indices):
  cached = list( fcache.get_features( indices ) )
  cached_ids = {_id: feature for (_id, feature) in cached if feature}
  all_ids = list( __get_index_to_id(searcher, indices) )

  docs2get = [(index, _id) for index, _id in all_ids if not _id in cached_ids.keys()]
  docs_in_cache = [(index, _id, cached_ids[_id]) for index, _id in all_ids if _id in cached_ids.keys()]

  print("Already got:", len(docs_in_cache), " docs from redis")
  print("Need to get:", len(docs2get), " docs from es")

  return docs2get, docs_in_cache

def __get_index_to_id(searcher, indices):
  for index in indices:
    for _id in searcher.ids_for_index(index, "article"):
      yield (index, _id)
      

if __name__ == "__main__":
  pass

