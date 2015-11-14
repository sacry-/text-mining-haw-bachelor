from scraping.source import Source


class BBC(Source):

  def __init__(self, 
      name="bbc", 
      url="http://www.bbc.com/news/world", 
      memoize=True, 
      whitelist=[
        "invalid_title",
        "request_error"
      ]
    ):
    super(BBC, self).__init__(name, url, memoize, whitelist)


if __name__ == "__main__":
  bbc = BBC()