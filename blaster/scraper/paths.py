# encoding: utf-8
import os
import ast


MODULE = os.path.dirname(os.path.abspath(__file__))
RESOURCES = os.path.join(MODULE, 'resources')

def newspaper_config():
  with open(newspapers_path()) as f:
    return ast.literal_eval(f.read())

def newspapers_path():
  return "{}/{}".format(RESOURCES, "newspapers.json")

def articles_path():
  return "{}/{}".format(RESOURCES, "articles")