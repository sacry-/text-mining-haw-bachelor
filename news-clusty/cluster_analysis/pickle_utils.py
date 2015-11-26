import os

from sklearn.externals import joblib



def base_path():
  return "/".join(os.path.abspath(__file__).split("/")[:-1])

def model_path(model_name):
  return "{}/es_pickles/{}.p".format(base_path(), model_name)

def get_sents_training(model_name):
  print("loading!")
  x_n = joblib.load(model_path(model_name))
  print("Loaded model: {} with docs: {}".format(x_n[0], len(x_n)))

  index = x_n[0]

  features, titles = [], []
  for feature in x_n[1:]:
    _id, sents = feature[0], feature[2:]
    features.append( sents )
    titles.append( _id )

  return features, titles


def get_semantic_training(model_name):
  model_name = "{}_semantic".format(model_name)

  print("loading!")
  x_n = joblib.load(model_path(model_name))
  print("Loaded model: {} with docs: {}".format(x_n[0], len(x_n)))

  index = x_n[0]

  features, titles = [], []
  for feature in x_n[1:]:
    _id, title = feature[0], feature[1]

    next_idx = 2
    len_key = next_idx + feature[next_idx]
    keywords = feature[next_idx+1:len_key+1]

    next_idx = next_idx + len(keywords) + 1
    len_pos = next_idx + feature[next_idx] + 1
    pos = feature[next_idx:len_pos]

    next_idx = next_idx + len(pos)
    len_ner = next_idx + feature[next_idx]
    ner = feature[next_idx:len_ner]

    next_idx = next_idx + len(ner) + 1
    nps = feature[next_idx:-1]
    
    features.append({
      "title" : title,
      "keywords" : keywords,
      "pos" : pos,
      "ner" : ner,
      "np" : nps
    })
    titles.append( _id )
    break

  return features, titles


if __name__ == "__main__":
  f, t = get_semantic_training("20151113")



