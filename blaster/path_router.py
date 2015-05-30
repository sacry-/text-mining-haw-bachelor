import sys
import os

base_path = os.path.dirname(os.path.realpath(__file__))

route_paths = [
  "persistence",
  "scraper",
  "nlp",
  "clustering",
  "summarization"
]

for route_path in route_paths:
  p = "%s/%s" % (base_path, route_path)
  if not p in sys.path:
    sys.path.insert( 0 , p )