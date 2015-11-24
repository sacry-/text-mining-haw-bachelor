import six
import random
import numpy as np
import matplotlib.pyplot as plt
import sklearn.decomposition as deco

from collections import defaultdict
from matplotlib.colors import LinearSegmentedColormap
import colorsys

from mpl_toolkits.mplot3d import Axes3D
from matplotlib import colors
import matplotlib.cm as cm


def get_colors(k):
  ugly_colors = set(["white", "black", "cyan", "magenta", "pink"])
  colors_ = set(sum([[x for x in xs] 
                for xs in list(six.iteritems(colors.cnames))], [])) - ugly_colors
  sample = random.sample(colors_, min(len(colors_), k))
  return list(set(sample))

def cluster_plot_3d(x, centroids, c, k, name):
  fig = plt.figure()
  fig.canvas.set_window_title(name)
  ax = fig.add_subplot(111, projection='3d')
  fig.suptitle("n clusters = {}".format(k), fontsize=12)
  point_colors = get_colors(k)

  cluster_size = {cidx: np.where(c == cidx)[0].shape[0] for cidx in range(0,k)}
  for i, cidx in enumerate(c):
    if cluster_size[cidx] <= 3:  
      ax.scatter(x[i,0], x[i,1], x[i,2],
        c="black", marker='x', zorder=-1
      )

    else:
      ax.scatter(x[i,0], x[i,1], x[i,2], 
        c=point_colors[cidx], marker='o', zorder=-1
      )

  if not centroids == None:
    for i in range(0, k):
      if cluster_size[i] <= 3:  
        continue
      c1, c2, c3 = centroids[i,0], centroids[i,1], centroids[i,2]
      ax.scatter(c1, c2, c3, 
        s=180.0, c=point_colors[i], marker='o', lw=2, zorder=100
      )
  plt.show()


def cluster_plot_2d(x, centroids, c, k, name):  
  fig = plt.figure()
  fig.canvas.set_window_title(name)
  fig.suptitle("n clusters = {}".format(k), fontsize=12)
  point_colors = get_colors(k)

  cluster_size = {cidx: np.where(c == cidx)[0].shape[0] for cidx in range(0,k)}
  for i, cidx in enumerate(c):
    if cluster_size[cidx] <= 3:  
      plt.scatter(x[i,0], x[i,1], 
        c="black", marker='x', zorder=-1
      )

    else:
      plt.scatter(x[i,0], x[i,1], 
        c=point_colors[cidx], marker='o', zorder=-1
      )

  if not centroids == None:
    for i in range(0, k):
      if cluster_size[i] <= 3:  
        continue
      c1, c2 = centroids[i,0], centroids[i,1]
      plt.scatter(c1, c2, 
        s=180.0, c=point_colors[i], marker='o', lw=2, zorder=100
      )
      annotate(plt, i, (c1, c2))

  plt.show()

def annotate(plt, label, xy):
  plt.annotate(
    str(label), xy=xy, 
    zorder=101, xytext = (-10, 10),
    textcoords = 'offset points', 
    ha = 'right', va = 'bottom',
    bbox = dict(boxstyle = 'round,pad=0.5', fc = 'yellow', alpha = 0.5)
  )

def annotate3d(plt, label, xyz):
  plt.annotate(
    str(label), xy=xyz, 
    zorder=101, xytext = (-10, 10),
    textcoords = 'offset points', 
    ha = 'right', va = 'bottom',
    bbox = dict(boxstyle = 'round,pad=0.5', fc = 'yellow', alpha = 0.5)
  )

def create_sample(num_docs, features):
  splitted = num_docs / 5
  a = 5 * np.random.random_sample((splitted, features))
  b = -5 * np.random.random_sample((splitted, features))
  c = np.random.normal(5, 4, (splitted, features))
  d = np.random.normal(-5, 4, (splitted, features))
  e = np.random.normal(0, 4, (splitted, features))
  return np.concatenate((a,b,c,d,e))


def titles_contain_word(word, col, threshold):
  return (word and sum([1 for x in col if word in x]) > threshold)

if __name__ == "__main__":
  get_colors(200)




