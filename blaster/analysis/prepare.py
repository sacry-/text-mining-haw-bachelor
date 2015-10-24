import re
from nltk import word_tokenize
from nltk.corpus import stopwords


NLTK_STOPS = stopwords.words('english')
STOPWORDS = """
a about above across after afterwards again against all almost alone along already also although always am among amongst amoungst amount an and another any anyhow anyone anything anyway anywhere are around as at back be
became because become becomes becoming been before beforehand behind being below beside besides between beyond bill both bottom but by call can
cannot cant co computer con could couldnt cry de describe
detail did didn do does doesn doing don done down due during
each eg eight either eleven else elsewhere empty enough etc even ever every everyone everything everywhere except few fifteen
fify fill find fire first five for former formerly forty found four from front full further get give go
had has hasnt have he hence her here hereafter hereby herein hereupon hers herself him himself his how however hundred i ie
if in inc indeed interest into is it its itself keep last latter latterly least less ltd
just
kg km
made make many may me meanwhile might mill mine more moreover most mostly move much must my myself name namely
neither never nevertheless next nine no nobody none noone nor not nothing now nowhere of off
often on once one only onto or other others otherwise our ours ourselves out over own part per
perhaps please put rather re
quite
rather really regarding
same say see seem seemed seeming seems serious several she should show side since sincere six sixty so some somehow someone something sometime sometimes somewhere still such system take ten
than that the their them themselves then thence there thereafter thereby therefore therein thereupon these they thick thin third this those though three through throughout thru thus to together too top toward towards twelve twenty two un under
until up unless upon us used using
various very very via
was we well were what whatever when whence whenever where whereafter whereas whereby wherein whereupon wherever whether which while whither who whoever whole whom whose why will with within without would yet you
your yours yourself yourselves
"""

STOPWORDS = frozenset(w for w in STOPWORDS.split() if w)
RE_NONALPHA = re.compile(r"\W", re.UNICODE)
RE_AL_NUM = re.compile(r"([a-z]+)([0-9]+)", flags=re.UNICODE)
RE_NUM_AL = re.compile(r"([0-9]+)([a-z]+)", flags=re.UNICODE)
RE_NUMERIC = re.compile(r"[0-9]+", re.UNICODE)


class Prepare():

  def __init__(self, sentence, options={ "non_alpha" : True}):
    self.non_alpha = options["non_alpha"]
    self.s = self.filter(sentence)

  def tokens(self):
    return word_tokenize(self.s.lower())

  def filter(self, s):
    s = self.remove_stopwords(s)
    s = self.strip_non_alphanum(s)
    s = self.split_alphanum(s)
    s = self.strip_numeric(s)
    return s

  def strip_non_alphanum(self, s):
    if self.non_alpha:
      return RE_NONALPHA.sub(" ", s)
    return s

  def remove_stopwords(self, s):
    return " ".join(w for w in word_tokenize(s) if self.is_not_noise(w))

  def split_alphanum(self, s):
    s = RE_AL_NUM.sub(r"\1 \2", s)
    return RE_NUM_AL.sub(r"\1 \2", s)

  def strip_numeric(self, s):
    return RE_NUMERIC.sub("", s)

  def is_not_noise(self, w):
    w = w.strip()
    return (w not in STOPWORDS or len(w) > 1 or not w.strip() in NLTK_STOPS)
