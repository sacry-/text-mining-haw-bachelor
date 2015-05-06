import request
import json
import xml
import csv


class ApiAdapter(object):

  def __init__(self, config):
    self.config = config

  def get(self):
    raise "Not implemented"

  def post(self):
    raise "Not implemented"

  def reqquest(self):
    raise "Not implemented"

  def newest_articles(self):
    raise "Not implemented"

  def all_articles(self):
    raise "Not implemented"

  def persist(self):
    raise "Not implemented"


class TheGuardian(ApiAdapter):

  def __init__(self, config):
    self.api_key = config.api_key
    self.base_url = config.base_url
    self.cached = config.cached

  def newest_articles(self):
    pass

  def all_articles(self):
    pass

  def persist(self):
    pass

class GuardianData(self):

  def __init__(self):
    pass

class NYT(ApiAdapter):

  def __init__(self, config):
    self.api_key = config.api_key
    self.base_url = config.base_url
    self.cached = config.cached

  def newest_articles(self):
    pass

  def all_articles(self):
    pass

  def persist(self):
    pass

class NYTData(ApiAdapter):

  def __init__(self):
    pass

