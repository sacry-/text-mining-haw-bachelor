
class ClusterStrategy(object):

  def __init__(self):
    pass

  def call(self):
    pass

class WordNetStrategy(ClusterStrategy):

  def __init__(self):
    pass

class WikipediaStrategy(ClusterStrategy):

  def __init__(self):
    pass

class CompositeStrategy(ClusterStrategy):

  def __init__(self, strategies*):
    self.strategies = strategies

  def call(self):
    res = ""
    for strategy in self.strategies:
      res = strategy.call(res)


if __name__ == "__main__":
  wordnet_strategy = WordNetStrategy()
  wordnet_strategy.call()

  wikipedia_strategy = WikipediaStrategy()
  wikipedia_strategy.call()

  composite_strategy = CompositeStrategy(wordnet_strategy, wikipedia_strategy)
  composite_strategy.call()




  

