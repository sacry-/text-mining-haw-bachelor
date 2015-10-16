from preprocessing.syntax import sentence_tokenize
from preprocessing.ner_tagger import get_configured_ner_tagger
from preprocessing.chunk import Chunk
from preprocessing.prepare import Prepare

from utils import date_today
from textblob import TextBlob
from textblob_aptagger import PerceptronTagger
from textblob.np_extractors import ConllExtractor
from elasticsearch_dsl import DocType, String


def preprocessor_from_chunk(chunk, tokenizer=None):
  pre = preprocess(chunk, tokenizer)

  prep = Prep(
    meta={'id' : chunk.id}, 
    tokens=pre.tokens,
    pos_tags=pre.pos_tags(),
    noun_phrases=pre.noun_phrases(),
    ner_tags=pre.ner_extract()
  )

  prep._index = chunk.index
  return prep


TAGGER = PerceptronTagger()
EXTRACTOR = ConllExtractor()

class Preprocessor():

  def __init__(self, text, tokenizer):
    self.text = str(text)
    self.tokenizer = tokenizer
    self.tokens = self.tokenizer( self.text )
    self.blob = TextBlob(self.text, pos_tagger=TAGGER, np_extractor=EXTRACTOR) 
    self.ner_tagger = get_configured_ner_tagger(self.tokens)

  def pos_tags(self):
    return self.blob.tags

  def noun_phrases(self):
    return self.blob.noun_phrases

  def ner_extract(self):
    self.ner_tagger.tag()
    return self.ner_tagger.extract()


class Prep(DocType):
  tokens = String(fields={'raw': String(index='not_analyzed')})
  pos_tags = String(fields={'raw': String(index='not_analyzed')})
  noun_phrases = String(fields={'raw': String(index='not_analyzed')})
  ner_tags = String(fields={'raw': String(index='not_analyzed')})

  class Meta:
    index = date_today()

  def save(self, ** kwargs):
    return super(Prep, self).save(** kwargs)

def preprocess(chunk, tokenizer=None):
  
  def default_tokenizer(text):
    return [word for sentence in sentence_tokenize( text ) for word in sentence]
  
  if not tokenizer:
    tokenizer = default_tokenizer

  print("Preprocessing start", chunk.index, chunk.id)
  chunk.text = Prepare(chunk.text).s
  pre = Preprocessor(chunk.text, tokenizer)
  pre.pos_tags()
  pre.noun_phrases()
  pre.ner_extract()
  
  return pre


