import logging
import json
import io
import paths

from datetime import date
from os import makedirs
from logger import Logger

logger = Logger(__name__).getLogger()

class Persister():

  def __init__(self, paper):
    self.paper = paper
    self.base = self.base_path()
    self.create_base()

  def create_base(self):
    makedirs(self.base, exist_ok=True)

  def save(self, data):
    ppath = self.path_for_article(data["ntitle"])
    with io.open(ppath, 'w+', encoding='utf-8') as f:
      json_data = json.dumps(data, indent=2, sort_keys=True)
      logger.info(self.paper + " - " + data["ntitle"])
      f.write(json_data)

  def path_for_article(self, ntitle):
    return "{}/{}.json".format(self.base, ntitle)

  def base_path(self):
    return "{}/{}/{}".format(paths.articles_path(), self.date_today(), self.paper)

  def date_today(self):
    return date.today().strftime("%Y%m%d")

