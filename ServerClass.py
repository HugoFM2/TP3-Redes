from threading import Thread
import socket
import json
import FuncoesApoio
import JSON

BUFSZ = 1024

class ServerThread(Thread):

    def __init__ (self, addr,PORT, TimeToSend):
          Thread.__init__(self)
          self.udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
          self.udp.bind((addr,PORT))
          self.myIP = addr          
          self.myRouteTable = {"127.0.0.1": [[18, "127.0.0.1"]], "127.0.0.4": [[10, "127.0.0.4"]]}
          #AAA ips temporarios para verificar a questao do update
          self.timeToSend = TimeToSend

    def run(self):
        while True:
            msg, (ipRecebido, portaRecebida) = self.udp.recvfrom(BUFSZ)
            print()
            print("MENSAGEM RECEBIDA:",msg.decode())
            msgload = json.loads(msg.decode())
            if(msgload["type"] == "trace"):
                self.traceRoute(msg.decode())
            else:
                if(FuncoesApoio.MessageForMe(self.myIP,msgload)):
                    print("MENSAGEM PARA MIM:",msg.decode())
                else:


                    if(msgload["type"] == "data"): #Repassar mensagem se for do tipo data
                        proxServ = FuncoesApoio.GetMenorRota(self.myIP,msgload["destination"],self.myRouteTable) # retorna o proximo servidor a repassar a mensagem
                        if(proxServ == 0):
                            print("Rota nao disponivel para",msgload["destination"])
                        else:
                            print("Enviar entao essa mensagem para:",proxServ) #

            # print("Recebeu do IP:",ipRecebido, "- Mensagem Recebida:" , msg.decode())

        print('Finalizando conexao do cliente')
        self.udp.close()

    def SendMsgTo(self,msg,ipDest):
        dest = (ipDest, 55151)
        self.udp.sendto(msg.encode(), dest)

    def AddFromTable(self,ipDest,ipFrom,weight): #ipFrom -> de onde a conexao vem
        print("tipo ipfrom:",type(ipFrom))
        print("adicionado")
        if(str(ipDest) in self.myRouteTable):
            for conexao in (self.myRouteTable[str(ipDest)]):
                print("ROTA:", conexao)
                if(conexao[1] == ipFrom):
                    self.myRouteTable[str(ipDest)].remove(conexao)
                    print("Essa rota ja existe,removendo rota para sobescreve-la ")

            print("ip ja adicionado no dicionario, incorporando a conexao a chave existente")
            self.myRouteTable[str(ipDest)].append([int(weight), str(ipFrom)])
        else:
            self.myRouteTable[str(ipDest)] = [[int(weight), ipFrom]]

    def DelFromTable(self,ip):
        if (ip in self.myRouteTable):
            for conexao in self.myRouteTable[ip]: #Passa por todas as conexoes desse ip
                print("CONEXAO:", conexao)
                if(conexao[1] == self.myIP): # Se a conexao foi feita desse enlace, remover conexao
                    self.myRouteTable[ip].remove(conexao)
            if(len(self.myRouteTable[ip]) == 0): # Se apos essa remocao, a lista estiver vazia, remover a key da lista
                self.myRouteTable.pop(ip)

    def TraceCommand(self,ipDest): # Formata o 1o trace e envia para o proximo servidor
        msg = JSON.Trace(self.myIP,ipDest,[self.myIP])
        proxServ = FuncoesApoio.GetMenorRota(self.myIP,ipDest,self.myRouteTable) # retorna o proximo servidor a repassar a mensagem
        self.SendMsgTo(msg,ipDest)
        print("Enviar 1o Trace:",msg)

    def traceRoute(self,JSONmsg): # Funcao a se usar quando recebe uma mensagem do tipo trace
        msg = json.loads(JSONmsg)
        msg["hops"].append(self.myIP)
        resultJSON = json.dumps(msg)
        if(self.myIP == msg["destination"]):
            dataMsg = JSON.Data(self.myIP,msg["source"],resultJSON)
            self.SendMsgTo(dataMsg,msg["source"])# Aqui eles se invertem uma vez q o ultimo trace q recebeu e chegou ao destino precisa repassar ao de origem
            print("Enviar Data:",dataMsg,"para:",msg["source"]) # Enviar mensagem como data aqui
        else:
            print("Enviar trace:",resultJSON) #enviar mensagem como trace aqui
    
    def sendPeriodic(self, ipDest):
        dicAux = {}
        for i in self.myRouteTable:
            if (i != self.myIP):
                aux1 = FuncoesApoio.GetMenorPesoRota(self.myIP, i, self.myRouteTable)
                aux2 = FuncoesApoio.GetMenorRota(self.myIP, i, self.myRouteTable)
                aux3 = FuncoesApoio.GetMenorPesoRota(self.myIP, ipDest, self.myRouteTable)
                print("i:",i)
                print("myIp:",self.myIP)
                print("aux1:",aux1)
                print("aux2:",aux2)
                print("aux3:",aux3)
                if (ipDest != i):
                    if(aux1[1] != self.myIP):
                        aux1[0] = aux1[0] + aux3[0]
                        dicAux[i] = aux1[0]
                    else:
                        dicAux[i] = aux1[0]
            print("dicAux:",dicAux)



#dics  = [1,2,3]

#dis = [{"ipFinal" : "127.0.1.5", "pesoTotal": "10", "atravesDeQualRota": "127.0.1.5"} for k in range(len(dics))]

#    def checkDicLocalAndChangePeso(dict,ipFinal,pesoNovo,rota):
#    if 
#    if ipFinal in dict:
#        dict[ipFinal]
#        dict[ipFinal]
#            a[i]["pesoTotal"] = c
#            a[i]["atravesDeQualRota"] = d

