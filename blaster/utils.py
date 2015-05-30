# encoding: utf-8
import ast
import json                                              
import re
import hashlib
import os
import time
import dateutil.parser as dp

from datetime import datetime
from logger import Logger

logger = Logger(__name__).getLogger()

def timeit(method):
  def timed(*args, **kw):
    name = method.__name__
    arguments = ", ".join(map(lambda x: str(x), list(args)))
    ts = time.time()
    result = method(*args, **kw)
    te = time.time()
    time_s = '{:s} {:2.2f} sec'.format( name, te-ts )
    print( time_s )
    logger.info( time_s )
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

def iso_to_sec(t):
  return dp.parse(t).strftime('%s')

def ts_now():
  return datetime.fromtimestamp(time.time()).isoformat()

def evaluate(python_data):
  return ast.literal_eval(python_data)

def read_json(abs_path):
  with open(abs_path) as f:
    return evaluate(f.read())

def freadlines(abs_path):
  with open(abs_path) as f:
    return f.readlines()









