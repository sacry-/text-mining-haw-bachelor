import ast
import redis
import os


LEVAL = ast.literal_eval

class Rediss(object):

  def __init__(self, db=0, host="localhost", port=6379, config=None):
    self.db = db
    self.host = host
    if os.environ["REDIS_HOST"]:
      self.host = os.environ["REDIS_HOST"]

    self.port = port
    if os.environ["REDIS_PORT"]:
      self.port = int(os.environ["REDIS_PORT"])

    if config:
      self.config = None
    self.rs = redis.StrictRedis(host=self.host, port=self.port, db=self.db)

  def __repr__(self):
    return "{ host='%s' port='%s' db='%s' }" % (self.host, self.port, self.db)

  def leval(self, o):
    return LEVAL(o.decode("utf-8"))

  def keys(self, pattern="*"):
    for key in self.rs.keys(pattern): 
      yield key.decode("utf-8")

  def pipeline(self, _transaction=False):
    return self.rs.pipeline(transaction=_transaction)

  def size(self):
    return self.rs.dbsize()

  def delete(self, keys):
    self.rs.delete(keys)
    return not self.exists(keys[0])

  def exists(self, index, _id):
    return self.rs.exists(self.key_name(index, _id))

  def ping(self):
    try:
      print("ping: %s from: %s" % (self.rs.ping(), self))
      return True
    except:
      print("ping to %s failed!" % (str(self)))
      return False

if __name__ == "__main__":
  pass


  