import os
import requests
import glob
import json
from requests_toolbelt import MultipartEncoder

url = "https://API_URL.net/api/stores/1/assets/"

headers = {
    "Content-Type" : "application/json",
    "Authorization":"Bearer JWT"
}

response = requests.request("GET", url, headers=headersDelete)
response = response.json()

for resposta in response['data']:
    urlResposta = url + str(resposta['id'])
    responseDelete = requests.delete(urlResposta, headers=headersDelete)

    print(resposta['filename'] + ' | ' + urlResposta)

files_grabbed = []

types = ('*.png', '*.jpeg', '*.jpg')

for files in types:
    files_grabbed.extend(glob.glob(r"C:\xampp\htdocs\PATH\scripts\assets\reset_assets\images_to_upload\/" + files ))

for fileToUpload in files_grabbed:

    nameFile = os.path.basename(fileToUpload)
    fileopen = open(fileToUpload, 'rb').read()
    payload = {'image': (fileopen)}

    m = MultipartEncoder(
        fields={'filename': nameFile,
                'image': ('filename', open(fileToUpload, 'rb'), 'image/png')}
        )

    headersUpload = {
        'Content-Type': m.content_type,
        'cache-control': "no-cache",
        "Authorization":"Bearer JWT"
    }

    response = requests.post(url, headers=headersUpload, data=m)
    print('Uploaded : ' + nameFile)