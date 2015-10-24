from textblob import TextBlob
from textblob_aptagger import PerceptronTagger
from textblob.np_extractors import ConllExtractor
from prepare import Prepare

TAGGER = PerceptronTagger()
EXTRACTOR = ConllExtractor()

s = "Along with more than 600 other fellow artists, we are announcing today that we will not engage in business-as-usual cultural relations with Israel. We will accept neither professional invitations to Israel, nor funding, from any institutions linked to its government. Since the summer war on Gaza, Palestinians have enjoyed no respite from Israel’s unrelenting attack on their land, their livelihood, their right to political existence. “2014,” says the Israeli human rights organisation B’Tselem, was “one of the cruellest and deadliest in the history of the occupation.” The Palestinian catastrophe goes on. Israel’s wars are fought on the cultural front too. Its army targets Palestinian cultural institutions for attack, and prevents the free movement of cultural workers. Its own theatre companies perform to settler audiences on the West Bank – and those same companies tour the globe as cultural diplomats, in support of “Brand Israel”. During South African apartheid, musicians announced they weren’t going to “play Sun City”. Now we are saying, in Tel Aviv, Netanya, Ashkelon or Ariel, we won’t play music, accept awards, attend exhibitions, festivals or conferences, run masterclasses or workshops, until Israel respects international law and ends its colonial oppression of the Palestinians. To see the full list of supporters, go to artistsforpalestine.org.uk. Khalid Abdalla, Riz Ahmed, Peter Ahrends, Hanan Al-Shaykh, Will Alsop, Richard Ashcroft, John Berger, Bidisha, Nicholas Blincoe, Leah Borrromeo, Haim Bresheeth, Victoria Brittain, Niall Buggy, Tam Dean Burn, Jonathan Burrows, David Calder, Anna Carteret, Taghrid Choucair-Vizoso, Ian Christie, Caryl Churchill, Sacha Craddock, Liam Cunningham, Selma Dabbagh, Colin Darke, April De Angelis, Andy de la Tour, Ivor Dembina, Shane Dempsey, Elaine Di Campo, Patrick Driver, Earl Okin, Sally El Hosaini, Brian Eno, Gareth Evans, Annie Firbank, James Floyd, Aminatta Forna, Jane Frere, Kadija George, Bob Giles, Mel Gooding, Tony Graham, Omar Robert Hamilton, Jeremy Hardy, Mike Hodges, James Holcombe, Rachel Holmes, Adrian Hornsby, Rose Issa, Ann Jungman, John Keane, Brigid Keenan, Hannah Khalil, Shahid Khan, Peter Kosminsky, Hari Kunzru, Paul Laverty, Alisa Lebow, Mike Leigh, Tom Leonard, Sonja Linden, Phyllida Lloyd, Ken Loach, Liz Lochhead, David Mabb, Sabrina Mahfouz, Miriam Margolyes, Kika Markham, Simon McBurney, Sarah McDade, Jimmy McGovern, Pauline Melville, Roger Michell, China Miéville, Russell Mills, Laura Mulvey, Jonathan Munby, Courttia Newland, Lizzie Nunnery, Rebecca O’Brien, Treasa O’Brien, Andrew O’Hagan, Jeremy Page, Timothy Pottier, Michael Radford, Maha Rahwanji, Ravinder Randhawa, Siobhan Redmond, Lynne Reid Banks, Ian Rickson, Leon Rosselson, Kareem Samara, Leila Sansour, Alexei Sayle, Seni Seneviratne, Kamila Shamsie, Anna Sherbany, Eyal Sivan, Gillian Slovo, John Smith, Max Stafford-Clark, Maggie Steed, Sarah Streatfeild, Mitra Tabrizian, Mark Thomas, Cat Villiers, Roger Waters, Esther Wilson, Penny Woolcock, Susan Wooldridge, Emily Young, Andrea Luka Zimmerman "
prepared = Prepare(s, options=["remove_alpha"]).s
blob = TextBlob(prepared, pos_tagger=TAGGER, np_extractor=EXTRACTOR) 
print(blob.noun_phrases)