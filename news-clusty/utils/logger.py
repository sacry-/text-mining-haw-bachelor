import logging
import os


class Logger():

  def __init__(self, name):
    self.name = name
    self.logger = logging.getLogger(self.name)

  def getLogger(self):
    self.logger = logging.getLogger(self.name)
    handler = logging.FileHandler("{}/{}.log".format(os.environ["LOG_PATH"], self.name))
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    self.logger.addHandler(handler)
    self.logger.setLevel(logging.INFO)
    return self.logger


if __name__ == "__main__":
  pass