# encoding: utf-8
import ast
import json                                              
import re
import hashlib
import time
import datetime
import collections


def timeit(method):
  def timed(*args, **kw):
    name = method.__name__
    ts = time.time()
    result = method(*args, **kw)
    te = time.time()
    print( '{:s} {:2.2f} sec'.format( name, te-ts ) )
    return result
  return timed
  
def normalize_title(s):
  s = s.strip().lower()
  s = re.sub('[\W\s]', '_', s)
  s = re.sub('\_+', '_', s)
  s = s.strip("_")
  return re.sub('\$', '', s)

def md5_hex(s):
  return hashlib.md5(url.encode()).hexdigest()

def evaluate(python_data):
  return ast.literal_eval(python_data)

def read_json(abs_path):
  with open(abs_path) as f:
    return evaluate(f.read())

def freadlines(abs_path):
  with open(abs_path) as f:
    return f.readlines()

def date_today():
  return datetime.date.today().strftime("%Y%m%d")

def flatten(seq):
  return list( flatten_gen(seq) )

def flatten_gen(seq):
  for item in seq:
    if is_iter(item):
      yield from flatten(item)
    else:
      yield item

def is_iter(x):
  is_iterable = isinstance(x, collections.Iterable) or (type(x) is tuple)
  return is_iterable and not isinstance(x, str)

def unique(seq):
  seen = set()
  seen_add = seen.add
  return [ x for x in seq if not (x in seen or seen_add(x)) ]

def flatmap(f, seq):
  for item in seq:
    yield from map(f, item)


if __name__ == "__main__":
  for a in map(lambda x: " ".join(x), flatten_gen(["abcd"])):
    print(a)

  