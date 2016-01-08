from collections import defaultdict
from collections import Counter

from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import normalize

from features import tfidf_vector
from features import count_vector
from features import lsa
from features import pca
from features import lda

from clustering import ward_linkage 
from clustering import kmeans
from clustering import birch
from clustering import plot

from io_utils import print_top_words
from os import listdir

from preprocessing import TextNormalizer

import re


STOPS = [
  "emph",
  "section",
  "subsection",
  "subsubsection",
  "paragraph",
  "cite",
  "chapter",
  "newcommand",
  "begin",
  "end",
  "table",
  "figure",
  "includegraphics",
  "ref",
  "label",
  "caption",
  "_",
  "mu",
  "png",
  "width",
  "textwidth",
  "tex",
  "hline",
  "usepackage",
  "kbordermatrix",
  "frac",
  "state",
  "return",
  "colorlet",
  "color",
  "gray",
  "gets", 
  "centering",
  "item",
  "newpage",
  "save",
  "box", 
  "quote",
  "ltiple",
  "sec",
  "wn"
]

IMPORTS = [
  "imports_definitions.tex",
  "citations.tex",
  "lexicon.tex",
  "thesis.tex"
]

ORDER = [
  "abstract.tex",
  "introduction.tex",
  "basics.tex",
  "data_pipeline.tex",
  "feature_selection.tex",
  "clustering_experiments.tex",
  "results_and_discussion.tex",
  "outlook.tex"
]

class ThesisData():

  def __init__(self, model_name=None):
    self.model_name = model_name
    if not self.model_name:
      self.model_name = "../../ba-clusty/latex"

  def read(self):
    text_normalizer = TextNormalizer()

    documents = {}
    for tex_path in self.yield_files():
      vec = self.with_open(tex_path)
      vec_norm = [ token for token in 
                   text_normalizer.fmap( vec ) 
                   if token.strip() ]
      vec_stop = self.remove_latex( vec_norm )
      if vec_stop: 
        tex_file = tex_path.split("/")[-1]
        documents[tex_file] = (tex_file, vec_stop) 

    return documents

  def with_open(self, tex_path):
    with open(tex_path, "r+") as features:
      return [feature for feature in features]

  def yield_files(self):  
    files = ["{}/{}".format(self.model_name, f) for f 
           in listdir(self.model_name) if not f in IMPORTS]
    return [f for f in files if ".tex" in f]

  def remove_latex(self, vec):
    vec_s = " ".join( vec )
    for stop_word in STOPS:
      vec_s = vec_s.replace(stop_word, "")
    return [t for t in vec_s.split(" ") if t.strip()]


if __name__ == "__main__":
  data = ThesisData()
  data_dict = data.read()
  for entry in ORDER:
    try:
      tex_file, doc = data_dict[entry]
      z, vsmodel = count_vector( doc, ngram=(1,1), max_df=0.8, min_df=2 )
      z, lda_model = lda( z, n_topics=3 )
      print("Summarized", tex_file)
      print_top_words(lda_model, vsmodel.get_feature_names(), 30)
    except:
      print("Could not summarize", tex_file)
