from preprocessing import TextNormalizer
from clustering.cluster_data import get_days_by_list
from clustering.feature_cache import FeatureCache
from es import EsSearcher

from utils.helpers import unique
from utils.helpers import flatten


def get_features(s_index, e_index):
  fcache = FeatureCache()
  searcher = EsSearcher()

  indices = list( searcher.possible_indices(s_index, e_index) )
  docs2get, docs_in_cache = _get_data( fcache, searcher, indices )

  for doc in get_days_by_list( docs2get ):
    feature = without_nouns_features(doc)
    fcache.set(doc["index"], doc["id"], feature)
    yield doc["index"], doc["id"], feature

  for index, _id, feature in docs_in_cache:
    yield index, _id, feature


def noun_phrase_features(doc):
  tn = TextNormalizer()
  noun_tokens = flatten([tn.tnormalize(np) for np in doc["np"]])
  title_tokens = tn.tnormalize(doc["title"])
  keyword_tokens = flatten([tn.tnormalize(kw) for kw in doc["keywords"]])
  return unique(noun_tokens + title_tokens + keyword_tokens)

def without_nouns_features(doc):
  tn = TextNormalizer()
  tokens = [tn.normalize(word) for word, pos in doc["pos"] 
            if pos != 'NNP' and pos != 'NNPS']
  res = filter(lambda x: x and len(x.strip()) > 1, 
              [tn.normalize(token) for token in stem(tokens)]
        )
  return list( res )

from nltk import PorterStemmer

PORTER = PorterStemmer()
def stem(tokens):
  for token in tokens:
    if token and len(token) > 0:
      yield PORTER.stem(token).lower()

# Private
def _get_data(fcache, searcher, indices):
  cached = list( fcache.get_features( indices ) )
  cached_ids = {_id: feature for (_id, feature) in cached if feature}
  all_ids = list( _get_index_to_id(searcher, indices) )

  docs2get = [(index, _id) for index, _id in all_ids if not _id in cached_ids.keys()]
  docs_in_cache = [(index, _id, cached_ids[_id]) for index, _id in all_ids if _id in cached_ids.keys()]

  print("Already got:", len(docs_in_cache), " docs from redis")
  print("Need to get:", len(docs2get), " docs from es")

  return docs2get, docs_in_cache

def _get_index_to_id(searcher, indices):
  for index in indices:
    for _id in searcher.ids_for_index(index, "article"):
      yield (index, _id)
      