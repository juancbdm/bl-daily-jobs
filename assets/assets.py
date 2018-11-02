# -*- Coding: UTF-8 -*-
# coding: utf-8
from __future__ import print_function, unicode_literals
import os
import requests
import glob
import json
import regex
from requests_toolbelt import MultipartEncoder
from PyInquirer import style_from_dict, Token, prompt, Separator, Validator, ValidationError
from pprint import pprint
from pyfiglet import figlet_format
from termcolor import cprint

style = style_from_dict({
    Token.Separator: '#cc5454',
    Token.QuestionMark: '#673ab7 bold',
    Token.Selected: '#cc5454',
    Token.Pointer: '#673ab7 bold',
    Token.Instruction: '',
    Token.Answer: '#f44336 bold',
    Token.Question: '',
})

class pathValidator(Validator):
    def validate(self, document):
        ok = regex.match(r'^[a-zA-Z]:\\[\\\S|*\S]?.*$', document.text)
        if not ok:
            raise ValidationError(
                message='Erro na validação do caminho da pasta',
                cursor_position=len(document.text))  # Move cursor to end

def ask_auth():
    auth_prompt = [
        {
            'type': 'input',
            'name': 'storeName',
            'message': 'Nome da Loja(a url sera montada dinamicamente ex: "https://NOME_DA_LOJA.api.betalabs.net/api/stores/1/assets")',
        }, {
            'type': 'input',
            'name': 'storeToken',
            'message': 'Beare Token',
        }
    ]
    answers = prompt(auth_prompt)
    return answers

def ask_pricncipalAction():
    principalAction_prompt = {
        'type': 'list',
        'name': 'pricncipalAction',
        'message': 'O que deseja fazer?',
        'choices': ['Subir pasta com imagens', 'Baixar Tudo', 'Baixar alguma', 'Excluir alguma', 'Excluir Tudo', 'Excluir tudo e subir uma pasta'],
    }
    answers = prompt(principalAction_prompt)
    return answers['pricncipalAction']

def ask_folder():
    askFolder_prompt = {
        'type': 'input',
        'name': 'folderDirectory',
        'message': r'Digite o caminho da pasta desejada(ex: "C:\xampp\htdocs\projeto\imagens\"*com barra ao final*):',
        'validate': pathValidator
    }
    answers = prompt(askFolder_prompt)
    return answers['folderDirectory']


def main():
    cprint(figlet_format('Assets Management', font='big'))
    print('Essa ferramenta faz integração com API via Token e Endpoint')
    mainAction()


def mainAction():
    auth = ask_auth()
    mainAction = ask_pricncipalAction()
    if (mainAction == 'Subir pasta com imagens'):
        uploadFolderAction(auth)
    elif (mainAction == 'Baixar Tudo'):
        downloadAllAction()
    elif (mainAction == 'Baixar alguma'):
        downloadOneAction()
    elif (mainAction == 'Excluir alguma'):
        deleteOneAction()
    elif (mainAction == 'Excluir Tudo'):
        deleteAllAction()
    elif (mainAction == 'Excluir tudo e subir uma pasta'):
        deleteAndUploadAction()
    else:
        print('Selecione uma ação')



def uploadFolderAction(auth):
    folder = ask_folder()
    uploadFolder(auth, folder)


def downloadAllAction():
    print('Download All')


def downloadOneAction():
    print('Download One')


def deleteOneAction():
    print('Delete One')


def deleteAllAction():
    print('Delete All')


def deleteAndUploadAction():
    print('Delete ans Upload')


def uploadFolder(auth, folder):
    url = "https://" + auth['storeName'] + \
        ".API_URL.net/api/stores/1/assets/"
    files_grabbed = []

    types = ('*.png', '*.jpeg', '*.jpg')

    for files in types:
        files_grabbed.extend(glob.glob(str(folder) + files))

    if(files_grabbed):
        print('Uploaded from: ' + folder)

        for fileToUpload in files_grabbed:

            nameFile = os.path.basename(fileToUpload)

            m = MultipartEncoder(
                fields={'filename': nameFile,
                        'image': ('filename', open(fileToUpload, 'rb'), 'image/png')}
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


if __name__ == '__main__':
    main()
