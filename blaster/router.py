# encoding: utf-8
from os import path
from utils.helpers import read_json


MODULE = path.dirname(path.abspath(__file__))
RESOURCES = path.join(MODULE, 'resources')
BACKUPS = path.join(MODULE, 'backups')

NEWSPAPER_CONFIG = "{}/{}".format(RESOURCES, "newspapers.json")
APP_CONFIG = "{}/{}".format(RESOURCES, "app_config.json")


def backup_path():
  return BACKUPS
  
def read_config(conf):
  return read_json(conf)

def newspaper_conf():
  return read_config(NEWSPAPER_CONFIG)

def app_conf():
  return read_config(APP_CONFIG)

def stanford_ner_conf():
  ner_conf = app_conf()["stanford_ner"]
  if ner_conf and ner_conf["ner_jar"] and ner_conf["classifier"]:
    expanded_ner = path.expanduser(ner_conf["ner_jar"])
    expanded_classifier = path.expanduser(ner_conf["classifier"])
    return ( expanded_ner, expanded_classifier ) 
  return ( None, None )

def elastic_conf():
  return app_conf()["elasticsearch"]

def log_path():
  return app_conf()["logpath"]

if __name__ == "__main__":
  pass