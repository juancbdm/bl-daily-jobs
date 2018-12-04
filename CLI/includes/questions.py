# -*- Coding: UTF-8 -*-
# coding: utf-8
from __future__ import print_function, unicode_literals
import regex
from PyInquirer import style_from_dict, Token, prompt, Separator, Validator, ValidationError

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
                cursor_position=len(document.text))

def ask_auth():
    auth_prompt = [
        {
            'type': 'input',
            'name': 'storeName',
            'message': 'Nome da Loja(a url sera montada dinamicamente ex: "https://NOME_DA_LOJA.api.URL.net/api/stores/1/assets")',
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
        'choices': ['Assets', 'Codes', 'Exit'],
    }
    answers = prompt(principalAction_prompt)
    return answers['pricncipalAction']


def ask_assetsSelectAction():
    assetsSelectAction_prompt = {
        'type': 'list',
        'name': 'assetsSelectAction',
        'message': 'O que deseja fazer?',
        'choices': ['Subir pasta com imagens', 'Baixar Tudo', 'Excluir Tudo', 'Excluir tudo e subir uma pasta'],
    }
    answers = prompt(assetsSelectAction_prompt)
    return answers['assetsSelectAction']

def ask_codesSelectAction():
    codesSelectAction_prompt = {
        'type': 'list',
        'name': 'codesSelectAction',
        'message': 'O que deseja fazer?',
        'choices': ['Subir pasta com codigos', 'Baixar Tudo', 'Watcher(subir enquanto edita)'],
    }
    answers = prompt(codesSelectAction_prompt)
    return answers['codesSelectAction']

def ask_folder():
    askFolder_prompt = {
        'type': 'input',
        'name': 'folderDirectory',
        'message': r'Digite o caminho da pasta desejada(ex: "C:\xampp\htdocs\projeto\imagens\"*com barra ao final*):',
        'validate': pathValidator
    }
    # verificar com regex " ^((\.\.\/|[a-zA-Z0-9_/\-\\])*\.[a-zA-Z0-9]+)$ "
    answers = prompt(askFolder_prompt)
    return answers['folderDirectory']
