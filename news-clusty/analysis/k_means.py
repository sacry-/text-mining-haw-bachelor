from __future__ import division

import numpy as np
import math
import random
import time
import sys

import sklearn.decomposition as deco

from visualize import cluster_plot_2d


# Helper
def create_sample(num_docs, features):
  splitted = num_docs / 5
  a = 5 * np.random.random_sample((splitted, features))
  b = -5 * np.random.random_sample((splitted, features))
  c = np.random.normal(5, 4, (splitted, features))
  d = np.random.normal(-5, 4, (splitted, features))
  e = np.random.normal(0, 4, (splitted, features))
  return np.concatenate((a,b,c,d,e))


# Algorithm
def distance(x, centroids):
  return np.linalg.norm(x - centroids, axis=1)**2

def cost_func(x, centroids, c):
  dist = distance(x, centroids[c.flatten()])
  return (1 / x.shape[0]) * np.sum( dist )

def initial_centroids(x, k):
  space = list(range(0, x.shape[0]))
  s = random.sample(space, k)
  return x[np.array(s)]

def assign_centroids(c, x, centroids):
  m = x.shape[0]
  for i in range(0, m):
    dist = (1 / m) * distance(x[i,:], centroids)
    c[i] = np.argmin(dist)
  return c

def move_centroids(centroids, x, c, k):
  for j in range(0, k):
    (cids, _) = np.where(c == j)
    base = 1 / max(len(cids), 1)
    centroids[j] = base * np.sum(x[cids], axis=0)
  return centroids.reshape(centroids.shape[0], -1)

def converged(j_history, i):
  if i > 3:
    diff = j_history[i-1] - j_history[i]
    return diff < 0.0000001 and not diff < 0
  return False

def kmeans(x, k, num_iter=40):
  j_history = []
  (m, _) = x.shape
  c = np.zeros((m, 1), dtype=np.int)
  centroids = initial_centroids(x, k)

  for i in range(0, num_iter):
    j_history.append( cost_func(x, centroids, c) )

    c = assign_centroids(c, x, centroids)
    centroids = move_centroids(centroids, x, c, k)

    if converged(j_history, i):
      print( "converged at iter: {}".format(i) )
      break

  print( "cost:", j_history[-1], "k:", k )

  return centroids, c, j_history

# Optimize cost function
def find_optimum(x, k=2, k_iter=10, num_iter=5):
  m = x.shape[0]
  centroids, c, j_history = None, None, None
  cost = float("inf")
  k_best, in_iter = k, 1

  iter_round = 0
  for i in range(0, num_iter):
    for k_off in range(0, k_iter):
      k_next = k + k_off
      centroids_, c_, j_history_ = kmeans(x, k_next)
      new_J = cost_func(x, centroids_, c_)

      if new_J < cost:
        print( "{}. new cost: {}, k: {}".format(
          iter_round + k_off, new_J, k_next) 
        )
        in_iter = (i * k_iter) + (k_off + 1)
        cost, k_best = new_J, k_next
        centroids, c, j_history = centroids_, c_, j_history_

    iter_round = ((i + 1) * k_iter)

  return in_iter, cost, centroids, c

# Reduce dimensions
def reduce_dimensions(x, dims=3):
  try:
    x = (x - np.mean(x, 0)) / np.std(x, 0)
  except:
    pass
  pca = deco.PCA(dims)
  y = pca.fit(x).transform(x)
  print("Reduced dims from {} to {}".format( x.shape, y.shape ))
  return y


if __name__ == "__main__":
  modes = [
    "optimized",
    "single",
    "sklearn"
  ]
  mode = modes[2]

  if mode == "optimized":
    x = create_sample(800, 10)
    x = reduce_dimensions(x, 2)
    in_iter, cost, centroids, c = find_optimum(x, k=1, k_iter=20, num_iter=3)
    k_best = centroids.shape[0]
    print( "iteration: {}, cost: {}, k: {}".format( in_iter, cost, k_best ) )
    cluster_plot_2d(x, centroids, c, k_best)

  elif mode == "single":
    k = 10
    x = create_sample(500, 10)
    x = reduce_dimensions(x, 2)
    centroids, c, j_history = kmeans(x, k)
    cluster_plot_2d(x, centroids, c, k)

  elif mode == "sklearn":
    from sklearn.cluster import KMeans

    x = create_sample(5000, 100)
    x = reduce_dimensions(x, 2)
    km = KMeans(init='k-means++',n_clusters=15, max_iter=30, n_init=20, copy_x=True)
    km.fit(x)
    centroids = km.cluster_centers_
    c = km.labels_
    k = km.n_clusters
    cluster_plot_2d(x, centroids, c, k)


