import logging
from os import path


class Logger():

  def __init__(self, name):
    self.name = name
    self.logger = logging.getLogger(self.name)

  def getLogger(self):
    self.logger = logging.getLogger(self.name)
    handler = logging.FileHandler(self.log_path(self.name))
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    self.logger.addHandler(handler)
    self.logger.setLevel(logging.INFO)
    return self.logger

  def log_path(self, name):
    p = path.dirname(path.realpath(__file__))
    return "%s/log/%s.log" % (p, name)