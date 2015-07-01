# encoding: utf-8
from os import path
import ast
from utils import read_json


MODULE = path.dirname(path.abspath(__file__))
RESOURCES = path.join(MODULE, 'resources')

NEWSPAPER_CONFIG = "{}/{}".format(RESOURCES, "newspapers.json")
APP_CONFIG = "{}/{}".format(RESOURCES, "app_config.json")


def read_config(conf):
  return read_json(conf)

def newspaper_conf():
  return read_config(NEWSPAPER_CONFIG)

def app_conf():
  return read_config(APP_CONFIG)

def stanford_ner_conf():
  ner_conf = app_conf()["stanford_ner"]
  if ner_conf and ner_conf["ner_jar"] and ner_conf["classifier"]:
    return ( ner_conf["ner_jar"], ner_conf["classifier"] ) 
  return ( None, None )
