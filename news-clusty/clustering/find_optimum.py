


# TODO
def find_optimal_cluster_algo( ffeatures, fids ):
  x = tfidf( ffeatures )
  (m, n) = x.shape
  
  reduction_f = lsa
  clusterer = k_means_cluster

  m_score, clusters, dim = 0, 0, 0
  for o_off in [7.5,7,6.5]:
    o_off = int(m * (1 / o_off))
    x_red = reduction_f(x, o_off)

    for i_off in [6,5.5]:
      n_clusters = int(m * (1 / i_off)) + 1
      centroids, c, k = clusterer(x_red, n_clusters)
      print("  kmeans with:", n_clusters, "i_off:", i_off)

      new_score = silhouette(x_red, c)

      if new_score >= m_score:
        print("    new score:", new_score, "clusters:", n_clusters, "dim for lsa:", o_off)
        m_score = new_score
        clusters = n_clusters
        dim = o_off

  print("final score:", m_score, "with k=",clusters, "dim lsa=",dim)
  x_red = reduction_f(x, 3)
  centroids, c, k = clusterer(x_red, clusters)
  cluster_plot_3d(x_red, centroids, c, k)
  print_clusters(c, fids)