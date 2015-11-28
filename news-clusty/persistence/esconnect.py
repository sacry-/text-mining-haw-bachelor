import requests
import os

from elasticsearch import Elasticsearch
from elasticsearch_dsl.connections import connections


class EsConnect():

  def __init__(self):
    self.host = os.environ["ELASTIC_HOST"]
    self.port = int(os.environ["ELASTIC_PORT"])

  def check(self):
    try:
      s = requests.get('{}/_status'.format(str(self)))
    except:
      raise Exception("Elasticsearch not running on {}".format(str(self)))

  def createConnection(self):
    self.show()
    connections.create_connection(hosts=['{}:{}'.format(self.host, self.port)])

  def getConnection(self):
    self.show()
    return Elasticsearch([{'host': self.host, 'port' : self.port}])

  def show(self):
    print("started es connection on {}".format(str(self)))

  def __repr__(self):
    return "http://{}:{}".format(self.host, self.port)

def check_es_is_up():
  EsConnect().check()
  