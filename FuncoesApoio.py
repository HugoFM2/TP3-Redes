# Funcoes de apoio para o funcionamento do programa
import numpy as np

def MessageForMe(meuIP,msgReceived): # Retorna verdadeiro se a mensagem e para mim, ou falso c.c
    if(msgReceived["destination"] == meuIP): # Se for para o meu ip, armazenar, senao repassar
        return True
    else:
        return False

def GetMenorRota(meuIP,ipDest,dict): # Retorna o IP da menor rota, para repassar a msg
    if (ipDest in dict): # Checa se existe o ip na routeTable
        min = np.argmin(dict[ipDest],axis=0)
        if(dict[ipDest][min[0]][1] == meuIP): # Se a melhor rota for atraves deste roteador, ja enviar direto
            return ipDest
        else:                                 # C.C enviar a melhor rota
            return dict[ipDest][min[0]][1]
    return 0 # Nao existem rotas disponiveis

def GetMenorPesoRota(meuIP,ipDest,dict): # Retorna o IP da menor rota, para repassar a msg
    if (ipDest in dict): # Checa se existe o ip na routeTable
        min = np.argmin(dict[ipDest],axis=0)
        return dict[ipDest][min[0]]
    return 0 # Nao existem rotas disponiveis

