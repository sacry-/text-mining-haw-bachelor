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
    feature = doc_features(doc)
    fcache.set(doc["index"], doc["id"], feature)
    yield feature

  for feature in docs_in_cache:
    yield feature


def doc_features(doc):
  tn = TextNormalizer()
  noun_tokens = flatten([tn.tnormalize(np) for np in doc["np"]])
  title_tokens = tn.tnormalize(doc["title"])
  keyword_tokens = flatten([tn.tnormalize(kw) for kw in doc["keywords"]])
  return noun_tokens + title_tokens + keyword_tokens


# Private
def _get_data(fcache, searcher, indices):
  cached = list( fcache.get_features( indices ) )
  cached_ids = {_id: feature for (_id, feature) in cached if feature}
  all_ids = list( _get_index_to_id(searcher, indices) )

  docs2get = [(index, _id) for index, _id in all_ids if not _id in cached_ids.keys()]
  docs_in_cache = [cached_ids[_id] for index, _id in all_ids if _id in cached_ids.keys()]

  print("Already got:", len(docs_in_cache), " docs from redis")
  print("Need to get:", len(docs2get), " docs from es")

  return docs2get, docs_in_cache

def _get_index_to_id(searcher, indices):
  for index in indices:
    for _id in searcher.ids_for_index(index, "article"):
      yield (index, _id)
      