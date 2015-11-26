import os
import numpy as np

from collections import Counter
from utils.helpers import flatten, unique

from clustering import cluster_plot_2d
from clustering import cluster_plot_3d


def print_measure(cluster_algo_name, measure_name, measure):
  print( "-"*40, "\n", cluster_algo_name, "-", measure_name, "-", measure, "\n","-"*40 )

def plot(x_red, centroids, c, k, cluster_algo_name, dim):
  if dim == 2:
    cluster_plot_2d(x_red, centroids, c, k, cluster_algo_name)
  else:
    cluster_plot_3d(x_red, centroids, c, k, cluster_algo_name)

def print_top_words(model, feature_names, n_top_words):
  for topic_idx, topic in enumerate(model.components_):
    print("Topic #%d:" % topic_idx)
    print(" ".join([feature_names[i] for i in topic.argsort()[:-n_top_words - 1:-1]]))
  print()


def print_clusters(c, fids):
  k = len(list(Counter(c).keys()))
  cluster_size = {cidx: np.where(c == cidx)[0].shape[0] for cidx in range(0,k)}

  clusters = {}
  for doc, cid in enumerate(c):
    if cid == -1:
      continue

    if not cid in clusters:
      clusters[cid] = []  
    clusters[cid].append( doc )

  for cid, docs in list(clusters.items()):
    if len(docs) < 1:
      continue
    collection = []
    for doc in docs:
      collection.append( fids[doc] )
      
    print("Cluster {}".format(cid))
    for doc in collection:
      print(doc)
    print("-"*40)
  
  features = {}
  for cid, docs in list(clusters.items()):
    features[cid] = unique(flatten([fids[doc].split("_") for doc in docs]))

  for cid, docs in list(clusters.items()):
    print( "{}. {} | {}".format(cid, len(docs), len(features[cid])))



def base_path():
  return "/".join(os.path.abspath(__file__).split("/")[:-1])

def model_path(model_name):
  return "{}/{}.txt".format(base_path(), model_name)
  
def append_to_file(model_name, features):
  with open(model_path(model_name), "a+") as f:
    for feature in features:
      f.write( "{}\n".format(feature) )

def read_from_file(model_name):
  result = []
  with open(model_path(model_name), "r+") as features:
    for feature in features:
      result.append(feature)
  return result







