import os
import signal
import numpy as np
import csv

from sklearn.externals import joblib
from collections import defaultdict
from itertools import zip_longest

from preprocessing import TextNormalizer
from preprocessing import sentence_tokenize
from preprocessing import Preprocessor

from utils import flatten, unique, normalize_title


# Utils
def base_path():
  return "/".join(os.path.abspath(__file__).split("/")[:-1])

def model_path(model_name):
  return "{}/data/{}.txt".format(base_path(), model_name)

def bbc_path():
  return "{}/bbc_data".format(base_path())

def grouper(n, iterable, fillvalue=None):
  "grouper(3, 'ABCDEFG', 'x') --> ABC DEF Gxx"
  args = [iter(iterable)] * n
  return list(zip_longest(fillvalue=fillvalue, *args))


# Read
def get_csv(model_name):
  result = []
  with open(model_path(model_name), "r+") as fp:
    csv_reader = csv.reader(fp, delimiter=";")
    for line in csv_reader:
      result.append(line) 
  return result

def get_bbc_categories():
  return get_csv("categories")

def get_bbc_titles():
  return get_csv("titles")

def get_bbc_sents():
  return get_csv("sents")

def get_bbc_pos():
  return [list(grouper(2, x)) for x in get_csv("pos")]

def get_bbc_nouns():
  return get_csv("nouns")


# Dump
def tokenizer(text):
  return [word for sentence in sentence_tokenize( text ) for word in sentence]

def semantics(doc):
  tn = TextNormalizer(options=["keep_alpha"])
  normalized = tn.normalize(doc)
  prep = Preprocessor(normalized, tokenizer)
  pos = prep.pos_tags()
  nouns = prep.noun_phrases()
  return (
    list(sum(pos, ())), 
    nouns
  )

def bbc_parser(doc, category): 
  try:
    signal.alarm(10)
    s = doc.split("\n")
    title = s[0]
    _id = normalize_title(title)

    tn = TextNormalizer()
    pos, nouns, ners = semantics(doc)
    nouns = tn.fmap(nouns)
    
    paragraphs = []
    sentences = []
    for line in s[1:]:
      if not line:
        continue
      sentences += tn.fmap(sentence_tokenize(line))
      paragraphs.append( tn.normalize(line) )

    signal.alarm(0)
    return {
      "id" : _id,
      "title" : title,
      "sents" : sentences,
      "paras" : paragraphs,
      "pos" : pos,
      "nouns" : nouns
    }
  except Exception as e:
    print("Could not process article")
  signal.alarm(0)
  return None

def timeout_handler(signum, frame):
  print("Timeout: could not preprocess article")
  raise Exception("Timeout: article is not processable!")

def files_for_category(category):
  bbc = bbc_path()
  final_path = "{}/{}".format(bbc, category)
  files = ["{}/{}".format(final_path, f) for f 
           in os.listdir(final_path)]
  
  print("Category: '{}' with n = {} files".format(category, len(files)))

  return files

def stream_to_set(model_scheme, entry):
  with open(model_path(model_scheme), "a+") as fp:
    csv.writer(fp, delimiter=';').writerow(entry)

def stream_bbc_data_by_category(category):
  signal.signal(signal.SIGALRM, timeout_handler) 

  files = files_for_category(category)
  
  for file_path in files:

    fname = file_path.split("/")[-1]
    new_doc = None

    with open(file_path, 'r+') as data_file:

      try:
        new_doc = bbc_parser(data_file.read(), category)
      except:
        print("Failed {}".format(fname))
        new_doc = None

    if new_doc:
      yield new_doc

def stream(categories):
  for category in categories:
    for doc in stream_bbc_data_by_category(category):
      stream_to_set("categories", [category])
      stream_to_set("titles", [doc["title"]])
      stream_to_set("sents", doc["sents"])
      stream_to_set("pos", doc["pos"])
      stream_to_set("nouns", doc["nouns"])

if __name__ == "__main__":
  categories = ["business", "entertainment", "politics", "sport", "tech"]
  # stream(categories)

  l1 = len(get_bbc_categories())
  l2 = len(get_bbc_titles())
  l3 = len(get_bbc_sents())
  l4 = len(get_bbc_pos())
  l5 = len(get_bbc_nouns())
  print(l1, l1 == l2 == l3 == l4 == l5)



