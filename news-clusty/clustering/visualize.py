import six
import random
import numpy as np
import matplotlib.pyplot as plt
import sklearn.decomposition as deco

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

def cluster_plot_3d(x, centroids, c, k):
  fig = plt.figure()
  fig.canvas.set_window_title("K means")
  ax = fig.add_subplot(111, projection='3d')
  fig.suptitle("k = {}".format(k), fontsize=12)
  point_colors = get_colors(k)

  for i, cidx in enumerate(c):
    ax.scatter(x[i,0], x[i,1], x[i,2], 
      c=point_colors[cidx], marker='o', zorder=-1
    )

  if not centroids == None:
    for i in range(0, k):
      ax.scatter(centroids[i,0], centroids[i,1], centroids[i,2], 
        s=180.0, c=point_colors[i], marker='o', lw=2, zorder=100
      )
  plt.show()


def cluster_plot_2d(x, centroids, c, k):  
  fig = plt.figure()
  fig.canvas.set_window_title("K means")
  fig.suptitle("k = {}".format(k), fontsize=12)
  point_colors = get_colors(k)

  for i, cidx in enumerate(c):
    plt.scatter(x[i,0], x[i,1], 
      c=point_colors[cidx], marker='o', zorder=-1
    )

  if not centroids == None:
    for i in range(0, k):
      plt.scatter(centroids[i,0], centroids[i,1], 
        s=180.0, c=point_colors[i], marker='o', lw=2, zorder=100
      )
  plt.show()


def big_clusterd_plot_2d(x, centroids, c, k):
  fig = plt.figure()
  fig.canvas.set_window_title("K means")
  fig.suptitle("k = {}".format(k), fontsize=12)
  point_colors = list(cm.rainbow(np.linspace(0, 10, 10 * (k + 1))))

  for i, cidx in enumerate(c):
    plt.scatter(x[i,0], x[i,1], 
      c=point_colors[cidx], marker='o', zorder=-1
    )
  
  if not centroids == None:
    for i in range(0, k):
      plt.scatter(centroids[i,0], centroids[i,1], 
        s=180.0, c=point_colors[i], marker='o', lw=2, zorder=100
      )
  
  plt.show()


def create_sample(num_docs, features):
  splitted = num_docs / 5
  a = 5 * np.random.random_sample((splitted, features))
  b = -5 * np.random.random_sample((splitted, features))
  c = np.random.normal(5, 4, (splitted, features))
  d = np.random.normal(-5, 4, (splitted, features))
  e = np.random.normal(0, 4, (splitted, features))
  return np.concatenate((a,b,c,d,e))

def reduce_dimensions(x, dims=3):
  x = (x - np.mean(x, 0)) / np.std(x, 0)
  pca = deco.PCA(dims)
  y = pca.fit(x).transform(x)
  print("Reduced dims from {} to {}".format( x.shape, y.shape ))
  return y

if __name__ == "__main__":
  get_colors(200)




