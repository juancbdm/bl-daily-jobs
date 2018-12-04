# -*- Coding: UTF-8 -*-
# coding: utf-8
import os.path
import requests
currentDir = os.path.dirname(os.path.abspath(__file__))
currentDir = os.path.join(currentDir, 'urls.json')

x = 0
while True:
    offset = x * 100
    x += 1
    url = "https://NAME.api.URL.net/api/stores/1/urls?_limit=100&_offset=" + str(offset) + "&_sort=-id"
    token = ""
    headers = {
        'cache-control': "no-cache",
        "Authorization": "Bearer " + token
    }
    response = requests.request("GET", url, headers=headers)
    responsejson = response.json()
    lenght = len(responsejson['data'])

    if(response.status_code != 200 or lenght <= 0):
        print('Todas URLs(%s paginas) em urls.json' % (x))
        break
        exit()

    retorno = str(responsejson['data'][0])
    f = open(currentDir, 'a')
    f.write(retorno)
    print('Download URLs, página:' + str(x))

#print('teste' + str(x))
#coment"""
