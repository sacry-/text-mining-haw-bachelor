from utils.logger import Logger
from persistence import EsConnect

from preprocessing.preprocessor import Prep


logger = Logger(__name__).getLogger()

class PrepPersister():

  def __init__(self, connector=None):
    if not connector:
      connector = EsConnect()
    connector.createConnection()

  def save(self, prep):
    try:
      Prep.init()
      prep.save()
      logger.info(self.log_text("preprocessed", prep))
    except Exception as e:
      logger.error(self.log_text("article could not be created", prep, str(e)))
      return False
    return True

  def log_text(self, msg, prep, err=""):
    return "{}: {}/prep/{} - {}".format(msg, prep._index, prep.meta.id, err)


if __name__ == "__main__":
  pass
