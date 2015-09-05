from .cluster_strategy import WikipediaStrategy
from .cluster_strategy import WordnetStrategy


class Cluster():

  def __init__(self, cluster_strategy, features):
    self.cluster_strategy = cluster_strategy
    self.features = features

  def call(self):
    self.cluster_strategy.call(self.features)


if __name__ == "__main__":
  strategy = WikipediaStrategy()
  cluster = Cluster(strategy, [])
  cluster.call()

  strategy = WordnetStrategy()
  cluster = Cluster(strategy, [])
  cluster.call()