# encoding: utf-8
import enchant 
from langdetect import detect
from nltk.corpus import brown, reuters
from nltk.corpus import wordnet as wn
from nltk import word_tokenize
from nltk.corpus import stopwords
from nltk import data

from textblob import TextBlob
from textblob_aptagger import PerceptronTagger
from textblob.np_extractors import ConllExtractor

STOPS = stopwords.words('english')
SENTENCE_DETECTOR = data.load('tokenizers/punkt/english.pickle')
TAGGER = PerceptronTagger()
EXTRACTOR = ConllExtractor()
EN_US_DICT = enchant.Dict("en_US")
EN_GB_DICT = enchant.Dict("en_GB")

def sentence_tokenize(s, f=lambda x: x):
  sentences = []
  for sentence in SENTENCE_DETECTOR.tokenize(s.strip()):
    try:
      if detect(sentence) == "en":
        words = word_tokenize(sentence)
        sentences.append( f(words) )
    except:
      pass
  return sentences

def remove_stopwords( words ):
  result = []
  for word in words:
    if not word.strip() in STOPS:
      result.append( word )
  return result

def as_tokens(text, f=lambda x: x):
  return [word for sentence in sentence_tokenize( text, f ) for word in sentence]

def splitter(seq):
  seq_ = []
  for e in seq:
    seq_ += e.split(" ")
  return seq_

def hyperfy(bag):
  lowest_hypernyms = []
  for (t1, t2) in zip(bag, bag[1:]):
    s1 = wn.synsets(t1)
    s2 = wn.synsets(t2)

    for (syn1, syn2) in zip(s1, s2):
      hyper = syn1.lowest_common_hypernyms(syn2)
      lowest_hypernyms += hyper
      
  return list(set(lowest_hypernyms))

def get_nouns( text ):
  t = sentence_tokenize(text)
  text = " ".join(map(lambda x: " ".join(x), t))
  blob = TextBlob(text)
  print(blob.noun_phrases)
  return blob.noun_phrases

