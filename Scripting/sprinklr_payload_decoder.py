import os
import re
import json


d = os.listdir()
payloads_generated = []
n = 1

for i in d:
  if re.match("myFile", i):
    print(n,i)
    n = n+1
    payloads_generated.append(i)

payload_selection = int(input("payload_id:"))
w1 = payloads_generated[payload_selection-1]

with open(w1) as json_file:
    json_payload = json.load(json_file)

outjson = json.dumps(json_payload[0], indent = 5)
print(outjson)
