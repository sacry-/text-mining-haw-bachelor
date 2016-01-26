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
def set_env_var(var, config_var):
  global variables

  if config_var in variables:
    var_value = variables[config_var]
    if var_value:
      os.environ[var] = var_value

  if not var in os.environ:
    raise Exception(
      "Please provide a valid argument for {} via ENV or in app_config.json via {}".format(var, config_var)
    )

set_env_var("LOG_PATH", "logpath")
set_env_var("CLUSTY_BACKUPS", "backups_path")

set_env_var("STANFORD_NER_JAR", "stanford_ner_jar")
set_env_var("STANFORD_NER_CLASSIFIER", "stanford_classifier")

set_env_var("ELASTIC_HOST", "elastic_host")
set_env_var("ELASTIC_PORT", "elastic_port")
set_env_var("REDIS_HOST", "redis_host")
set_env_var("REDIS_PORT", "redis_port")
