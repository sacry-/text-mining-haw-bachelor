from datetime import date
from elastic import Elastic
from logger import Logger


logger = Logger(__name__).getLogger()

class EsScraper():

  def __init__(self, paper):
    self.paper = paper
    self.es = Elastic()

  def save(self, data):
    logger.info("es: " + self.paper + " - " + data["ntitle"])
    self.es.index_doc(self.date_today(), self.paper, data["ntitle"], data)

  def date_today(self):
    return date.today().strftime("%Y%m%d")