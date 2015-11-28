import csv

from itertools import zip_longest

from paths import model_path


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


if __name__ == "__main__":
  l1 = len(get_bbc_categories())
  l2 = len(get_bbc_titles())
  l3 = len(get_bbc_sents())
  l4 = len(get_bbc_pos())
  l5 = len(get_bbc_nouns())
  print(l1, l1 == l2 == l3 == l4 == l5)


