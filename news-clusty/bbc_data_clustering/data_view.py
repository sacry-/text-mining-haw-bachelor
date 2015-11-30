import csv

from itertools import zip_longest
from collections import defaultdict

from paths import model_path
from preprocessing import tokenize
from utils import flatten
from utils import unique


class BBCDocuments():


  def __init__(self):

    self._categories = None
    self._cat_to_id = None
    self._id_to_cat = None

    self._titles = None
    self._sents = None
    self._tokens = None

    self._pos = None
    self._nouns = None
    self._ners = None           

  def categories(self):
    if not self._categories:
      self._categories = get_categories() 
    return self._categories

  def cat_to_id(self):
    if not self._cat_to_id:
      self._cat_to_id = { cat: cat_id for cat_id, cat 
                         in enumerate(unique(self.categories())) }
    return self._cat_to_id

  def id_to_cat(self):
    return { v: k for k, v in self.cat_to_id().items() }

  def titles(self):
    if not self._titles:
      self._titles = get_titles()
    return self._titles

  def sents(self):
    if not self._sents:
      self._sents = get_sents()
    return self._sents

  def tokens(self):
    if not self._tokens:
      self._tokens = flatten( [ tokenize( x ) for x in self.sents() ] )
    return self._tokens

  def pos(self):
    if not self._pos:
      self._pos = get_pos()
    return self._pos

  def nouns(self):
    if not self._nouns:
      self._nouns = get_nouns()
    return self._nouns

  def ners(self):
    if not self._ners:
      self._ners = get_ners()
    return self._ners


class BBCData():

  def __init__(self, bbc, percent=0.8):
    self.bbc = bbc
    self.train = None
    self.test = None  

    self.index_train = None
    self.index_test = None  

    self.percent = percent     

    self._set_test_train_set()

  def itrain(self, _id):
    return self.index_train[_id]

  def itest(self, _id):
    return self.index_test[_id]

  def _set_test_train_set(self):
    print("Indexing and initializing training and test set")

    segments = defaultdict(list)
    index = defaultdict(list)

    for idx, (cat, sent) in enumerate(zip(self.bbc.categories(), self.bbc.sents())):
      segments[cat].append(sent)
      index[cat].append(idx)


    self.train = defaultdict(list)
    self.test = defaultdict(list)
    self.index_train = []
    self.index_test = []

    for cat, cat_id in self.bbc.cat_to_id().items():
      cat_sents = segments[cat]
      doc_ids = index[cat]

      train = int(len(cat_sents) * self.percent)
      self.train[cat].extend(cat_sents[:train])
      self.test[cat].extend(cat_sents[train:])

      self.index_train.extend(doc_ids[:train])
      self.index_test.extend(doc_ids[train:])


  def _labels(self, aset):    
    return flatten([ [self.bbc.cat_to_id()[cat] for _ in cat_sent] 
                      for cat, cat_sent in aset.items() ])

  def _data(self, aset):
    return flatten([ [". ".join(s) for s in cat_sent] 
                      for _, cat_sent in aset.items() ])
  
  def X(self):
    return self._data(self.train)

  def y(self):
    return self._labels(self.train)

  def X_test(self):
    return self._data(self.test)

  def y_test(self):
    return self._labels(self.test)



# Factories
def grouper(n, iterable, fillvalue=None):
  "grouper(3, 'ABCDEFG', 'x') --> ABC DEF Gxx"
  args = [iter(iterable)] * n
  return list(zip_longest(fillvalue=fillvalue, *args))

def group_2(seq):
  return [list(grouper(2, x)) for x in seq]

def get_csv_list(model_name):
  result = []
  with open(model_path(model_name), "r+") as fp:
    csv_reader = csv.reader(fp, delimiter=";")
    for line in csv_reader:
      result.append(line) 
  return result

def get_csv_single(model_name):
  result = []
  with open(model_path(model_name), "r+") as fp:
    csv_reader = csv.reader(fp, delimiter=";")
    for line in csv_reader:
      result.append(line[0]) 
  return result

def get_categories():
  return get_csv_single("categories")

def get_titles():
  return get_csv_single("titles")

def get_sents():
  return get_csv_list("sents")

def get_pos():
  return group_2(get_csv_list("pos"))

def get_ners():
  return group_2(get_csv_list("ners"))

def get_nouns():
  return get_csv_list("nouns")


if __name__ == "__main__":
  l1 = len(get_categories())
  l2 = len(get_titles())
  l3 = len(get_sents())
  l4 = len(get_pos())
  l5 = len(get_nouns())
  l6 = len(get_ners())
  print(l1, l1 == l2 == l3 == l4 == l5 == l6)

