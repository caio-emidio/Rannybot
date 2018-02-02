import requests

import json
#Pega token.json e poe na variavel dataJson
dataJson = json.load(open('token.json'))

#Quando for fazer mudanca apenas mudar no json homologacao e aqui o amb para o de baixo :) 
amb = "producao"
#amb = "homologacao"

token = dataJson['ambiente'][amb]['token']
tokenVerify = dataJson['tokenVerify']
linkGrafh = dataJson['linkGrafh']

def payloadTextoSimples(sender,retorno = ""):
    payload = {'recipient': {'id': sender}, 'message': {'text': retorno}} 
    r = requests.post(linkGrafh + token, json=payload)

def payloadLocalizacao(sender):
    payload =  { 
        "recipient": {
            "id": sender
        },
        "message": {
            "text": "Compartilhe sua localização:",
            "quick_replies": [
                {
                    "content_type": "location",
                }
            ]
        }
    }
    r = requests.post(linkGrafh + token, json=payload)

def payloadAjuda(sender, listaNumeros):
    botoes = []
    for elemento in listaNumeros:
        replies = {}
        replies['type'] = "phone_number"
        replies['title'] = "Ligar para: " + elemento[0]
        replies['payload'] = elemento[1]
        botoes.append(replies)
    payload = {
  "recipient": {
    "id": sender
  },
  "message": {
    "attachment": {
      "type": "template",
      "payload": {
        "template_type": "button",
        "text": "Precisa de ajuda?",
        "buttons": botoes
      }
    }
  }
}
    r = requests.post(linkGrafh + token, json=payload)
'''
[
  {
    "type":"web_url",
    "url":"https://www.messenger.com",
    "title":"Visit Messenger"
  }
]
'''

def payloadReplies(sender,retorno,listaReplies):
	quickReplies = []
	for repliestext in listaReplies:
		replies = {}
		replies['content_type'] = "text"
		replies['title'] = repliestext
		replies['payload'] = "<POSTBACK_PAYLOAD>"
		quickReplies.append(replies)


	payload = {
  "recipient":{
    "id":sender
  },
  "message":{
    "text": retorno,
    "quick_replies":quickReplies
  }
}
	r = requests.post(linkGrafh + token, json=payload)
