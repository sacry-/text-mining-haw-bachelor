import os
import json


if __name__ == "__main__":
  def read_json(abs_path):
    with open(abs_path) as f:
      return json.loads(f.read())

  base = "/Users/sacry/dev/uni/bachelor/text-mining-haw-bachelor/blaster/scraper/resources/articles"

  sdirs = []
  for root, dirs, files in os.walk(base):
    for adir in dirs:
      if adir != "theguardian":
        sdirs.append(adir)

  h = {}
  for root, dirs, files in os.walk(base):
    for adir in sdirs:
      if not adir in h:
        h[adir] = []
      for f in files:
        if f.endswith(".json"):
          abs_path = os.path.join(root, f)
          if adir in abs_path:
            ajson = read_json(abs_path)
            h[adir].append( ajson ) 

  for ts, collection in h.items():
    for element in collection:
      print(e["ntitle"])

