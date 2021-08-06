import requests
import json

url = "https://api2.sprinklr.com//api/v2/reports/query"

payload = json.dumps({
  "timeField": None,
  "startTime": 1626004800000,
  "endTime": 1626048000000,
  "timeZone": "UTC",
  "page": 0,
  "pageSize": 1000,
  "reportingEngine": "LISTENING",
  "report": "SPRINKSIGHTS",
  "filters": [
    {
      "dimensionName": "TOPIC_IDS",
      "filterType": "IN",
      "values": [
        "60baed0060ead003bbb77f68",
        "60baec5d60ead003bbb755d9",
        "60baee0260ead003bbb7a1d7",
        "60baedd760ead003bbb79f42",
        "60baeefb60ead003bbb7b782",
        "60baf0d760ead003bbb7de4a",
        "60baf1c160ead003bbb7f053"
      ],
      "details": {
        "contentType": "DB_FILTER",
        "DRILLDOWN": False,
        "dF": True,
        "OLD_DIM_NAME": "TOPIC",
        "EXIST_FILTER": False
      }
    }
  ],
  "groupBys": [
    {
      "heading": "ES_MESSAGE_ID",
      "dimensionName": "ES_MESSAGE_ID",
      "groupType": "FIELD",
      "details": None
    }
  ],
  "projections": [
    {
      "heading": "MENTIONS_COUNT",
      "measurementName": "MENTIONS_COUNT",
      "aggregateFunction": "SUM",
      "details": None
    }
  ],
  "sorts": None,
  "projectionDecorations": None,
  "additional": None,
  "skipResolve": False,
  "jsonResponse": True
})
headers = {
  'Authorization': 'Bearer DN5Epv8KfwagstvLfQ/9zO9Oa3h/kvTJEWwe4D1dR6Y0MTVkNDZiMzMxYjIwMjNmNmE0NmJjMjU0NmRlYzJiMg==',
  'Key': '92gj84ekt7emq9wp76p5rskm',
  'Accept': 'application/json',
  'Content-Type': 'application/json',
  'Cookie': 'AWSALB=O65LSuSh154dzXKYdV8kiWOsEVYlQSAnecOWNcXvK3EKjPkJIY/K65Eha/U3QG447HxE3Qq4DkNLj0r8dJIPHyqFi90cBLhK88YTDaPDz5hcYskcEuNkdw8akOKm; AWSALBCORS=O65LSuSh154dzXKYdV8kiWOsEVYlQSAnecOWNcXvK3EKjPkJIY/K65Eha/U3QG447HxE3Qq4DkNLj0r8dJIPHyqFi90cBLhK88YTDaPDz5hcYskcEuNkdw8akOKm'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.content)
#r = response.content
#with open('listeningquery.json', 'w') as fp:
#    json.dump(r, fp)
