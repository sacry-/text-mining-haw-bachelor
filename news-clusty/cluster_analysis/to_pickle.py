import os
import numpy as np

from collections import defaultdict
from preprocessing import TextNormalizer
from preprocessing import sentence_tokenize
from features import get_days
from utils.helpers import flatten, unique

from sklearn.externals import joblib



def base_path():
  return "/".join(os.path.abspath(__file__).split("/")[:-1])

def model_path(model_name):
  return "{}/data/{}.p".format(base_path(), model_name)

def dump_set(docs, write_to):
  print("dumping!")
  for index, docs in sorted(x_dict.items(), key=lambda y: y[0]):
    joblib.dump([index] + docs, write_to)
  print("dumped!")

'''
{ 
  "20151114" : [{
    "index" : "20151114",
    "id" : "clinton_in_iowa",
    "title" : "Clinton in Iowa. Nice!",
    "text" : "Clinton is in iowa",
    "keywords" : ["Clinton", "politics"],
    "pos" : [["Cliton", "NP"], ["politics", "NP"]],
    "sents" : ["Clinton is in iowa", "Nice!"],
    "ner" : ["Hilary Clinton"]
  },..]
} -> [ index, [id, len(keywords), *keywords, len(flatten(pos)), *flatten(pos), len(ner), *ner], ...]
'''
def get_sents_set(from_date, to_date=None):
  if not to_date:
    to_date = from_date

  tn = TextNormalizer()

  docs = defaultdict(list)
  for doc in get_days(from_date, to_date):
    doc["sents"] = sentence_tokenize(doc["text"], tn.normalize)
    p = [doc["id"], doc["title"]] + doc["sents"]
    docs[doc["index"]].append( p )

  return docs


def get_semantic_set(from_date, to_date=None):
  if not to_date:
    to_date = from_date

  tn = TextNormalizer()

  docs = defaultdict(list)
  for doc in get_days(from_date, to_date):
    keywords = list(doc["keywords"])
    pos = flatten(doc["pos"])
    ner = __ners(doc["ner"])
    nps = doc["np"]

    p = [
      doc["id"], 
      doc["title"]
    ]
    p += [len(keywords)] + keywords
    p += [len(pos)] + pos
    p += [len(ner)] + ner
    p += [len(nps)] + nps

    docs[doc["index"]].append( p )
  return docs

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
  base_date = "201507"
  post_fix = "_semantic"
  for idx, n in enumerate([str(i) for i in range(1,19+1)]):
    if len(n) == 1: 
      n = "0" + n 
    from_date = "{}{}".format(base_date, n)

    x_dict = get_semantic_set(from_date)

    write_to = model_path("{}{}".format(from_date, post_fix))
    dump_set(x_dict, write_to)

    print("loading!")
    x_n = joblib.load(write_to)
    print("{}. {}, {}".format(idx, x_n[0], len(x_n)))




