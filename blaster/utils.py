# encoding: utf-8
import ast
import json                                              
import re
import hashlib
import time
import datetime


def timeit(method):
  def timed(*args, **kw):
    name = method.__name__
    arguments = ", ".join(map(lambda x: str(x), list(args)))
    ts = time.time()
    result = method(*args, **kw)
    te = time.time()
    time_s = '{:s} {:2.2f} sec'.format( name, te-ts )
    print( time_s )
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


if __name__ == "__main__":
  pass
