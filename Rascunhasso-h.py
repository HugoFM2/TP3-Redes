import JSON
import json
import numpy as np
from Exemplos import Tables

#
# myListInicial = [ # Formato IP : Peso
# [myIp,0,myIp]
# ]
#
# myListPasso0 = [ # Formato [ipFinal, pesoTotal, AtravesDeQualRota]
# [myIp,0,myIp],
# ["127.0.1.5",10,"127.0.1.5"],
# ["127.0.1.1",20,"127.0.1.5"],
# ["127.0.1.2",20,"127.0.1.5"],
# ["127.0.1.3",20,"127.0.1.5"],
# ]
#

# myDict = { # Formato [ipFinal, pesoTotal, AtravesDeQualRota]
# myIp : [[0,myIp]],
# "127.0.1.5"  :  [[10,"127.0.1.5"]],
# "127.0.1.1"  :  [[20,"127.0.1.5"]],
# "127.0.1.3"  :  [[20,"127.0.1.5"]],
# "127.0.1.4"  :  [[20,"127.0.1.5"]],
# }
#



def MessageForMe(meuIP,msgReceived): # Retorna verdadeiro se a mensagem é para mim, ou falso c.c
    if(msgReceived["destination"] == meuIP): # Se for para o meu ip, armazenar, senao repassar
        print("ARMAZENAR MENSAGEM AQUI")
        return True
    else:
        return False

def GetMenorRota(meuIP,ipDest,dict): # Retorna o IP da menor rota, para repassar a msg
    if (ipDest in dict): # Checa se existe o ip na routeTable
        min = np.argmin(dict[ipDest],axis=0)
        # print("MINIMO:",min)
        if(dict[ipDest][min[0]][1] == meuIP): # Se a melhor rota for atraves deste roteador, já enviar direto
            return ipDest
        else:                                 # C.C enviar a melhor rota
            return dict[ipDest][min[0]][1]
    return 0 # Nao existem rotas disponiveis

print(GetMenorRota("127.0.1.4","127.0.1.1",Tables.dictRoute4))

# if(RecebeTrace):
#     - adiciona my ip ao final de hops, caso o myip seja igual ao destination, adicionar ao final e
#         mandar como data para o source
#     - caso nao seja, manda a mensagem para o proximo

def traceCommand(meuIP,ipDest):
    msg = JSON.Trace(meuIP,ipDest,[meuIP])
    print("Enviar 1o Trace",msg)

def traceRoute(meuIP,JSONmsg):
    msg = json.loads(JSONmsg)
    msg["hops"].append(meuIP)
    resultJSON = json.dumps(msg)
    if(meuIP == msg["destination"]):
        dataMsg = JSON.Data(meuIP,msg["source"],resultJSON)
        print("Enviar Data:",dataMsg) # Enviar mensagem como data aqui
    else:

        print("Enviar trace:",resultJSON) #enviar mensagem como trace aqui





# print(getRoutesFromIP(dictRoute,"127.0.1.5"))
# getMinimumDistanceRoute(myDict,"127.0.1.2")
# TraceMSG = "{\"type\": \"trace\",\"source\": \"127.0.1.1\",\"destination\": \"127.0.1.2\",\"hops\": [] }"
traceCommand(Tables.meuIP1,Tables.meuIP2)
msgRecebida5 = "{\"type\": \"trace\", \"source\": \"127.0.1.1\", \"destination\": \"127.0.1.2\", \"hops\": [\"127.0.1.1\"]}"
traceRoute(Tables.meuIP5,msgRecebida5) # msg enviada do 127.0.1.5, para o 127.0.1.2
msgRecebida2 = "{\"type\": \"trace\", \"source\": \"127.0.1.1\", \"destination\": \"127.0.1.2\", \"hops\": [\"127.0.1.1\", \"127.0.1.5\"]}"
traceRoute(Tables.meuIP2, msgRecebida2)
# traceRoute
# print(msgRecebida5)
# msgRecebida2 = traceRoute(meuIP2,msgRecebida5)
# print(msgRecebida2)
