# -*- Coding: UTF-8 -*-
# coding: utf-8
from __future__ import print_function, unicode_literals
import os
import os.path
import requests
import glob
import json
import regex
from requests_toolbelt import MultipartEncoder
from pyfiglet import figlet_format
import urllib 
from requests_toolbelt import MultipartEncoder

from includes.questions import ask_auth,ask_pricncipalAction,ask_assetsSelectAction,ask_codesSelectAction, ask_folder

class Action:
    def __init__(self, storename, token):
        self.storename = storename
        self.token = token

    def mountUrl(self):
        return "https://" + self.storename + ".api.URL.net/api/stores/1/"

    def mountHeader(self):
        return 'teste'

def main():
    print(figlet_format('Codes & Assets Management', font='big'))
    print('Essa ferramenta faz integração com API URL via Token e Endpoint')
    auth = ask_auth()
    mainAction(auth)

def mainAction(auth):

    mainAction = ask_pricncipalAction()
    if (mainAction == 'Assets'):
        assetsAction = ask_assetsSelectAction()
        if (assetsAction == 'Subir pasta com imagens'):
            assetsUploadFolder(auth)
        elif (assetsAction == 'Baixar Tudo'):
            assetsDownloadAll(auth)
        elif (assetsAction == 'Excluir Tudo'):
            assetsDeleteAll(auth)
        elif (assetsAction == 'Excluir tudo e subir uma pasta'):
            assetsReset(auth)
        else:
            print('Selecione uma ação')
    elif (mainAction == 'Codes'):
        codestAction = ask_codesSelectAction()
        if (codestAction == 'Subir pasta com codigos'):
            codesUploadFolder(auth)
        elif (codestAction == 'Baixar Tudo'):
            codesDownloadAll(auth)
        elif (codestAction == 'Watcher(subir enquanto edita)'):
            codesWatcher()
        else:
            print('Selecione uma ação')
    elif (mainAction == 'Exit'):
        exit()
    else:
        print('Selecione uma ação')

def assetsUploadFolder(auth):
    folder = ask_folder()
    assetsUploadFolderAction(auth, folder)

def assetsDownloadAll(auth):
    print('assetsDownloadAll')

def assetsDeleteAll(auth):
    assetsDeleteAllAction(auth)

def assetsReset(auth):
    print('assetsReset')

def codesUploadFolder(auth):
    folder = ask_folder()
    codesUploadFolderAction(auth, folder)

def codesDownloadAll(auth):
    codesDownloadAllAction(auth)

def codesWatcher():
    print('codesWatcher')

def codesUploadFolderAction(auth, folder):

    url = "https://" + auth['storeName'] + \
        ".api.URL.net/api/stores/1/source-codes/"
    headersGet = {
        'Content-Type': "application/json",
        'cache-control': "no-cache",
        'Authorization': "Bearer " + auth['storeToken']
    }
    responseGet = requests.request("GET", url, headers=headersGet).json()

    folder = str(folder)
    folder = folder + "*/"


    files_grabbed = []
    types = ('*.js', '*.css', '*.blade.php')
    for files in types:
        path = folder + r"*/" + files;
        pathRoot = folder + r"/" + files;
        files_grabbed.extend(glob.glob(pathRoot))
        files_grabbed.extend(glob.glob(path))
    
    if(files_grabbed):
        for fileToUpload in files_grabbed:
            nameFile = os.path.basename(fileToUpload)
            fileopen = open(fileToUpload, 'rb',).read()
            name, ext = os.path.splitext(nameFile)

            idCode = ''
            sourceCode = ''

            for infos in responseGet['data']:
                if(nameFile == infos['view_name']):
                    idCode = str(infos['id'])
                    sourceCode = infos['source']

            content = urllib.parse.urlencode({"source":sourceCode,"content":fileopen})#"active":1,"view_name":nameFile,"id":idCode,"source":sourceCode,
            payload = "active=1&view_name=" + nameFile + "&id=" + idCode + "&" + content
            headers = {
                'Content-Type': "application/x-www-form-urlencoded",
                'cache-control': "no-cache",
                "Authorization": "Bearer " + auth['storeToken']
            }
            urlToRequest = url + idCode
            print(payload)
            response = requests.request("PUT", urlToRequest, data=payload, headers=headers)
            #coment"""
    else:
        print('Nenhum arquivo correspondente aos formatos suportados foi encontrado na pasta: "' + folder + '"')

    ask_pricncipalAction()

def codesDownloadAllAction(auth):
    url = "https://" + auth['storeName'] + \
        ".api.URL.net/api/stores/1/source-codes/"
    headers = {
        'cache-control': "no-cache",
        "Authorization": "Bearer " + auth['storeToken']
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
            print("Baixado: " + completeName)
            f = open(completeName, "wb+")
            #line =  sourceCode['content'].encode("utf-8").replace('\r', '').replace('\n', '').replace('  ', '')
            line =  sourceCode['content'].encode("utf-8")
            f.write(line)
            f.close()
        elif(ext == '.css'):
            save_path = currentDir + "\css"
            if not os.path.exists(save_path):
                os.makedirs(save_path)
            completeName = os.path.join(save_path, sourceCode['view_name'])
            print("Baixado: " + completeName)
            f = open(completeName, "wb+")
            #line =  sourceCode['content'].encode("utf-8").replace('\r', '').replace('\n', '').replace('\t', '').replace('  ', '')
            line =  sourceCode['content'].encode("utf-8")
            f.write(line)
            f.close()
        else:
            f = open(sourceCode['view_name'], "wb+")
            print("Baixado: " + sourceCode['view_name'])
            #line =  sourceCode['content'].encode("utf-8").replace('\r', '').replace('\n', '').replace('\t', '').replace('  ', '')
            line =  sourceCode['content'].encode("utf-8")
            f.write(line)
            f.close()
            
    ask_pricncipalAction()

def assetsDeleteAllAction(auth):
    url = "https://" + auth['storeName'] + \
        ".api.URL.net/api/stores/1/assets/"

    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + auth['storeToken']
    }

    response = requests.request("GET", url, headers=headers)
    response = response.json()

    for resposta in response['data']:
        urlResposta = url + str(resposta['id'])
        responseDelete = requests.delete(urlResposta, headers=headers)

        print(resposta['filename'] + ' | ' + responseDelete)


# Function to upload all images from a folder
def assetsUploadFolderAction(auth, folder):
    #Vars
    url = "https://" + auth['storeName'] + \
        ".api.URL.net/api/stores/1/assets/"
    files_grabbed = []

    # Tipos de imagens
    types = ('*.png', '*.jpeg', '*.jpg')

    for files in types:
        files_grabbed.extend(glob.glob(str(folder) + files))

    if(files_grabbed):
        print('Uploaded from: ' + folder)

        for fileToUpload in files_grabbed:

            nameFile = os.path.basename(fileToUpload)

            m = MultipartEncoder(
                fields={'filename': nameFile,'image': ('filename', open(fileToUpload, 'rb'), 'image/png')}
            )

            headersUpload = {
                'Content-Type': m.content_type,
                'cache-control': "no-cache",
                "Authorization": "Bearer " + auth['storeToken']
            }

            apiCall = requests.post(url, headers=headersUpload, data=m)

            if apiCall.status_code == 201:
                print('Uploaded : ' + nameFile)
            else:
                print('Erro: ' + apiCall.status_code)

    else:
        print('Nenhum arquivo correspondente aos formatos suportados foi encontrado na pasta: "' + folder + '"')

    ask_pricncipalAction()

if __name__ == '__main__':
    main()
