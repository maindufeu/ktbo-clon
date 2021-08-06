import tr_list
import json

with open('Middleware/transformations.json') as f:
  oldtr = json.load(f)

oldtr = str(oldtr)

newtr = str(tr_list.transform_l())
newtr = str(newtr)

if newtr == oldtr:
    print('no changes today')
else:
    print(newtr-oldtr)