if __name__ == "__main__":
  text = "When Mina Liccione packed her clown\u2019s nose and tap shoes and moved to the Middle East in 2008, she had no real idea how it would turn out.\n\nIt turned out like this: driving through the Jordanian desert dressed in striped pull-up socks, mismatched clothes and look-twice spectacles, on her way to an audience of hundreds of Syrian children who hadn\u2019t had a proper laugh in a long time.\n\n\u201cA young boy was peering out from behind a thick sheet being used as a doorway,\u201d Liccione recalls of last summer\u2019s venture by her Clowns Who Care project. \u201cHe walked outside slowly, staring at us as we drove in. I remember wondering if he was going to smile. I waved, and he waved back.\n\n\u201cBut no smile; not yet anyway.\u201d\n\nSmiles are what she and her Emirati comedian business partner and husband, Ali al-Sayed, live for. The pair, who have been taking their comedy across the Middle East and Africa for seven years, are passionate about bringing joy to communities that may not otherwise find it.\n\nBut if you\u2019d asked the couple a few years ago where they would be today, doing comedy charity work in the Middle East would not have been their answer.\n\n\u201cIn 2007 I was booked to perform in Dubai as part of an arts festival,\u201d Liccione says. \u201cThe trip was meant to be 10 days but it turned into a month as I kept getting hired to compere, teach or perform comedy.\n\n\u201cEveryone I met kept saying there wasn\u2019t enough comedy here and suggested I come back and open the first comedy and urban-arts school in the region.\u201d\n\nWhich is what she did in 2008.\n\n\u201cI took a leap of faith and came armed with tap shoes, notebooks packed with material, a clown nose and years of experience,\u201d she says. \u201cBack in Dubai, I started teaching comedy \u2013 stand-up, improv and physical comedy \u2013 and launched Dubomedy, with my now husband Ali, in April 2008.\u201d\n\nThat\u2019s when UAE-born comedian Sayed ditched his corporate job to go funny full time. The Clowns Who Care project came about a year later, when he and Liccione decided to offer support to \u201ccentres for children and adults with special needs, senior citizens, charity organisations and hospitals\u201d.\n\nSoon after establishing Clowns Who Care, the pair were invited to Uganda.\n\n\u201cWe were helping out at the Live It Up home for rescued children and were so deeply moved by the kids there that we asked what more we could do,\u201d Liccione says. \u201cThe director said the kids get bored over the summer, so we organised an arts camp and went back.\u201d\n\nThen, in 2011, the Syrian conflict flared up.\n\nFacebook Twitter Pinterest Ali al-Sayed of Clowns Who Care with a young audience member. Photograph: Dubomedy Arts\n\n\u201cOur hearts broke while watching the news,\u201d Liccione says. \u201cWe desperately wanted to do something, so we decided to take Clowns Who Care to Jordan, which is where many of the Syrian refugee camps are.\u201d\n\nIn June 2014, the team \u2013 made up of Liccione , Sayed and 10 volunteers, most of them former Dubomedy students \u2013 set off to the tented camp of Sahab, about an hour\u2019s drive from Amman to launch Operation: Joy to Sahab. With the help of the global aid agency Mercy Corps, they organised two-day sessions for young people from the 300 families living in the camp at the time.\n\n\u201cWhen we visit these camps, we do performing-arts workshops with the kids,\u201d Liccione explains. \u201cWe incorporate dance, music with recycled objects, physical comedy routines, acrobatics, circus skills and rhythm work.\u201d\n\nAnd where does the clowning come into it? \u201cWe perform for the kids too,\u201d she adds. \u201cOur style of clowning is European, incorporating physical comedy and being a lot more neutral and community oriented, making it more inviting.\u201d\n\nSayed says the team also does \u201cvisual-arts projects with the children, which is why our suitcases are always full of paper, glue, scissors, pipe cleaners, fabric, markers and Polaroid cameras. The guys at airport security must really wonder what kind of holiday we\u2019re going on.\u201d\n\nOn the couple\u2019s second trip to Jordan, in December 2014, the team \u201cdid a 10-show, 10-workshop marathon in the Azraq and Zaatari refugee camps over three days,\u201d Sayed says. \u201cWe wanted to reach as many kids as possible, as well as to help train teachers to continue the work we had started.\u201d\n\nOur style of clowning, being a lot more neutral and community orientated, is more inviting Mina Liccione\n\nLiccione says that while the opportunity to work with refugees is a blessing, there are tough days. \u201cWe were teaching the children to dance in one of the smaller camps when a man who lived in the tent next door came over to watch with his wife and baby girl,\u201d she says.\n\n\u201cAfter we were done he approached us and, even though he had very little, he insisted on making us tea. We sat and drank with him, which is when he told us his little girl was small for her age because his wife couldn\u2019t breastfeed.\n\n\u201cHe went on to explain she was the only child in their family who survived. Walking on foot from Syria meant that many of the refugees froze during the winter of 2014 and didn\u2019t make it to the camps. It was gut-wrenching to hear him speak, yet we couldn\u2019t cry in front of him. He was so proud of what he had left. He came to visit us the next day and watched every workshop with a big smile, his baby girl in his arms.\u201d\n\nSayed is looking ahead: \u201cWe plan on returning to Jordan this summer to work in the Syrian and Palestinian refugee camps, as well as in camps in Lebanon and Turkey. We\u2019re also hoping to branching out to Bangladesh to work with kids from the slums.\u201d\n\nThe Clowns Who Care project doesn\u2019t accept monetary donations but does encourage support from volunteers. \u201cThe best way to get involved is to email lol@dubomedy.com,\u201d Liccione says. \u201cWe also have a Facebook group for volunteers where we post call-outs and people sign up to help.\u201d"
  text = "In April 2014, nine bloggers and journalists were arrested in Ethiopia. Several of these men and women had worked with Zone9, a collective blog that covered social and political issues in Ethiopia and promoted human rights and government accountability. And four of them were Global Voices authors. In July 2014, they were charged under the country’s Anti-Terrorism Proclamation. They have been behind bars ever since and their trial has only recently begun. This post is part of our series – “They Have Names” – that seeks to highlight the individual bloggers who are currently in jail. We wish to humanize them, to tell their particular and peculiar stories. This story comes from Endalk Chala, a founding member of the Zone9 collective who was spared arrest on account of being in the United States, where he is pursuing a PhD in Media Studies. I first came to know Edom Kassaye through Befeqadu, the great convener of the Zone9 blogging collective. We met in 2012, when she had just returned from a year-long reporting trip in Kenya. She furnished me with many wonderful stories that she covered during her trip. The stories she told me and the relative journalistic freedom she experienced in Kenya generated deep conversations about the unfortunate situation of Ethiopia’s freedom of expression. From then on, until I left the country in 2013, Edom and I met frequently for coffee. We grew to become good friends. When I think about my time with Edom, I realize it is no wonder that she got arrested along with six members of the Zone9 collective. People ask why Edom was arrested and charged with terrorism when she was not a member of the group. I believe it was Edom’s willingness to bring about a gentle change in Ethiopia’s polarized political environment that suggested an affinity between her and the Zone9 blogging collective. We shared common principles. Edom participated in every single online campaign the Zone9 blogging collective held. It seems that her participation in the online campaigns got her noticed by state authorities monitoring social networks. In the days and weeks leading up to her arrest, Edom resisted pressure to serve as an informant about her friends from the collective. Instead, she opted to be jailed with her friends. Her integrity and convictions demonstrate something special about her character — her intense commitment to active citizenship within an increasingly brainwashed and fragmented populous. Jomanex, an exiled blogger, a colleague and friend often calls Edom ‘Miss Integrity’. Edom is one of the few female journalists I know in the country who practiced journalism on multiple platforms. Her CV reads as a fast-growing multimedia journalist with keen interest in environment, public health, and social justice. For outsiders, Edom looked like any young aspiring journalist whose works appeared everywhere from state-owned daily newspaper to independent Addis Ababa radio stations. But a few details set her apart. Edom began her journalism career at the state-owned daily newspaper. Working as a senior reporter, she tried to inspire optimism about hihg-quality journalism that the Ethiopian state media has rarely exhibited. But her tendency to ask critical questions was incompatible with the sycophantic culture of state journalism and she decided to take a different career path. In 2011, she won her reporting fellowship in Kenya, where she focused on environmental reporting. Upon her return, she decided not to work for state media, opting instead to freelance for various media organizations. When we began Global Voices’ Amharic language site in 2012 she served as a volunteer translator for the site. In 2013, Edom, Befeqadu, Zelalem and I worked together to produce a report on the state of freedom of expression in Ethiopia which later was submitted to United Nations Commission on Human Rights for their Universal Periodic Review. In 2011, the government arrested and prosecuted more than 12 journalists on sham terrorism charges, an act that has become routine since 2005. Edom took pride in showing solidarity with these journalists. She routinely traveled back and forth to the prisons to visit award-winning journalists such as Reeyot Alemu and Eskinder Nega, who are still serving their long prison terms. This gave Edom a glimpse of what these journalists’ lives looked like in prison. As a gesture of her solidarity toward the journalists, she regularly tweeted the counts of the days the journalists were made to spend in the prison. I wonder if she ever imagined that she would share a similar fate with them. Once I asked her where she drew the inspiration for using her Twitter handle as timer to document the dire situation of the journalists. She told me that in Kality Prison, where Eskinder Nega is held, the guards count prisoners every morning using morning whistles. They shout loudly – ‘Kotera፣ Kotera፣ Kotera’ which means make yourselves available for the tally, for the tally, for the tally. This ritual is common throughout the prison system in Ethiopia. It has two purposes: the first is to make the prisoners arise early; the second is to make the prisoners available for morning count. Edom poignantly took this counting ritual and used it in her tweets, to document the days the journalists were forced to spend behind bars. Edom did this until the day she herself become one of them. Since April 25, 2014, Edom has been denied her tweeting rights for showing solidarity with these jailed journalists. In her prison journal, where she narrated how she was arrested, she wrote: ወዲያው ልሂድ ብሎ ወጣ ጣፋጭ በር ላይ ተሰነባበትን ፡፡ ወዲያው አስፓልቱን ስሻገር አንድ መኪና መንገድ ዘጋብኝና ሁለት ተራ ወንበዴዎች የመሰሉ ሰዎች አንድገባ አዘዙኝ፡፡ አልገባም አልኩኝ ፡፡አንደኛው እጄን ጠምዝዞ አስገድዶ ወደመኪናው መራኝ ያኔ መከራከሩ እንደማያወጣ ገባኝ፡፡ ከኋላ አስገብተውኝ ግራና ቀኝ ተቀመጡ፡፡ መኪናዋን ይኸው የትምህርት ቤት ወዳጄ ይዟት እንዳየሁ አስታወስኩ፡። ቆሻሻና ዳሽ ቦርድ የሌላት መኪና ናት፡። ከነሹፌሩ የቀን ስራ ሲሰሩ ውለው ያላባቸው የሚመስሉ ሶስት ወጣቶች አሉ፡፡ ጋቢና ያለው ወጣት “ኤዲ አንዴት ነሽ ?” አለኝ ጸጥ አልኩኝ፡፡ ፓሊስ ጣቢያ ለጉዳይ አንደፈለጉኝ እና ቶሎ አንደምለቀቅ ተናግሮ ሊያረጋጋኝ ሞከረ፡፡ ሹፌሩ ያለምንም ማቅማማት ጥቁር አንበሳ እና ባንኮዲሮማ ህንጻ ጋር ያሉትን መብራቶች እየጣሰ ጉዞ ወደፒያሳ ሆነ፣ ምን እነዳጣደፈው እንጃ ።። ቤተሰቦቼ ጋር አንድደውል ይፈቀድልኝ ብልም ስልኬን ወስደው ፍቃደኛ ሳይሆኑ ቀሩ ፡፡ ማአከላዊ ስንደርስ 12.50 አካባቢ ሆኗል፡፡ መደበኛ ምዝገባ ተደርጎልኝ ንብረቶቼን አስረከብኩ ፣ እርቃኔን ከሆንኩ በኋላ ቁጭ ብድግ እያልኩ ሰውነቴ ሁሉ ተፈትሿል፡፡ ከታሰሩ ሴቶች ጋር ስቀላቀል እራትና የሌሊት ልብስ ሰጡኝ፡። ከጥቂት ሰአታት በኋላ የእግር ኮቴ ስንሰማ ተሽቀዳድመን በቀዳዳ ስናይ ማህሌትን ወደ ሌላ ክፍል ሲያስገቧት አየሁ ፡፡ ያኔ ለመጀመሪያ ጊዜ አለቀስኩ ፡፡ ቤተሰቦቼ ልጃችን ምን ዋጣት ብለው አንዴት አንደሚነጋላቸው እየተጨነኩ ነጋ፡፡ As I walked across the street a vehicle approached me and closed my walkway. Then a couple of hooligan looking men jumped off the car and swarmed at me and they started to ask me to get on to the vehicle. When I resisted getting on to the vehicle one of the men twisted my wrist; at that moment I just recognized my fight not to be arrested is a futile one but I get on to the car defiantly then squeezed into the back seat in the middle of two men. Seating in the car with reflexive silence I asked them to let me make a telephone call to my family. They denied me and seized my mobile phone violently …. Near sundown we arrived at notorious Maekelawi, Federal Police Investigation Centre. I passed through a dehumanizing search before they led me to a dark cell to be with other inmates…. After a while I heard footsteps we all swarmed to have a look through a peephole to see what is going on then I have seen Mahlet being escorted to other cell….At that moment I felt a reflexive horror for my family since they would extremely be worried about my whereabouts and I felt my tears wetting my cheek. Edom has done journalism along with her understated activism with a remarkable elegance. She has her own unique and polite way of making sure she gets her point across without being intimidating or manipulative. Two months ahead of my departure to the US for my graduate studies, Edom traveled to Tunisia and on her return, brought me a palm-shaped key holder which is popularly believed to provide protection from evil. It pains me that I could not give Edom protection from the wickedness of our government. I cherish every minute I spent with Edom, a woman who bravely stands for her convictions."

  prep = preprocess( Chunk(text) )

  print("--------- tokens: -----")
  print(prep.tokens)
  print("--------- pos tags: -----")
  print(prep.pos_tags())
  print("--------- blob ner: -----")
  print(prep.noun_phrases())
  print("--------- stanford ner: -----")
  for e in prep.ner_extract():
    print(e.entities)
  print("  finished")



