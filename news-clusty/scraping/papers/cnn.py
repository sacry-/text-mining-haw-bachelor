from scraping.source import Source


class CNN(Source):

  def __init__(self, 
      name="cnn", 
      url="http://edition.cnn.com/world", 
      memoize=True, 
      whitelist=[
        "invalid_title",
        "request_error"
      ]
    ):
    super(CNN, self).__init__(name, url, memoize, whitelist)


if __name__ == "__main__":
  cnn = CNN()