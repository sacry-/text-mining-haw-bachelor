
from nltk.corpus import wordnet as wn
from nltk import PorterStemmer
from io_utils import read_from_file
from preprocessing import TextNormalizer
from itertools import zip_longest
from collections import defaultdict

# Loading the Wordnet domains.
def load_wn_domains():
  p = "/Users/sacry/dev/uni/bachelor/data/wordnet-domains-sentiwords/wn-domains/wn-domains-3.2-20070223"
  domain2synsets = defaultdict(list)
  synset2domains = defaultdict(list)
  for i in open(p, 'r'):
    ssid, doms = i.strip().split('\t')
    doms = doms.split()
    synset2domains[ssid] = doms
    for d in doms:
      domain2synsets[d].append(ssid)
  return domain2synsets, synset2domains

def synset2id(ss):
  return str(ss.offset()).zfill(8) + "-" + ss.pos()

normalizer = TextNormalizer()
PORTER = PorterStemmer()
def stem(w):
  return PORTER.stem(w).lower()

def hyper_closure(syn):
  return list(syn.closure(lambda x: x.hypernyms()))

def hypo_closure(syn):
  return list(syn.closure(lambda x: x.hyponyms()))


def n_gram_concepts(closure1, closure2):
  r = []
  for clos1 in closure1:
    for clos2 in closure2:
      sim = clos1.path_similarity(clos2)
      if sim:
        r.append( (sim, clos1, clos2) )
  concepts = set([])
  for _, c1, c2 in sorted(r, key=lambda x: -x[0])[:5]:
    concepts.add(c1)
    concepts.add(c2)
  return concepts


def grouper(n, iterable, fillvalue=None):
  "grouper(3, 'ABCDEFG', 'x') --> ABC DEF Gxx"
  args = [iter(iterable)] * n
  return zip_longest(fillvalue=fillvalue, *args)


def topics_single_sentence(words, domain2synsets, synset2domains):
  result = defaultdict(int)
  cache = {}
  for w in words:
    concepts = wn.synsets(w)

    for concept in concepts:

      if not concept in cache:
        cache[concept] = synset2id(concept)
      ssid = cache[concept]

      if ssid in synset2domains:
        for domain in synset2domains[ssid]:
          result[domain] += 1
  
  return result

def get_category(r):
  if not r:
    return "factotum"

  def minimize(r):
    return min(r.items(), key=lambda x: -x[1])[0]

  if len(r) == 1:
    return list(r.keys())[0]

  if "factotum" in r:
    del r["factotum"]

  return minimize(r)


features = read_from_file("generative_1")
domain2synsets, synset2domains = load_wn_domains()


for idx, fst in enumerate(features[3:]):

  sentences = [w.strip("\n") for w in fst.split("__PLACE_HOLDER__")]
  intuition = sentences[:2]

  r = defaultdict(int)
  for sentence in sentences:
    words = sentence.split(" ")
    topics = topics_single_sentence(words, domain2synsets, synset2domains)
    for k, v in topics.items():
      r[k] += v

  print("-"*40, "\n{}. {}\n  {}".format(idx, get_category(r), intuition))
  print(r)




