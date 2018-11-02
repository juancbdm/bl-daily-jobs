# -*- Coding: UTF-8 -*-
# coding: utf-8
import os
import os.path
import requests
import json
url = "https://API_URL.net/api/stores/1/source-codes"

headers = {
    "Content-Type" : "application/json",
    "Authorization":"Bearer JWT"
}
response = requests.request("GET", url, headers=headers)
response = response.json()
currentDir = os.path.dirname(os.path.abspath(__file__))
for sourceCode in response['data']:
    name, ext = os.path.splitext(sourceCode['view_name'])
    if(ext == '.js'):
        save_path = currentDir + "\js"
        if not os.path.exists(save_path):
            os.makedirs(save_path)
        completeName = os.path.join(save_path, sourceCode['view_name'])
        f = open(completeName, "w+")
        f.write(sourceCode['content'].encode("utf-8"))
        f.close()
    elif(ext == '.css'):
        save_path = currentDir + "\css"
        if not os.path.exists(save_path):
            os.makedirs(save_path)
        completeName = os.path.join(save_path, sourceCode['view_name'])
        f = open(completeName, "w+")
        f.write(sourceCode['content'].encode("utf-8"))
        f.close()
    else:
        f = open(sourceCode['view_name'], "w+")
        f.write(sourceCode['content'].encode("utf-8"))
        f.close()