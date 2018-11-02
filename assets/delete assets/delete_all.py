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

for resposta in response['data']:
    urlResposta = url + str(resposta['id'])
    responseDelete = requests.delete(urlResposta, headers=headers)

    print(resposta['filename'] + ' | ' + urlResposta)
    