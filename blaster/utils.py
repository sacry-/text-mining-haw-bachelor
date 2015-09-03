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


DATE_INDEX_PATTERN = re.compile("^(2[0-9]{3})\W+([0-9]{1,2})\W+([0-9]{1,2})")
def date_for_index(date_str):
  m = DATE_INDEX_PATTERN.match(date_str)
  if m:
    return "".join([m.group(x) for x in range(1, 3 + 1)])
  return None


DATE_PATTERN = re.compile("([0-9]{4})([0-9]{2})([0-9]{2})")
def date_range(from_date, to_date):

  def split_by_date(some_date):
    return [int(x) for x in DATE_PATTERN.split(some_date) if x and x.strip()]

  start = split_by_date(from_date)
  end = split_by_date(to_date)

  assert (len(start) == 3 and len(end) == 3), "from_date and/or to_date is malformed. Use YYYYMMDD (e.g. 20150711) only! input: {} {}".format( start, end )

  year, month, day = start
  start_date = datetime.date(year, month, day)
  year, month, day = end
  end_date = datetime.date(year, month, day)

  r = ( end_date + datetime.timedelta(days=1) - start_date ).days
  times = [start_date + datetime.timedelta(days=i) for i in range(r)]

  without_dash = [str(date).replace("-", "") for date in times]
  return without_dash

def date_today():
  return datetime.date.today().strftime("%Y%m%d")


if __name__ == "__main__":
  pass
