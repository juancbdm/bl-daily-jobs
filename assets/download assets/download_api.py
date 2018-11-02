import os
import requests
import json

url = "https://API_URL.net/api/stores/1/assets/"

headers = {
    "Content-Type" : "application/json",
    "Authorization":"Bearer JWT"
}

response = requests.request("GET", url, headers=headers)
response = response.json()
#print(response)

for resposta in response['data']:
    urlResposta = "https://API_URL.net/production/VAR/images/stores/1/" + resposta['filename']
    
    result = requests.get(urlResposta, stream=True)
    if result.status_code == 200:
        image = result.raw.read()
        open(resposta['filename'],"wb").write(image)
        print('Download: ' + resposta['filename'] + ' | From: ' + urlResposta )