from es import EsSearcher

from features.cache import Cache


def get_days_by_list(index_id_pairs):
  searcher = EsSearcher()
  for (index, _id) in index_id_pairs:
    article = searcher.article_at(index, "article", _id)
    doc = new_doc( searcher, article )
    if doc: 
      yield doc


def get_days(s_index, e_index):
  searcher = EsSearcher()
  for article in searcher.articles_from_to(s_index, e_index):
    doc = new_doc( searcher, article )
    if doc: 
      yield doc


def get_features(s_index, e_index, feature_func):
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


def features_to_cache(s_index, e_index, feature_func):
  if not feature_func:
    feature_func = without_noun_func

  fcache = Cache()
  searcher = EsSearcher()

  indices = list( searcher.possible_indices(s_index, e_index) )
  docs2get, docs_in_cache = __get_data( fcache, searcher, indices )

  for doc in get_days_by_list( docs2get ):
    feature = feature_func(doc)
    fcache.set(doc["index"], doc["id"], feature)


def features_from_cache(s_index, e_index):
  fcache = Cache()
  searcher = EsSearcher()

  indices = list( searcher.possible_indices(s_index, e_index) )
  _, docs_in_cache = __get_data( fcache, searcher, indices )

  for index, _id, feature in docs_in_cache:
    yield index, _id, feature


# Private
def new_doc(searcher, article):
  _id = article.meta.id
  index = article._index

  try:  
    prep = searcher.prep_for_index(index, _id)
    return {
      "id" : _id,
      "index" : index,
      "title" : article.title,
      "keywords" : article.meta_keywords,
      "pos" : prep["pos_tags"],
      "np" : prep["noun_phrases"],
      "ner" : prep["ner_tags"],
      "tokens" : prep["tokens"]
    }

  except Exception as e:
    print(str(e), " -> ", e.__doc__) 
    return None


def __get_data(fcache, searcher, indices):
  cached_ids = {_id: feature for (_id, feature) in fcache.get_features( indices )
                if feature}

  all_ids = list( __get_index_to_id(searcher, indices) )

  docs2get = [(idx, _id) for (idx, _id) in all_ids
              if not _id in cached_ids.keys()]

  docs_in_cache = [(index, _id, cached_ids[_id]) for index, _id in all_ids 
                   if _id in cached_ids.keys()]

  print("Already got:", len(docs_in_cache), " docs from redis")
  print("Need to get:", len(docs2get), " docs from es")

  return docs2get, docs_in_cache


def __get_index_to_id(searcher, indices):
  for index in indices:
    for _id in searcher.ids_for_index(index, "article"):
      yield (index, _id)


if __name__ == "__main__":
  pass


  