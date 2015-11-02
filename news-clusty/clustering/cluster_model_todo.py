
class PreClusterStrategy(object):

  def __init__(self):
    pass

  def call(self, points):
    return points

class SeedStrategy(object):

  def __init__(self):
    pass

  def call(self, points):
    return points

class ClusterAlgorithm(object):

  def __init__(self):
    pass

  def call(self, points):
    return points

class PostClusterStrategy(object):

  def __init__(self):
    pass

  def call(self, points):
    return points


class Clustering(object):

  def __init__( self, 
    pre_cluster_strategy: PreClusterStrategy, 
    seed_strategy: SeedStrategy,
    cluster_algorithm: ClusterAlgorithm,
    post_cluster_strategy: PostClusterStrategy ):

    self.pre_cluster_strategy = pre_cluster_strategy
    self.seed_strategy = seed_strategy
    self.cluster_algorithm = cluster_algorithm
    self.post_cluster_strategy = post_cluster_strategy

  def call(self, points):
    r = self.pre_cluster_strategy.call( points )
    r = self.seed_strategy.call( r )
    r = self.cluster_algorithm.call( r )
    return self.post_cluster_strategy.call( r )


if __name__ == "__main__":
  points = [
    ["t","abc","t", "defg", "t"], 
    ["abc", "t", "defg"], 
    ["y", "t", "x"], 
    ["t", "z", "t", "defg"]
  ]
  result = Clustering(
    pre_cluster_strategy=PreClusterStrategy(),
    seed_strategy=SeedStrategy(),
    cluster_algorithm=ClusterAlgorithm(),
    post_cluster_strategy=PostClusterStrategy()
  ).call( points )

  print( "points:", points )
  print( "result:", result )
