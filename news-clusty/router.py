# encoding: utf-8
import os
import json
import ast


def evaluate(python_data):
  return ast.literal_eval(python_data)

def read_json(abs_path):
  with open(abs_path) as f:
    return evaluate(f.read())

MODULE = os.path.dirname(os.path.abspath(__file__))
CONFIG = os.path.join(MODULE, 'config')
APP_CONFIG = "{}/{}".format(CONFIG, "app_config.json")

variables = read_json(APP_CONFIG)

os.environ["LOG_PATH"] = variables["logpath"]
os.environ["CLUSTY_BACKUPS"] = variables["backups_path"]

os.environ["STANFORD_NER_JAR"] = variables["stanford_ner_jar"]
os.environ["STANFORD_NER_CLASSIFIER"] = variables["stanford_classifier"]

os.environ["ELASTIC_HOST"] = variables["elastic_host"]
os.environ["ELASTIC_PORT"] = variables["elastic_port"]
os.environ["REDIS_HOST"] = variables["redis_host"]
os.environ["REDIS_PORT"] = variables["redis_port"]