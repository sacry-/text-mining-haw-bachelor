import requests
import os 
import re

from preprocessing import TextNormalizer
from collections import defaultdict
from utils.helpers import flatten


def get_categories():
  h = {}
  h["world"] = [
    "Public_administration",
    "Political_science",
    "Sociology",
    "Social_work",
    "International_relations",
    "Demographics",
    "War", 
    "Rights", 
    "Politics", 
    "Peace",
    "Organizations", 
    "Military", 
    "Mass_media", 
    "Law",
    "Activism", 
    "Crime", 
    "Education", 
    "Ethnic_groups", 
    "Family", 
    "Globalization", 
    "Government", 
    "Infrastructure",
    "Heads_of_state",
    "Political_people",
    "Rivalry", 
    "Social_groups",
    "Subcultures",
    "Cities", 
    "Communities", 
    "Continents", 
    "Countries"
  ]
  h["entertainment"] = [
    "Arts_and_crafts",
    "Celebrity",
    "Censorship_in_the_arts",
    "Festivals",
    "Humor", 
    "Literature",
    "Museums",
    "Parties",
    "Poetry",
    "Popular_culture",
    "Circus",
    "Dance",
    "Film",
    "Music",
    "Opera",
    "Storytelling", 
    "Theatre",
    "Broadcasting", 
    "Film", 
    "Internet", 
    "Magazines", 
    "Newspapers", 
    "Publications", 
    "Publishing", 
    "Television", 
    "Radio"
  ]
  h["health"] = [ 
    "Health_promotion", 
    "Life_extension", 
    "Prevention",
    "Sexual_health",
    "Sleep", 
    "Care",
    "Mental_health",
    "Healthcare", 
    "Health_law", 
    "Health_promotion",
    "Health_standards",
    "Hospitals",
    "Occupational_safety_and_health",
    "Pharmaceutical_industry",
    "Pharmaceuticals_policy",
    "Safety"
  ]
  h["tech"] = [
    "Artificial_intelligence", 
    "Companies", 
    "Computer_model", 
    "Computer_engineering", 
    "Computer_science",
    "Computer_security", 
    "Computing_and_society",
    "Information_systems",
    "Information_technology",
    "Operating_systems", 
    "Platforms", 
    "Software",
    "Unsolved_problems_in_computer_science",
    "Avionics",
    "Digital_electronics", 
    "Water_technology",  
    "Surveillance", 
    "Telecommunications",
    "Aerospace_engineering",
    "Bioengineering",
    "Chemical_engineering", 
    "Civil_engineering", 
    "Electrical_engineering", 
    "Environmental_engineering",
    "Nuclear_technology"
  ]
  h["science"] = [
    "Formal_sciences", 
    "Science", 
    "Biology",
    "Botany",
    "Ecology", 
    "Neuroscience",
    "Zoology",
    "Atmospheric_sciences",
    "Geography", 
    "Geology", 
    "Geophysics", 
    "Oceanography",
    "Nature", 
    "Animals", 
    "Environment", 
    "Humans", 
    "Life", 
    "Natural_resources",
    "Plants", 
    "Pollution",
    "Astronomy", 
    "Chemistry", 
    "Climate", 
    "Physics", 
    "Space", 
    "Universe"
  ]
  h["religion"] = [
    "Agnosticism",
    "Atheism",  
    "Buddhism", 
    "Chinese_folk_religion",
    "Christianity", 
    "Confucianism", 
    "Hinduism", 
    "Islam", 
    "Jainism", 
    "Judaism", 
    "Rastafarianism", 
    "Satanism", 
    "Scientology",
    "Taoism", 
    "Universalism",
    "Abrahamic_mythology", 
    "Buddhist_mythology", 
    "Christian_mythology", 
    "Hindu_mythology", 
    "Islamic_mythology", 
    "Jewish_mythology"
  ]
  h["economics"] = [
    "Economics", 
    "Business", 
    "Finance", 
    "Industries", 
    "Money"
  ]
  h["sports"] = [
    "Air_sports",
    "American_football",
    "Association_football",
    "Auto_racing",
    "Baseball",
    "Basketball",
    "Boating",
    "Boxing", 
    "Canoeing",
    "Cricket", 
    "Cycling", 
    "Exercise", 
    "Fishing", 
    "Golf", 
    "Gymnastics",
    "Horse_racing",
    "Ice_hockey",
    "Lacrosse",
    "Olympic_Games", 
    "Rugby_league", 
    "Rugby_union", 
    "Sailing", 
    "Skiing", 
    "Swimming", 
    "Tennis", 
    "Track_and_field", 
    "Walking_trails", 
    "Water_sports",
    "Whitewater_sports",
    "Climbing"
  ]
  return h


