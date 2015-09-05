from .features_strategy import TFIDFStrategy
from .features_strategy import Distances


class Features():

  def __init__(self, feature_strategy, documents):
    self.feature_strategy = feature_strategy
    self.documents = documents

  def call(self):
    self.feature_strategy.call(self.documents)


class Feature():

  def __init__(self, document):
    self.document = document


if __name__ == "__main__":
  strategy = TFIDFStrategy()
  features = Features(strategy, [])
  features.call()

  strategy = Distances()
  features = Features(strategy, [])
  features.call()