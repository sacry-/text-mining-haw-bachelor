from utils import normalize_title

from preprocessing import TextNormalizer
from preprocessing import sentence_tokenize
from preprocessing import Preprocessor

def tokenizer(text):
  return [word for sentence in sentence_tokenize( text ) for word in sentence]

def semantics(doc):
  tn = TextNormalizer(options=["keep_alpha"])
  normalized = tn.normalize(doc)
  prep = Preprocessor(normalized, tokenizer)
  pos = prep.pos_tags()
  nouns = prep.noun_phrases()
  ners = prep.ner_extract()
  return pos, nouns, ners

def bbc_parser(doc):  
  s = doc.split("\n")
  title = s[0]
  _id = normalize_title(title)

  print("Parsing: {}".format(_id))

  tn = TextNormalizer()
  pos, nouns, ners = semantics(doc)
  nouns = tn.fmap(nouns)
  
  paragraphs = []
  sentences = []
  for line in s[1:]:
    if not line:
      continue
    sentences += tn.fmap(sentence_tokenize(line))
    paragraphs.append( tn.normalize(line) )

  return {
    "id" : _id,
    "title" : title,
    "sents" : sentences,
    "paras" : paragraphs,
    "pos" : pos,
    "nouns" : nouns,
    "ners" : ners
  }




t = '''Watchdog probes e-mail deletions

The information commissioner says he is urgently asking for details of Cabinet Office orders telling staff to delete e-mails more than three months old.

Richard Thomas "totally condemned" the deletion of e-mails to prevent their disclosure under freedom of information laws coming into force on 1 January. Government guidance said e-mails should only be deleted if they served "no current purpose", Mr Thomas said. The Tories and the Lib Dems have questioned the timing of the new rules.

Tory leader Michael Howard has written to Tony Blair demanding an explanation of the new rules on e-mail retention. On Monday Lib Dem constitutional affairs committee chairman Alan Beith warned that the deletion of millions of government e-mails could harm the ability of key probes like the Hutton Inquiry. The timing of the new rules just before the Freedom of Information Act comes into forces was "too unlikely to have been a coincidence", Mr Beith said. But a Cabinet Office spokeswoman said the move was not about the new laws or "the destruction of important records". Mr Beith urged the information commissioner to look at how the "e-mail regime" could "support the freedom of information regime".

Mr Thomas said: "The new Act of Parliament makes it very clear that to destroy records in order to prevent their disclosure becomes a criminal offence." He said there was already clear guidance on the retention of e-mails contained in a code of practice from the lord chancellor. All e-mails are subject to the freedom of information laws, but the important thing was the content of the e-mail, said Mr Thomas.

"If in doubt retain, that has been the long-standing principle of the civil service and public authorities. It's only when you've got no further use for the particular record that it may be legitimate to destroy it. "But any deliberate destruction to avoid the possibility of later disclosure is to be totally condemned." The Freedom of Information Act will cover England, Wales and Northern Ireland from next year. Similar measures are being brought in at the same time in Scotland. It provides the public with a right of access to information held by about 100,000 public bodies, subject to various exemptions. Its implementation will be monitored by the information commissioner.'''

for k, v in bbc_parser(t).items(): 
  print(k, v)



