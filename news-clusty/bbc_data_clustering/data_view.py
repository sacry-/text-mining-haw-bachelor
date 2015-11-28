import csv

from itertools import zip_longest

from paths import model_path


def grouper(n, iterable, fillvalue=None):
  "grouper(3, 'ABCDEFG', 'x') --> ABC DEF Gxx"
  args = [iter(iterable)] * n
  return list(zip_longest(fillvalue=fillvalue, *args))

def group_2(seq):
  return [list(grouper(2, x)) for x in seq]

# Read
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

