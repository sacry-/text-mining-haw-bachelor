from es import EsSearcher


def cat_indices(_from=None, _to=None, doctype="article"):
  es = EsSearcher()

  print("index:", doctype)
  if not _from and not _to:
    
    article_count = es.count_all("article")
    preped_article_count = es.count_all("article", {"match" : { "preprocessed" : True}})

    print("  article count:",article_count)
    print("  preped article count:",preped_article_count)
    print("  missing:", article_count - preped_article_count)

  elif not _to:
    print( " ", _from, "->", es.count_index(_from, doctype) )

  else:
    total = 0
    for day_idx, index in enumerate(es.possible_indices(_from, _to)):
      c = es.count_index(index, doctype)
      total += c
      print( "  {}.".format(day_idx+1), index, "->", c )
    print( "   ", "total ->", total)

