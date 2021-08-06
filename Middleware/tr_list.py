import requests
import json
from pprint import pprint
import subprocess

###Authorization
url = "https://KTBO.datatap.adverity.com/api/transformer/"

payload={}
headers = {
  'Authorization': 'Token c49e653ffa8a0c80768bbf1af0887905a56fff9b'
}
###request
response = requests.request("GET", url, headers=headers, data=payload).json()
t_list = response['results']

###loop to get all pages
while response['next'] is not None:
    url = response['next']
    response = requests.request("GET", url, headers=headers, data=payload).json()
    t_list.extend(response['results'])
    #print(response['next'])

#pprint(t_list)

###loop to get all the instructions
inst = {'transformations':[]}
inst_d = {'name':[],'tr':[]}

t_dict = {}

cont = 1
N = len(t_list)

for i in t_list:
    url = f'https://KTBO.datatap.adverity.com/api/transformer/{i["id"]}'
    response = requests.request("GET", url, headers=headers, data=payload).json()
    #print(url)
    transform2 = response['instructions']
    key_name = response['name']

    print("%i/%i ---- %s"%(cont, N, key_name))
    cont = cont + 1

    #print(key_name, transform2)
    t_dict[key_name] = transform2


with open('transformations.json', 'w') as fp:
    json.dump(t_dict, fp)
    subprocess.call('git add . >> log_transformations.log', shell=True)
    subprocess.call('git commit -m "trans" >> log_transformations.log', shell=True)
    subprocess.call('git push >> log_transformations.log', shell=True)
    subprocess.call('date >> log_transformations.log', shell=True)
    subprocess.call('echo "---pushed" >> log_transformations.log', shell=True)
    print("transformation updated")