BASE_URL = "https://en.wikipedia.org/w/api.php"
CATEGORIES = get_categories()

def wiki_base_path():
  base = "/".join(os.path.abspath(__file__).split("/")[:-1])
  return "{}/wikipedia_sources".format(base)

def wiki_path(category):
  return "{}/wiki_{}.txt".format(wiki_base_path(), category)

def get_lines(line_per_category):
  tn = TextNormalizer()
  for category in CATEGORIES.keys():
    with open(wiki_path(category), "r+") as f:
      print("Loaded category {}".format(category))
      i = 0
      for line in f:
        if line:
          normalized = tn.normalize(line.lower().strip("\n")).strip()
          if normalized:
            yield (category, normalized)
          i += 1
        if i % line_per_category == 0:
          break


def append_file(main_cat, titles):
  with open(wiki_path(main_cat), "a+") as f:
    print( len( titles ) )
    cats = "\n".join( titles )
    cats = "{}\n{}".format( main_cat, cats )
    f.write( cats )


def query(payload):
  last_continue = {"continue" : ""}

  while True:
    req = payload.copy()

    if last_continue["continue"]:
      req.update(last_continue)

    result = requests.get(BASE_URL, params=req).json()

    if 'error' in result: 
      raise Error(result['error'])

    if 'warnings' in result: 
      print(result['warnings'])

    if 'query' in result: 
      yield result['query']

    if 'continue' not in result: 
      break

    last_continue = result["continue"]


def sub_cat_download(main_cat, sub_cat):
  titles = set([])

  payload = {
    "format" : "json",
    "action" : "query",
    "list" : "categorymembers",
    "cmtitle" : "Category:%s" % sub_cat
  }

  for r in query( payload ):
    members = r["categorymembers"]

    for member in members:
      print( "   ", member["title"] )
      titles.add( member["title"] )

  return titles


def normalized(title):
  return title.replace(" ", "_").lower().capitalize()


def find_and_split(title, split_on):
  try:
    last = title.split(split_on)[-1]
    normal = normalized(last)
    return normal

  except: 
    return None


def partition(titles):
  concrete, categories = [], []

  for title in titles:
    
    if title.find("File:") != -1:
      continue

    if title.find("Category") != -1:
      category = find_and_split(title, "Category:")
      categories.append( category )

    else:
      concrete.append( title )

  return concrete, categories


def retrieve_categories():
  for main_cat, sub_cats in CATEGORIES.items():
    print(main_cat)

    depth = 3
    while depth:

      for sub_cat in sub_cats:
        print( " ", sub_cat)

        new_titles = sub_cat_download( main_cat, sub_cat )
        concrete, categories = partition( new_titles )

        if not categories:
          break

        if depth > 0:
          sub_cats = categories

        else:
          concrete += categories

        append_file( main_cat, list(set(concrete)) )

      depth -= 1


def prune_categories(category_to_titles):
  total = 0
  for category, lines in category_to_titles:
    unique_tokens = list(set(lines))
    current = len(unique_tokens)
    print( "{} + {} = {}".format( total, current, total + current ) )
    total += current

    with open(wiki_path(category), "w+") as f:
      f.write("\n".join(unique_tokens))


def stream_titles(category_to_titles):
  tn = TextNormalizer()
  fin = defaultdict(list)
  for category, titles in category_to_titles:
    for title in titles:
      try:
        payload = {
          "format" : "json",
          "action" : "query",
          "titles" : title.strip("\n[#<>[]|{}]"),
          "prop" : "revisions",
          "rvprop" : "content"
        }

        for r in query( payload ):
          for _, h1 in r["pages"].items():
            print(category, h1["title"])
            content = tn.normalize( h1["revisions"][0]["*"] )
            append_file(category, [content])

      except Exception as e:
        print(e.__doc__)


if __name__ == "__main__":
  arg = 2

  if arg == 0:
    print( "Retrieving categories..." )
    retrieve_categories()

  elif arg == 1:
    print( "Pruning duplicated categories..." )
    category_to_titles = list( get_lines(line_per_category=1000) )
    prune_categories( category_to_titles )

  elif arg == 2:
    print( "Get titles for all categories" )
    category_to_titles = list( get_lines(line_per_category=1000) )
    stream_titles( category_to_titles )

  else:
    print( "Option unknown!" )


