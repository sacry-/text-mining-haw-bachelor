import redis
import ast


LEVAL = ast.literal_eval
def leval(o):
  return LEVAL(str(o))

class Rediss(object):

  def __init__(self, host="localhost", port=6379, config=None):
    self.host = host
    self.port = port
    if config:
      self.config = None

  def __repr__(self):
    return "{ host='%s' port='%s' " % (self.host, self.port)

  def keys(self, pattern="*"):
    for key in self.rs.keys(pattern): 
      yield str(key)

  def values(self, key_names, ordered=False):
    keys = self.key_names(key_names)
    return self.values_by_keys(keys, ordered)

  def values_by_keys(self, keys, ordered=False):
    for val in self.rs.mget(keys):
      if val:
        yield leval(val)
      else:
        if ordered:
          yield {}

  def keys_values(self, key_names):
    keys = self.key_names(key_names)
    values = self.values_by_keys(keys, True)
    for (idx, val) in enumerate(values):
      if keys[idx] and val:
        yield (keys[idx], leval(val))

  def values_by_pattern(self, pattern):
    for val in self.rs.mget(list(self.keys(pattern))):
      if val:
        yield leval(val)

  def pipeline(self, _transaction=False):
    return self.rs.pipeline(transaction=_transaction)

  def size(self):
    return self.rs.dbsize()

  def delete(self, keys):
    self.rs.delete(keys)
    return not self.exists(keys[0])

  def exists(self, key_name):
    return self.rs.exists(key_name)

  def ping(self):
    try:
      print("ping: %s from: %s" % (self.rs.ping(), self))
      return True
    except:
      print("ping to %s failed!" % (str(self)))
      return False


class ClusterCache(Rediss):

  def __init__(self, host="localhost", port=6379):
    super(ClusterCache, self).__init__(host, port)
    self.db = 0
    self.rs = redis.StrictRedis(host=self.host, port=self.port, db=self.db)

  def key_name(self, index, _id):
    return "{}/cluster/{}".format(index, _id)

  def key_names(self, docs):
    return [self.key_name(index, _id) for (index, _id) in docs]

  def get(self, index, _id):
    key = self.key_name(index, _id)
    val = self.rs.get(key)
    return leval(str(val))

  def put(self, index, _id, content):
    self.rs.set(self.key_name(index, _id), content)

  def __repr__(self):
    return "ClusterCache%s db=%s }" % (super(ClusterCache, self).__repr__(), self.db)


if __name__ == "__main__":
  rcache = ClusterCache()
  if rcache.ping():
    rcache.put("a", "b", "c")
    rcache.put("d", "e", "f")
    print(rcache.get("a", "b"))
    l = [("a", "b"), ("d", "e")]
    for e in rcache.keys_values(l):
      print(e)



