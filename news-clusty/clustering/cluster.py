

'''
  Cluster your data by choosing the functionality yourself with a 
  minimum scheme of control from the clusmin function.

  Params: Functions piping intermediate results

    doc = slice[slice[str]]
    doc_meta = slice[dict]
    cluster_in = any object that matches cluster_in

    data_func :: () -> doc_meta
    select_features_func :: doc_meta -> doc
    prepare_func :: doc -> doc
    build_corpus_func :: (doc, doc_meta) -> (corpus, dict)
    scale_func :: (doc, corpus, dict) -> doc
    vectorize_func :: (doc, corpus, dict) -> doc
    topic_model_func :: (doc, corpus, dict) -> doc
    algorithm_func :: cluster_in -> cluster_out
    search_space_func :: cluster_out -> search_space_out
    cost_func :: cost_func_in -> cost_func_out

  Optional Params:

    n_features - number of features to be used during clustering
    n_dimensions - can be used to rescale the features

  Return: ( X, X-labels, Centroids, cost )

  constrains:
    - every function must have a suitable output for the next invoking
    function
    - named arguments are options to provide, like how many features in 
    total to extract or dimensions to reduce to if any
    - pass in None or lambda a: a, as an identity function if nothing
    should happen
'''

def clusmin(
    data_func, 
    prepare_func,
    select_features_func,
    build_corpus_func,
    scale_func,
    vectorize_func,
    topic_model_func,
    algorithm_func,
    search_space_func,
    cost_func,

    n_features = 1,
    n_dimensions = 10
  ):

  def fit():
    import time
    time.sleep(2)
    print(prepare_func)
    print(n_features)
    return "fitted!"

  return fit



if __name__ == "__main__":
  clus = clusmin(
    data_func = lambda: [{"text" : "a"}, {"text" : "b"}],
    prepare_func = lambda a: a+1, 
    select_features_func = None, 
    build_corpus_func = None,
    scale_func = None,
    vectorize_func = None,
    topic_model_func = None,
    algorithm_func = None,
    search_space_func = None,
    cost_func = None
  )
  print("bla")
  clus()




