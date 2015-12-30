import signal
import csv

from os import listdir

from data_view import BBCDocuments
from preprocessing import TextNormalizer
from preprocessing import sentence_tokenize
from preprocessing import preprocess
from preprocessing import get_tagger

from utils import normalize_title
from utils import flatten

from paths import model_path
from paths import bbc_path

from knowledge import wordnet_lemmatize


# Dump
def semantics(doc):
  prep = preprocess(doc)
  return (
    flatten( prep.pos_tags() ),
    prep.noun_phrases(),
    flatten( prep.get_entities() )
  )

def bbc_parser(doc, category): 
  try:
    signal.alarm(15)
    s = doc.split("\n")
    title = s[0]
    _id = normalize_title(title)

    tn = TextNormalizer()
    pos, nouns, ners = semantics(doc)
    nouns = tn.fmap(nouns)
    ners = tn.fmap(ners)
    
    paragraphs = []
    sentences = []
    for line in s[1:]:
      if not line:
        continue
      sentences += tn.fmap(sentence_tokenize(line))
      paragraphs.append( tn.normalize(line) )

    signal.alarm(0)
    return {
      "id" : _id,
      "title" : title,
      "sents" : sentences,
      "paras" : paragraphs,
      "pos" : pos,
      "nouns" : nouns,
      "ners" : ners
    }
  except Exception as e:
    print("Could not process article")
  signal.alarm(0)
  return None

def timeout_handler(signum, frame):
  print("Timeout: could not preprocess article")
  raise Exception("Timeout: article is not processable!")

def files_for_category(category):
  bbc = bbc_path()
  final_path = "{}/{}".format(bbc, category)
  files = ["{}/{}".format(final_path, f) for f 
           in listdir(final_path)]
  
  print("Category: '{}' with n = {} files".format(category, len(files)))

  return files

def stream_to_set(model_scheme, entry):
  with open(model_path(model_scheme), "a+") as fp:
    csv.writer(fp, delimiter=';').writerow(entry)

def stream_bbc_data_by_category(category):
  signal.signal(signal.SIGALRM, timeout_handler) 

  files = files_for_category(category)
  
  for file_path in files:

    fname = file_path.split("/")[-1]
    new_doc = None

    with open(file_path, 'r+') as data_file:

      try:
        new_doc = bbc_parser(data_file.read(), category)
      except (KeyboardInterrupt, SystemExit):
        raise SystemExit("\nKeyboard was interrupted - Exiting System")
      
      except Exception as e:
        print(e, fname)
        new_doc = None

    if new_doc:
      yield new_doc


# Stream classes
def stream_bbc_data(categories):
  for category in categories:
    for doc in stream_bbc_data_by_category(category):
      stream_to_set("categories", [category])
      stream_to_set("titles", [doc["title"]])
      stream_to_set("sents", doc["sents"])
      stream_to_set("pos", doc["pos"])
      stream_to_set("nouns", doc["nouns"])
      stream_to_set("ners", doc["ners"])

def stream_bbc_ners(categories):
  for category in categories:
    for idx, doc in enumerate(stream_bbc_data_by_category(category)):
      print(" ", idx, "-", doc["title"])
      stream_to_set("ners", doc["ners"])


def stream_wordnet_projection():
  bbc = BBCDocuments()
  for idx, doc in wordnet_lemmatize( bbc.pos() ):
    stream_to_set("wordnet_lemmas", doc)
    print(idx, bbc.titles()[idx])


if __name__ == "__main__":
  # categories = ["business", "entertainment", "politics", "sport", "tech"]
  # stream_bbc_ners(categories)

  stream_wordnet_projection()


