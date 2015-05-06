# encoding: utf-8
import os


MODULE = os.path.dirname(os.path.abspath(__file__))
RESOURCES = os.path.join(MODULE, 'resources')

def newspapers_path():
  return "{}/{}".format(RESOURCES, "newspapers.json")

def articles_path():
  return "{}/{}".format(RESOURCES, "articles")