from scraping.source import Source


class Guardian(Source):

  def __init__(self, 
      name="theguardian", 
      url="http://www.theguardian.com/world", 
      memoize=True, 
      whitelist=["invalid_title","request_error"]
    ):
    super(Guardian, self).__init__(name, url, memoize, whitelist)


if __name__ == "__main__":
  guardian = Guardian()