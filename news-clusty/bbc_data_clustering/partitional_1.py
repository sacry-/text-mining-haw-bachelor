import data_view

from preprocessing import get_configured_ner_tagger
from preprocessing import sentence_word_tokenize

from utils import flatten


labels = data_view.get_bbc_categories()
titles = data_view.get_bbc_titles()
sents = data_view.get_bbc_sents()


tokens = flatten(sentence_word_tokenize(raw_text))

ner_tagger = get_configured_ner_tagger(tokens)
ners = ner_tagger.get_entities()
print(ners)