if __name__ == "__main__":
  text = str("In April 2014, nine bloggers and journalists were arrested in Ethiopia. Several of these men and women had worked with Zone9, a collective blog that covered social and political issues in Ethiopia and promoted human rights and government accountability. And four of them were Global Voices authors. In July 2014, they were charged under the country’s Anti-Terrorism Proclamation. They have been behind bars ever since and their trial has only recently begun. This post is part of our series – “They Have Names” – that seeks to highlight the individual bloggers who are currently in jail. We wish to humanize them, to tell their particular and peculiar stories. This story comes from Endalk Chala, a founding member of the Zone9 collective who was spared arrest on account of being in the United States, where he is pursuing a PhD in Media Studies. I first came to know Edom Kassaye through Befeqadu, the great convener of the Zone9 blogging collective. We met in 2012, when she had just returned from a year-long reporting trip in Kenya. She furnished me with many wonderful stories that she covered during her trip. The stories she told me and the relative journalistic freedom she experienced in Kenya generated deep conversations about the unfortunate situation of Ethiopia’s freedom of expression. From then on, until I left the country in 2013, Edom and I met frequently for coffee. We grew to become good friends. When I think about my time with Edom, I realize it is no wonder that she got arrested along with six members of the Zone9 collective. People ask why Edom was arrested and charged with terrorism when she was not a member of the group. I believe it was Edom’s willingness to bring about a gentle change in Ethiopia’s polarized political environment that suggested an affinity between her and the Zone9 blogging collective. We shared common principles. Edom participated in every single online campaign the Zone9 blogging collective held. It seems that her participation in the online campaigns got her noticed by state authorities monitoring social networks. In the days and weeks leading up to her arrest, Edom resisted pressure to serve as an informant about her friends from the collective. Instead, she opted to be jailed with her friends. Her integrity and convictions demonstrate something special about her character — her intense commitment to active citizenship within an increasingly brainwashed and fragmented populous. Jomanex, an exiled blogger, a colleague and friend often calls Edom ‘Miss Integrity’. Edom is one of the few female journalists I know in the country who practiced journalism on multiple platforms. Her CV reads as a fast-growing multimedia journalist with keen interest in environment, public health, and social justice. For outsiders, Edom looked like any young aspiring journalist whose works appeared everywhere from state-owned daily newspaper to independent Addis Ababa radio stations. But a few details set her apart. Edom began her journalism career at the state-owned daily newspaper. Working as a senior reporter, she tried to inspire optimism about hihg-quality journalism that the Ethiopian state media has rarely exhibited. But her tendency to ask critical questions was incompatible with the sycophantic culture of state journalism and she decided to take a different career path. In 2011, she won her reporting fellowship in Kenya, where she focused on environmental reporting. Upon her return, she decided not to work for state media, opting instead to freelance for various media organizations. When we began Global Voices’ Amharic language site in 2012 she served as a volunteer translator for the site. In 2013, Edom, Befeqadu, Zelalem and I worked together to produce a report on the state of freedom of expression in Ethiopia which later was submitted to United Nations Commission on Human Rights for their Universal Periodic Review. In 2011, the government arrested and prosecuted more than 12 journalists on sham terrorism charges, an act that has become routine since 2005. Edom took pride in showing solidarity with these journalists. She routinely traveled back and forth to the prisons to visit award-winning journalists such as Reeyot Alemu and Eskinder Nega, who are still serving their long prison terms. This gave Edom a glimpse of what these journalists’ lives looked like in prison. As a gesture of her solidarity toward the journalists, she regularly tweeted the counts of the days the journalists were made to spend in the prison. I wonder if she ever imagined that she would share a similar fate with them. Once I asked her where she drew the inspiration for using her Twitter handle as timer to document the dire situation of the journalists. She told me that in Kality Prison, where Eskinder Nega is held, the guards count prisoners every morning using morning whistles. They shout loudly – ‘Kotera፣ Kotera፣ Kotera’ which means make yourselves available for the tally, for the tally, for the tally. This ritual is common throughout the prison system in Ethiopia. It has two purposes: the first is to make the prisoners arise early; the second is to make the prisoners available for morning count. Edom poignantly took this counting ritual and used it in her tweets, to document the days the journalists were forced to spend behind bars. Edom did this until the day she herself become one of them. Since April 25, 2014, Edom has been denied her tweeting rights for showing solidarity with these jailed journalists. In her prison journal, where she narrated how she was arrested, she wrote: ወዲያው ልሂድ ብሎ ወጣ ጣፋጭ በር ላይ ተሰነባበትን ፡፡ ወዲያው አስፓልቱን ስሻገር አንድ መኪና መንገድ ዘጋብኝና ሁለት ተራ ወንበዴዎች የመሰሉ ሰዎች አንድገባ አዘዙኝ፡፡ አልገባም አልኩኝ ፡፡አንደኛው እጄን ጠምዝዞ አስገድዶ ወደመኪናው መራኝ ያኔ መከራከሩ እንደማያወጣ ገባኝ፡፡ ከኋላ አስገብተውኝ ግራና ቀኝ ተቀመጡ፡፡ መኪናዋን ይኸው የትምህርት ቤት ወዳጄ ይዟት እንዳየሁ አስታወስኩ፡። ቆሻሻና ዳሽ ቦርድ የሌላት መኪና ናት፡። ከነሹፌሩ የቀን ስራ ሲሰሩ ውለው ያላባቸው የሚመስሉ ሶስት ወጣቶች አሉ፡፡ ጋቢና ያለው ወጣት “ኤዲ አንዴት ነሽ ?” አለኝ ጸጥ አልኩኝ፡፡ ፓሊስ ጣቢያ ለጉዳይ አንደፈለጉኝ እና ቶሎ አንደምለቀቅ ተናግሮ ሊያረጋጋኝ ሞከረ፡፡ ሹፌሩ ያለምንም ማቅማማት ጥቁር አንበሳ እና ባንኮዲሮማ ህንጻ ጋር ያሉትን መብራቶች እየጣሰ ጉዞ ወደፒያሳ ሆነ፣ ምን እነዳጣደፈው እንጃ ።። ቤተሰቦቼ ጋር አንድደውል ይፈቀድልኝ ብልም ስልኬን ወስደው ፍቃደኛ ሳይሆኑ ቀሩ ፡፡ ማአከላዊ ስንደርስ 12.50 አካባቢ ሆኗል፡፡ መደበኛ ምዝገባ ተደርጎልኝ ንብረቶቼን አስረከብኩ ፣ እርቃኔን ከሆንኩ በኋላ ቁጭ ብድግ እያልኩ ሰውነቴ ሁሉ ተፈትሿል፡፡ ከታሰሩ ሴቶች ጋር ስቀላቀል እራትና የሌሊት ልብስ ሰጡኝ፡። ከጥቂት ሰአታት በኋላ የእግር ኮቴ ስንሰማ ተሽቀዳድመን በቀዳዳ ስናይ ማህሌትን ወደ ሌላ ክፍል ሲያስገቧት አየሁ ፡፡ ያኔ ለመጀመሪያ ጊዜ አለቀስኩ ፡፡ ቤተሰቦቼ ልጃችን ምን ዋጣት ብለው አንዴት አንደሚነጋላቸው እየተጨነኩ ነጋ፡፡ As I walked across the street a vehicle approached me and closed my walkway. Then a couple of hooligan looking men jumped off the car and swarmed at me and they started to ask me to get on to the vehicle. When I resisted getting on to the vehicle one of the men twisted my wrist; at that moment I just recognized my fight not to be arrested is a futile one but I get on to the car defiantly then squeezed into the back seat in the middle of two men. Seating in the car with reflexive silence I asked them to let me make a telephone call to my family. They denied me and seized my mobile phone violently …. Near sundown we arrived at notorious Maekelawi, Federal Police Investigation Centre. I passed through a dehumanizing search before they led me to a dark cell to be with other inmates…. After a while I heard footsteps we all swarmed to have a look through a peephole to see what is going on then I have seen Mahlet being escorted to other cell….At that moment I felt a reflexive horror for my family since they would extremely be worried about my whereabouts and I felt my tears wetting my cheek. Edom has done journalism along with her understated activism with a remarkable elegance. She has her own unique and polite way of making sure she gets her point across without being intimidating or manipulative. Two months ahead of my departure to the US for my graduate studies, Edom traveled to Tunisia and on her return, brought me a palm-shaped key holder which is popularly believed to provide protection from evil. It pains me that I could not give Edom protection from the wickedness of our government. I cherish every minute I spent with Edom, a woman who bravely stands for her convictions.")
  bag = as_tokens(text, remove_stopwords)
  hypernyms = hyperfy( bag )
  for nym in hypernyms:
    print( nym )



