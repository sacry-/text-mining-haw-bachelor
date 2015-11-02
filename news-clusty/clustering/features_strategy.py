class FeatureStrategy(object):

  def __init__(self):
    pass

  def call(self):
    pass

class TFIDFStrategy(FeatureStrategy):

  def __init__(self):
    pass

class Distances(FeatureStrategy):

  def __init__(self):
    pass


if __name__ == "__main__":
  strategy = TFIDFStrategy()
  strategy.call()

  strategy = Distances()
  strategy.call()