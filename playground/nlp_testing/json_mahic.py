import json


json1 = {"a" : "b"}
json2 = {"a" : "b"}
json3 = {"a" : "b"}
json4 = {"a" : "b"}

articles = [json1, json2, json3, json4]

res = []
for a in articles:
  res.append(a)
with open("backup.json", "w+") as f:
  data = json.dumps(res, indent=2)
  f.write(data)