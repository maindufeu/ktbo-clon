# coding: utf-8
import requests

params = {
  'access_key': '910b5239f69d8a4949bdb657977a81d0',
  'query': 'Tehuacán'
}

api_result = requests.get('http://api.weatherstack.com/current', params)
print(api_result)
api_response = api_result.json()

#print(u'Current temperature in %s is %d℃' % (api_response['location']['name'], api_response['current']['temperature']))
print(u'FULL RESPONSE', api_response)
