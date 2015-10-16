from scraping.papers.guardian import Guardian
from scraping.papers.nytimes import NyTimes


class Sources():

  def __init__(self, *items):
    self.sources = items

  def __iter__(self):
    self.counter = 0
    return self

  def __next__(self):
    self.counter += 1 
    if self.counter <= len(self.sources):
      return self.sources[self.counter - 1]
    else:
      raise StopIteration

  def __getitem__(self, idx):
    return self.sources[idx]

  def __contains__(self, obj):
    return obj in self.sources

  def __len__(self):
    return len(self.sources)

def get_sources():
  return Sources( 
    Guardian(), NyTimes() 
  )
