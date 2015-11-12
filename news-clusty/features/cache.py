from features.rediss import Rediss


class Cache(Rediss):

  def __init__(self, db=0, host="localhost", port=6379):
    super(Cache, self).__init__(db, host, port)

  def key_name(self, index, _id):
    return "{}/features/{}".format(index, _id)

  def key_names(self, docs):
    return [self.key_name(index, _id) for (index, _id) in docs]

  def set(self, index, _id, val):
    self.rs.set(self.key_name(index, _id), val)

  def get(self, index, _id):
    return self.leval(self.rs.get(self.key_name(index, _id)))

  def mget(self, index_id_pairs):
    return self.rs.mget(index_id_pairs)

  def get_features(self, indices):
    for index in indices:
      keys = list( self.keys("{}*".format( index )) )
      if not keys:
        continue
      for key, val in zip(keys, self.mget(keys)):
        _id = key.split("/")[-1]
        if val:
          yield (_id, self.leval(val))
        else:
          yield (_id, None)

  def __repr__(self):
    return "FeatureCache %s" % super(Cache, self).__repr__()


if __name__ == "__main__":
  fcache = Cache()
  print(fcache)
