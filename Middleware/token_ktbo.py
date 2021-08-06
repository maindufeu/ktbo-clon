import requests

data= {'username':'edher@ktbo.com','password':'Schopenhauer2021&'}
response=requests.post('https://KTBO.datatap.adverity.com/api/auth/token/', data=data)
print(response.content)
