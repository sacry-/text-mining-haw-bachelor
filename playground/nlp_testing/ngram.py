from __future__ import division

# NGrams are N-token sequences i.e. ["your", "homework"], ["you", "have"], ["have", "to"]
# with which one can predict on what word or sequence of words will most likely follow
# a set of distinct other words.
def tokenize(sent):
  return map(lambda x: x.lower(), sent.split(" "))

def bag_of_words(sents):
  bag = set([])
  for sent in sents:
    bag.update(tokenize(sent))
  return list(bag)

class Bigrams():

  def __init__(self, sents=None):
    self.d = {}
    if sents:
      self.add_sents(sents)

  def add_sents(self, sents):
    for sent in sents:
      self.add_sent(sent)

  def add_sent(self, sent):
    sent_tokens = tokenize(sent)
    for (pos1, pos2) in zip(sent_tokens, sent_tokens[1:]):
      if self.d.has_key(pos1):
        if not self.d[pos1].has_key(pos2):
          self.d[pos1][pos2] = 0
        self.d[pos1][pos2] += 1
      else:
        self.d[pos1] = {
          pos2 : 1
        }

  def mle(self, wn1, wn):
    if not self.d.has_key(wn1):
      return 0
    counts = self.d[wn1].iteritems()
    total = reduce(lambda a,x: a + x[1], counts, 0)
    occurences = 0
    if self.d[wn1].has_key(wn):
      occurences = self.d[wn1][wn]
    return (occurences, total, occurences / total)


sents = [
  "This is a sentence",
  "This is another sentence",
  "This is yet another sentence",
  "This is yet another sentence",
  "This is yet another sentence",
  "This might not be a sentence",
  "Let's make a sentence for different probabilities",
  "A sentence is another sentence if they might be equal",
  "A sentence is not another sentence if it might be equal",
  "A sentence is maybe another sentence when it's might be equal",
  "This is another issue."
]

bigram = Bigrams(sents)
probs = {}
for sent in sents:
  tokens = tokenize(sent)
  for (p1, p2) in zip(tokens, tokens[1:]):
    if not probs.has_key((p1, p2)):
      probs[(p1, p2)] = bigram.mle(p1, p2)

for ((p1, p2), (occs, total, mle)) in sorted(probs.iteritems(),key=lambda x: -x[1][0]):
  print "%s ~> %s (%s / %s = %s)" % (p1, p2, occs, total, mle)





