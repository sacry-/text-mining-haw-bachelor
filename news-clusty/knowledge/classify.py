from __future__ import division

import numpy as np
import pickle
import json

from collections import defaultdict
from persistence import EsSearcher

from sklearn.externals import joblib
from sklearn.preprocessing import StandardScaler
from sklearn.naive_bayes import MultinomialNB

from preprocessing import TextNormalizer
from transformation import hash_vector
from features import flattened_features
from wiki_categories import get_lines
from wiki_categories import wiki_base_path
from utils.helpers import unique


def get_test_set(from_date = "20151114", to_date = "20151114"):
  return flattened_features( 
    from_date, to_date
  )

  es = EsSearcher()
  tn = TextNormalizer()
  features, titles = [], []
  for a in es.articles_from_to(from_date, to_date):
    features.append( tn.normalize(a.text) )
    titles.append( a.title )
  return features, titles


def cat_to_id_mapping(category_to_titles):
  cat_to_id = {}
  cats = unique([cat for (cat,_) in category_to_titles])
  for cat_id, cat in enumerate(cats):
    cat_to_id[cat] = cat_id
  return cat_to_id


def preprocess(category_to_titles):
  print("Preprocess..")
  cat_to_id = cat_to_id_mapping( category_to_titles )

  y_train = []
  for category, line in category_to_titles:
    y_train.append( cat_to_id[category] )

  print("Hashing..")
  x = [lines for (_, lines) in category_to_titles]

  x_train, vsmodel = hash_vector(x, ngram=(1,2))

  return cat_to_id, x_train.toarray(), y_train, vsmodel


def best3_probas(model, new_text, id_to_cat):
  r = []
  for cat_id, prob in enumerate(model.predict_proba(new_text)[0]):
    r.append((cat_id, prob))

  sproba = sorted(r, key=lambda x: -x[1])
  return [(id_to_cat[cat_id], prob) for cat_id, prob in sproba[0:3]]



def path_to_bayes():
  return "{}/mbayes_topics.pkl".format(wiki_base_path())

def path_to_vsmodel():
  return "{}/vsmodel_topics.pkl".format(wiki_base_path())

def path_to_cat_id():
  return "{}/cat_id_topics.json".format(wiki_base_path())


def load_bayes():
  print("Loading bayes, vsmodel and id_to_cat mapping..")
  
  bayes = joblib.load(path_to_bayes())
  print("{} - check!".format(bayes))
  
  vsmodel = joblib.load(path_to_vsmodel())
  print("{} - check!".format(vsmodel))

  with open(path_to_cat_id(), 'r+') as data_file:
    cat_to_id = json.load(data_file)

  print("category mapping - check!")

  return bayes, vsmodel, cat_to_id


def save_bayes(bayes, vsmodel, cat_to_id):
    print("Dumping bayes..")
    joblib.dump(bayes, path_to_bayes()) 

    print("Dumping vsmodel..")
    joblib.dump(vsmodel, path_to_vsmodel()) 

    with open(path_to_cat_id(), 'w+') as fp:
      json.dump(cat_to_id, fp)


def train_bayes(preload, persist):
  if preload:
    return load_bayes()

  line_per_category=1000

  print("Train Multinomial Bayes...\n\twith {} features".format(line_per_category))
  bayes = MultinomialNB(alpha=0.0001)
  print(bayes)

  category_to_titles = list( get_lines(line_per_category=line_per_category) )
  cat_to_id, x_train, y_train, vsmodel = preprocess( category_to_titles )

  print("Fitting..")
  bayes.fit(x_train, y_train)

  if persist:
    save_bayes(bayes, vsmodel, cat_to_id)

  return bayes, vsmodel, cat_to_id


def show_bayes(model, vsmodel, cat_to_id, ffeatures, fids):
  id_to_cat = {v: k for k, v in cat_to_id.items()}
  print(id_to_cat)
  categories = defaultdict(list)
  for idx, text in enumerate(ffeatures):
    new_text = vsmodel.fit_transform([text]).toarray()
    predicted_cat, cat_id = [(id_to_cat[_id], _id) for _id in model.predict(new_text)][0]
    categories[predicted_cat].append(fids[idx])
  for category, _ids in categories.items():
    print((category + " ")*3)
    for _id in _ids:
      print(" ", _id)
    print("-"*40)

  
if __name__ == "__main__":
  model, vsmodel, cat_to_id = train_bayes(
    preload=True, 
    persist=False
  )
  ffeatures, fids = get_test_set(from_date = "20151114", to_date = "20151114")
  show_bayes( model, vsmodel, cat_to_id, ffeatures, fids )


