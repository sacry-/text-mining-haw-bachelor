from preprocessing.syntax import tokenize
from preprocessing.syntax import get_fast_blob

from preprocessing.ner_tagger import get_tagger
from preprocessing.text_normalizer import TextNormalizer

from utils import date_today
from elasticsearch_dsl import DocType, String


# Factories
def preprocess(text, tokenize_func=None):  
  if not tokenize_func:
    tokenize_func = tokenize

  pre = Preprocessor(text, tokenize_func)
  pre.pos_tags()
  pre.noun_phrases()
  pre.get_entities()
  
  return pre

def preprocess_and_persist(a, tokenize_func=None):
  print("Preprocessing {}".format(str(a)))

  pre = preprocess(a.text, tokenize_func)

  nouns = pre.noun_phrases()
  ners = pre.get_entities()

  prep = Prep(
    meta={'id' : a.meta.id}, 
    tokens=pre.tokens,
    pos_tags=pre.pos_tags(),
    noun_phrases=nouns if nouns else [],
    ner_tags=ners if ners else []
  )

  prep._index = a._index
  return prep


# Glue Interface
class Preprocessor():

  def __init__(self, text, tokenize_func):
    self.text = str(text)
    self.text_norm = self.normalize(self.text)
    self.tokenize_func = tokenize_func
    self.tokens = self.tokenize_func( self.text_norm )
    self.blob = get_fast_blob(self.text_norm)
    self.ner_tagger = get_tagger(
      self.tokenize_func( self.text )
    )

  def normalize(self, text):
    tn = TextNormalizer(options=["keep_alpha"])
    return tn.normalize(str(text))

  def pos_tags(self):
    return self.blob.tags

  def noun_phrases(self):
    return self.blob.noun_phrases

  def get_entities(self):
    return self.ner_tagger.get_entities()


# Persistence
class Prep(DocType):
  tokens = String(fields={'raw': String(index='not_analyzed')})
  pos_tags = String(fields={'raw': String(index='not_analyzed')})
  noun_phrases = String(fields={'raw': String(index='not_analyzed')})
  ner_tags = String(fields={'raw': String(index='not_analyzed')})

  class Meta:
    index = date_today()

  def save(self, ** kwargs):
    return super(Prep, self).save(** kwargs)

  def __repr__(self):
    return "{}/prep/{}".format(self._index, self.meta.id)




if __name__ == "__main__":
  s = "It was a very long and cool day. 'I am satisfied!' Mr. crowley said. Have you heard that Google held a lot of coding competitions in the past?"

  prep = preprocess( s )

  print("--------- tokens: -----")
  print(prep.tokens)
  print("--------- pos tags: -----")
  print(prep.pos_tags())
  print("--------- blob ner: -----")
  print(prep.noun_phrases())
  print("--------- stanford ner: -----")
  for e in prep.get_entities():
    print(e)
  print("  finished")



