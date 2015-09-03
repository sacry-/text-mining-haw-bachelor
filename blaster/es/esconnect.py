from elasticsearch import Elasticsearch
from elasticsearch_dsl.connections import connections


class EsConnect():

  def __init__(self, config=None):
    self.host = "localhost" 
    self.port = 9200
    if config:
      self.host = config["host"]
      self.port = config["port"]

  def createConnection(self):
    connections.create_connection(hosts=['{}:{}'.format(self.host, self.port)])
    self.show()

  def getConnection(self):
    self.show()
    return Elasticsearch([{'host': self.host, 'port' : self.port}])

  def show(self):
    print("started connection with",self.host,":",self.port)