import os


def base_path():
  return "/".join(os.path.abspath(__file__).split("/")[:-1])

def model_path(model_name):
  return "{}/data/{}.txt".format(base_path(), model_name)

def bbc_path():
  return "{}/bbc_raw".format(base_path())