from bs4 import BeautifulSoup
from flask import Flask, request,render_template
from paylib import payloadTextoSimples,payloadAjuda, payloadReplies

import os
import traceback
import requests
import json
import urllib.request

#Funcoes
from noticias import funcNoticias
from aleatorio import funcAleatorio
from piadas import funcPiada
from tratatexto import tratatexto

#Programa
app = Flask(__name__)

#Pega token.json e poe na variavel dataJson
dataJson = json.load(open('token.json'))

#Quando for fazer mudanca apenas mudar no json homologacao e aqui o amb para o de baixo :) 
amb = "producao"
#amb = "homologacao"

token = dataJson['ambiente'][amb]['token']
tokenVerify = dataJson['tokenVerify']
linkGrafh = dataJson['linkGrafh']

#Entradas
entrada = ['olá','oi','bom dia','ola','i aew','iae','blz', 'eae', 'e ae']
sentimentos = ['bom?','tudo bom?','esta bem?','como vai voce','como vai','voce esta legal','bem?']
megasena = ['resultado da mega','resultado da mega sena','resultado da megasena','numeros da megasena','megasena','sena']
trabalho = ['quando começou a trabalhar?','trabalha desde quando','voce trabalha ?','trabalha?']
tchau = ['ate mais','tchau','xau']
vindo = ['bem']
listafuncao = ['funcao', 'funcoes', 'functions', 'func']
noticias = ['noticia','news','noticias']
aleatorio = ['aleatorio', 'randomico']
teste = ['teste', 'try']
ajuda = ['ajuda', 'socorro', 'help', 'socoro']
meuid = ['meuid']
#Funcoes
def funcFuncao(sender):
    lista = ['megasena', 'noticias [esporte|time]', 'Aleatorio [Qtd] [Minimo] [Maximo]', 'Socorro']
    retorno = "Como estou em desevolvimento, tenho somente as seguintes funções"
    payloadReplies(sender, retorno, lista)

def funcMegasena(sender):
    #Feita por Alison Aguiar
    #Em 15/12/2017
    #Em 01/02/2018 Caio Carnelos percebeu que nao estava funcionando
    source = requests.get('http://loterias.caixa.gov.br/wps/portal/loterias/landing/megasena/').text
    soup = BeautifulSoup(source,'lxml')
    #class numbers mega-sena
    numeros = soup.find('ul',class_='numbers mega-sena')

    
    #tratamento de string
    for i in range(0,12,2):
        numeros = soup.find('ul',class_='numbers mega-sena')
        num += '-'+numeros.text[i:i+2]

    result = num[14:31]
    concurso = soup.find('div',class_='title-bar clearfix')
    resConc = concurso.h2.span.text

    retorno = 'O resultado do ultimo \n' + resConc + ' \nfoi: ' + result + ' \n\nSaiba mais aqui. \nhttp://loterias.caixa.gov.br/wps/portal/loterias/landing/megasena/\n'
    payloadTextoSimples(sender,retorno)



@app.route('/', methods=['GET', 'POST'])
def webhook():
    if request.method == 'POST':
        try:
            data = json.loads(request.data)

            text = data['entry'][0]['messaging'][0]['message']['text'] # mensagem recebida
            #A principio nao vai precisar mais :)
            #msg = str(text.lower()) #mensagem json para string
            msg = tratatexto(str(text))

            #Variaveis
            #text = MENSAGEM QUE CHEGA PARA O FACEBOOK
            #msg = text tratado. 
            #sender = quem enviou a msg.
            sender = data['entry'][0]['messaging'][0]['sender']['id'] # id do mensageiro

            if msg in entrada: 
                retorno = 'Olá tudo bem,em que posso lhe ajuda, conhece minhas funções ? :)'#Mensagem de retorno ao usuario
                payloadTextoSimples(sender,retorno)
                funcFuncao(sender)

            elif msg in listafuncao:
                funcFuncao(sender)

            elif msg in megasena:
                source = requests.get('http://loterias.caixa.gov.br/wps/portal/loterias/landing/megasena/').text

                soup = BeautifulSoup(source,'lxml')
                #class numbers mega-sena
                numeros = soup.find('ul',class_='numbers mega-sena')

                result = numeros
                concurso = soup.find('div',class_='title-bar clearfix')
                
                retorno = str(result)
                payload = {'recipient': {'id': sender}, 'message': {'text': retorno}} 
                r = requests.post(linkGrafh + token, json=payload) 

                
            elif msg in trabalho:
                retorno = 'Eu trabalho desde o dia 12 de dezembro de 2017 e ja estou na minha V41'
                payloadTextoSimples(sender,retorno) 

            elif msg in sentimentos:
                retorno = 'Estou muito Bem :) Obrigada.'
                payloadTextoSimples(sender,retorno)

            elif msg in tchau:
                retorno = 'Até mais :), estou a sua disposição'
                payloadTextoSimples(sender,retorno)

            elif msg in ajuda:
            	listaAjuda = [['Policia','190'],['SAMU','192'],['Bombeiro','193']]
            	payloadAjuda(sender,listaAjuda)

            elif msg in meuid:
                payloadTextoSimples(sender,str(sender))
            else:
                #Aqui começa a parte via token:
                splitz = msg.split()
                if splitz[0] in noticias:
                    funcNoticias(sender,msg)

                elif splitz[0] in aleatorio:
                    funcAleatorio(sender,msg)


                else:
                    retorno='Isso nao faz parte da minha função'
                    payloadTextoSimples(sender,retorno)
                    funcFuncao(sender)
            
        except Exception as e:
           print(traceback.format_exc())

    elif request.method == 'GET': # Para a verificação inicial
        if request.args.get('hub.verify_token') == tokenVerify:
            print("verificado")
            return request.args.get('hub.challenge')
        return render_template("home.html")
    return "Nada retornado"

if __name__ == '__main__':
    app.run(debug=True)
