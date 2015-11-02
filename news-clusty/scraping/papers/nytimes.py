from scraping.source import Source


class NyTimes(Source):

  def __init__(self, 
      name="nytimes", 
      url="http://international.nytimes.com/", 
      memoize=True, 
      whitelist=[
        "the_new_york_times_page_not_found",
        "invalid_title",
        "mediafed_content_channels",
        "request_error"
      ]
    ):
    super(NyTimes, self).__init__(name, url, memoize, whitelist)


if __name__ == "__main__":
  nytimes = NyTimes()


