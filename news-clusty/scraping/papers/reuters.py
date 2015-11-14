from scraping.source import Source


class Reuters(Source):

  def __init__(self, 
      name="reuters", 
      url="http://www.reuters.com/news/world", 
      memoize=True, 
      whitelist=[
        "invalid_title",
        "request_error"
      ]
    ):
    super(Reuters, self).__init__(name, url, memoize, whitelist)


if __name__ == "__main__":
  reuters = Reuters()