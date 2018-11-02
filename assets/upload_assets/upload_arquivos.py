import os
import requests
import glob
import json
from requests_toolbelt import MultipartEncoder

files_grabbed = []

types = ('*.png', '*.jpeg', '*.jpg')

for files in types:
    files_grabbed.extend(glob.glob(r"C:\Users\Juan\Desktop\PATH\upload_imagens\images_to_upload\/" + files ))

urlToRequest = "https://API_URL.net/api/stores/1/assets"

def pretty_print_POST(req):
    print('{}\n{}\n{}\n\n{}'.format(
        '-----------START-----------',
        req.method + ' ' + req.url,
        '\n'.join('{}: {}'.format(k, v) for k, v in req.headers.items()),
        req.body,
    ))

for fileToUpload in files_grabbed:

    nameFile = os.path.basename(fileToUpload)
    fileopen = open(fileToUpload, 'rb').read()
    payload = {'image': (fileopen)}

    m = MultipartEncoder(
        fields={'filename': nameFile,
                'image': ('filename', open(fileToUpload, 'rb'), 'image/png')}
        )

    headers = {
        'Content-Type': m.content_type,
        'cache-control': "no-cache",
        "Authorization":"Bearer JWT"
    }

    response = requests.post(urlToRequest, headers=headers, data=m)

    if response == 201:
        print('Uploaded : ' + nameFile)
