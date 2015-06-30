import os
import json
import re
from datetime import datetime
form esscraper import EsScraper


def read_json(abs_path):
  with open(abs_path) as f:
    return json.loads(f.read())

if __name__ == "__main__":
  persister = EsScraper("theguardian")

  articles = "/Users/sacry/dev/uni/bachelor/text-mining-haw-bachelor/blaster/resources/articles"

  for folder_date in os.listdir(articles):

    date_path = articles + "/" + folder_date

    for paper in os.listdir(date_path):

      paper_path = date_path + "/" + paper

      for articlejson in os.listdir(paper_path):  

        article_path = paper_path + "/" + articlejson
        article = articlejson.split(".json")[0]
        
        data = read_json(article_path)

        persister.save(data)




