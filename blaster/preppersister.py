from logger import Logger
from esconnect import EsConnect

from preprocessor import prep_from_chunk
from preprocessor import Prep


logger = Logger(__name__).getLogger()

class PrepPersister():

  def __init__(self, connector=None):
    if not connector:
      connector = EsConnect()
    self.es = connector.createConnection()

  def save(self, prep):
    try:
      Prep.init()
      prep.save()
      logger.info(self.logging_text(prep))
    except Exception as e:
      logger.error("article could not be created: " + e)
      return False
    return True

  def logging_text(self, prep):
    return "preprocessed: {}/prep/{}".format(prep._index, prep.meta.id)


if __name__ == "__main__":
  pass
