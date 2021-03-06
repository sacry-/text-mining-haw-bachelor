import os

from nltk.tag.stanford import NERTagger


def get_tagger(tokens):
  ner_jar, classifier = os.environ["STANFORD_NER_JAR"], os.environ["STANFORD_NER_CLASSIFIER"]  
  stanford_tagger = NERTagger( classifier, ner_jar )
  return NerTagger(stanford_tagger, tokens)


class NerTagger():

  def __init__(self, tagger, tokens):
    self.tagger = tagger
    self.tokens = tokens
    self.tagged = None
    self.entities = []

  def get_entities(self):
    if not self.entities:
      self.__tag__()
      return self.__extract__()
    return self.entities

  def is_tagged(self):
    return self.tagged != None

  def __tag__(self):
    if not self.is_tagged():
      self.tagged = self.tagger.tag( self.tokens )
    return self.tagged

  def __extract__(self):
    for sentence in self.tagged:

      tagged_entities = []
      for (word, tag) in sentence:
        if tag != "O":
          tagged_entities.append( (word, tag) )

        else:

          if tagged_entities:
            entity_tokens = [ w for (w, t) in tagged_entities ]
            entity = " ".join( entity_tokens )
            tag = tagged_entities[0][1]
            tagged_entity = ( entity, tag )
            self.entities.append(tagged_entity)

          tagged_entities = []

    return self.entities


if __name__ == "__main__":
  from preprocessing.syntax import tokenize

  s = "When Mina Liccione packed her clown\u2019s nose and tap shoes and moved to the Middle East in 2008, she had no real idea how it would turn out.\n\nIt turned out like this: driving through the Jordanian desert dressed in striped pull-up socks, mismatched clothes and look-twice spectacles, on her way to an audience of hundreds of Syrian children who hadn\u2019t had a proper laugh in a long time.\n\n\u201cA young boy was peering out from behind a thick sheet being used as a doorway,\u201d Liccione recalls of last summer\u2019s venture by her Clowns Who Care project. \u201cHe walked outside slowly, staring at us as we drove in. I remember wondering if he was going to smile. I waved, and he waved back.\n\n\u201cBut no smile; not yet anyway.\u201d\n\nSmiles are what she and her Emirati comedian business partner and husband, Ali al-Sayed, live for. The pair, who have been taking their comedy across the Middle East and Africa for seven years, are passionate about bringing joy to communities that may not otherwise find it.\n\nBut if you\u2019d asked the couple a few years ago where they would be today, doing comedy charity work in the Middle East would not have been their answer.\n\n\u201cIn 2007 I was booked to perform in Dubai as part of an arts festival,\u201d Liccione says. \u201cThe trip was meant to be 10 days but it turned into a month as I kept getting hired to compere, teach or perform comedy.\n\n\u201cEveryone I met kept saying there wasn\u2019t enough comedy here and suggested I come back and open the first comedy and urban-arts school in the region.\u201d\n\nWhich is what she did in 2008.\n\n\u201cI took a leap of faith and came armed with tap shoes, notebooks packed with material, a clown nose and years of experience,\u201d she says. \u201cBack in Dubai, I started teaching comedy \u2013 stand-up, improv and physical comedy \u2013 and launched Dubomedy, with my now husband Ali, in April 2008.\u201d\n\nThat\u2019s when UAE-born comedian Sayed ditched his corporate job to go funny full time. The Clowns Who Care project came about a year later, when he and Liccione decided to offer support to \u201ccentres for children and adults with special needs, senior citizens, charity organisations and hospitals\u201d.\n\nSoon after establishing Clowns Who Care, the pair were invited to Uganda.\n\n\u201cWe were helping out at the Live It Up home for rescued children and were so deeply moved by the kids there that we asked what more we could do,\u201d Liccione says. \u201cThe director said the kids get bored over the summer, so we organised an arts camp and went back.\u201d\n\nThen, in 2011, the Syrian conflict flared up.\n\nFacebook Twitter Pinterest Ali al-Sayed of Clowns Who Care with a young audience member. Photograph: Dubomedy Arts\n\n\u201cOur hearts broke while watching the news,\u201d Liccione says. \u201cWe desperately wanted to do something, so we decided to take Clowns Who Care to Jordan, which is where many of the Syrian refugee camps are.\u201d\n\nIn June 2014, the team \u2013 made up of Liccione , Sayed and 10 volunteers, most of them former Dubomedy students \u2013 set off to the tented camp of Sahab, about an hour\u2019s drive from Amman to launch Operation: Joy to Sahab. With the help of the global aid agency Mercy Corps, they organised two-day sessions for young people from the 300 families living in the camp at the time.\n\n\u201cWhen we visit these camps, we do performing-arts workshops with the kids,\u201d Liccione explains. \u201cWe incorporate dance, music with recycled objects, physical comedy routines, acrobatics, circus skills and rhythm work.\u201d\n\nAnd where does the clowning come into it? \u201cWe perform for the kids too,\u201d she adds. \u201cOur style of clowning is European, incorporating physical comedy and being a lot more neutral and community oriented, making it more inviting.\u201d\n\nSayed says the team also does \u201cvisual-arts projects with the children, which is why our suitcases are always full of paper, glue, scissors, pipe cleaners, fabric, markers and Polaroid cameras. The guys at airport security must really wonder what kind of holiday we\u2019re going on.\u201d\n\nOn the couple\u2019s second trip to Jordan, in December 2014, the team \u201cdid a 10-show, 10-workshop marathon in the Azraq and Zaatari refugee camps over three days,\u201d Sayed says. \u201cWe wanted to reach as many kids as possible, as well as to help train teachers to continue the work we had started.\u201d\n\nOur style of clowning, being a lot more neutral and community orientated, is more inviting Mina Liccione\n\nLiccione says that while the opportunity to work with refugees is a blessing, there are tough days. \u201cWe were teaching the children to dance in one of the smaller camps when a man who lived in the tent next door came over to watch with his wife and baby girl,\u201d she says.\n\n\u201cAfter we were done he approached us and, even though he had very little, he insisted on making us tea. We sat and drank with him, which is when he told us his little girl was small for her age because his wife couldn\u2019t breastfeed.\n\n\u201cHe went on to explain she was the only child in their family who survived. Walking on foot from Syria meant that many of the refugees froze during the winter of 2014 and didn\u2019t make it to the camps. It was gut-wrenching to hear him speak, yet we couldn\u2019t cry in front of him. He was so proud of what he had left. He came to visit us the next day and watched every workshop with a big smile, his baby girl in his arms.\u201d\n\nSayed is looking ahead: \u201cWe plan on returning to Jordan this summer to work in the Syrian and Palestinian refugee camps, as well as in camps in Lebanon and Turkey. We\u2019re also hoping to branching out to Bangladesh to work with kids from the slums.\u201d\n\nThe Clowns Who Care project doesn\u2019t accept monetary donations but does encourage support from volunteers. \u201cThe best way to get involved is to email lol@dubomedy.com,\u201d Liccione says. \u201cWe also have a Facebook group for volunteers where we post call-outs and people sign up to help.\u201d"
  tokens = tokenize(s)

  ner_tagger = get_tagger(tokens)
  for e in ner_tagger.get_entities():
    print(e)

