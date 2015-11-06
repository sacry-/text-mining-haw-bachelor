from es import EsSearcher


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
      "np" : prep["noun_phrases"],
      "ner" : prep["ner_tags"],
      "tokens" : prep["tokens"]
    }

  except Exception as e:
    print(str(e), " -> ", e.__doc__) 
    return None
