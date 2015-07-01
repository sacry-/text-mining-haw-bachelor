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
    log_dir = path.dirname(path.abspath(__file__))
    return "{}/log/{}.log".format(log_dir, name)